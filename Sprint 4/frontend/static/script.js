// ─────────────────────────────────────────────────────────────────────────────
// BetDesicion — Frontend adaptado a FastAPI
// Versión con gamificación de Megatron (balones, mensajes, perfil)
// Con retardo para mostrar el mensaje del perfil
// ─────────────────────────────────────────────────────────────────────────────

const API = 'http://localhost:8000';

async function apiPost(endpoint, body) {
  const res = await fetch(API + endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  return res.json();
}

async function apiGet(endpoint) {
  const res = await fetch(API + endpoint);
  return res.json();
}

$(document).ready(function () {

  var app = {
    currentUser: null,
    selectedAlgo: 'pd',
    historyFilter: 'all',
    matches: [],
    history: [],
    lastResult: null,
    megatronBalloons: 0,
    hasPendingBets: false,
    profileMessageTimeout: null   // para controlar el retardo
  };

  var savedUser = sessionStorage.getItem('BetDesicion_user');
  if (savedUser) {
    try { app.currentUser = JSON.parse(savedUser); } catch (e) { }
  }

  var savedBalloons = sessionStorage.getItem('megatron_balloons');
  if (savedBalloons !== null) {
    app.megatronBalloons = parseInt(savedBalloons);
  }

  var fullPath = location.pathname;
  if (fullPath !== '/' && fullPath !== '/login') {
    if (!app.currentUser) {
      location.href = '/login';
    } else {
      $('#navbar-username').text(app.currentUser.nombre);
      if (fullPath === '/partidos-page') loadMatches();
      if (fullPath === '/historial-page') loadHistory();
    }
  }

  window.goTo = function (n) {
    var pages = { 1: '/partidos-page', 2: '/optimizar-page', 3: '/historial-page' };
    if (pages[n]) location.href = pages[n];
  };

  window.switchLoginTab = function (tab) {
    $('.tab-btn').removeClass('active');
    $('.login-form').removeClass('active');
    $('#btn-tab-' + tab).addClass('active');
    $('#form-' + tab).addClass('active');
  };

  window.handleLogin = async function () {
    var email = $('#login-email').val().trim();
    var pass = $('#login-pass').val();
    if (!email || !pass) { showToast('Completa todos los campos', 'error'); return; }

    $('#btn-login').html('<span class="spinner"></span> Entrando...').prop('disabled', true);

    try {
      var resp = await apiPost('/login', { correo: email, password: pass });
      if (resp.ok) {
        app.currentUser = { id: resp.id, nombre: resp.nombre };
        loginSuccess();
      } else {
        showToast(resp.detail || 'Credenciales incorrectas', 'error');
        $('#btn-login').html('ENTRAR AL SISTEMA').prop('disabled', false);
      }
    } catch (e) {
      showToast('Error de conexión. ¿Está corriendo el backend?', 'error');
      $('#btn-login').html('ENTRAR AL SISTEMA').prop('disabled', false);
    }
  };

  window.handleRegister = async function () {
    var name = $('#reg-name').val().trim();
    var email = $('#reg-email').val().trim();
    var pass = $('#reg-pass').val();
    if (!name || !email || !pass) { showToast('Completa todos los campos', 'error'); return; }
    if (pass.length < 6) { showToast('La contraseña debe tener al menos 6 caracteres', 'error'); return; }

    $('#btn-register').html('<span class="spinner"></span> Creando cuenta...').prop('disabled', true);

    try {
      var resp = await apiPost('/registro', { nombre: name, correo: email, password: pass });
      if (resp.ok) {
        var login = await apiPost('/login', { correo: email, password: pass });
        app.currentUser = { id: login.id, nombre: login.nombre };
        loginSuccess();
      } else {
        showToast(resp.detail || 'Error al registrar', 'error');
        $('#btn-register').html('CREAR CUENTA').prop('disabled', false);
      }
    } catch (e) {
      showToast('Error de conexión. ¿Está corriendo el backend?', 'error');
      $('#btn-register').html('CREAR CUENTA').prop('disabled', false);
    }
  };

  function loginSuccess() {
    sessionStorage.setItem('BetDesicion_user', JSON.stringify(app.currentUser));
    showToast('¡Bienvenido, ' + app.currentUser.nombre + '!', 'success');
    setTimeout(function () { location.href = '/partidos-page'; }, 800);
  }

  window.handleLogout = function () {
    sessionStorage.removeItem('BetDesicion_user');
    app.currentUser = null;
    showToast('Sesión cerrada', 'info');
    setTimeout(function () { location.href = '/login'; }, 600);
  };

  async function loadMatches() {
    try {
      var data = await apiGet('/partidos');
      app.matches = data.partidos.map(function (p) {
        return {
          local: p.local,
          visitante: p.visitante,
          momio_local: p.momios.local.momio,
          momio_empate: p.momios.empate.momio,
          momio_visitante: p.momios.visitante.momio,
          prob_local: p.momios.local.prob,
          prob_empate: p.momios.empate.prob,
          prob_visitante: p.momios.visitante.prob,
          recomendado: p.recomendado.resultado,
          ev_local: p.recomendado.ev,
          ev_positivo: p.ev_positivo
        };
      });
      renderMatchList();
    } catch (e) {
      showToast('No se pudieron cargar los partidos', 'error');
      $('#match-list').html('<div class="empty-state"><div class="icon">⚠</div><p>Error al cargar partidos.</p></div>');
    }
  }

  function renderMatchList() {
    var positivos = app.matches.filter(function (m) { return m.ev_positivo; });
    var negativos = app.matches.filter(function (m) { return !m.ev_positivo; });
    $('#stat-total').text(app.matches.length);
    $('#stat-positivos').text(positivos.length);
    $('#stat-negativos').text(negativos.length);

    var html = '';
    $.each(app.matches, function (i, m) {
      var isPos = m.ev_positivo;
      var evPct = (parseFloat(m.ev_local) * 100).toFixed(1);
      var evSign = isPos ? '+' : '';

      var pills = [
        { label: 'Local', momio: m.momio_local, prob: m.prob_local, rec: m.recomendado === 'Local' },
        { label: 'Empate', momio: m.momio_empate, prob: m.prob_empate, rec: m.recomendado === 'Empate' },
        { label: 'Visitante', momio: m.momio_visitante, prob: m.prob_visitante, rec: m.recomendado === 'Visitante' },
      ];
      var pillsHtml = pills.map(function (pill) {
        var style = pill.rec ? ' style="background:rgba(0,230,118,.15);border-color:rgba(0,230,118,.4);color:#00e676;"' : '';
        return '<div class="odd-pill"' + style + '>' +
          (pill.rec ? '🟢 ' : '') + pill.label +
          ' <span>' + pill.momio + '</span>' +
          ' <span style="color:var(--text-dim);font-size:.7rem;">(' + pill.prob + '%)</span>' +
          '</div>';
      }).join('');

      html += '<div class="match-card ' + (isPos ? 'ev-positive' : 'ev-negative') + '">' +
        '<div class="match-rank ' + (i < 3 ? 'top' : '') + '">#' + (i + 1) + '</div>' +
        '<div class="match-info">' +
        '<div class="match-teams">' + m.local + ' <span class="vs-tag">VS</span> ' + m.visitante + '</div>' +
        '<div class="match-odds">' + pillsHtml + '</div>' +
        '</div>' +
        '<div class="match-ev">' +
        '<div class="ev-val ' + (isPos ? 'pos' : 'neg') + '">' + evSign + evPct + '%</div>' +
        '<div class="ev-lbl">EV</div>' +
        '</div>' +
        '<div class="match-action">' +
        (isPos
          ? '<span class="badge badge-green">✓ EV Positivo</span>'
          : '<span class="badge badge-red">✗ EV Negativo</span>') +
        '</div>' +
        '</div>';
    });
    $('#match-list').html(html);
  }

  window.selectAlgo = function (a) {
    app.selectedAlgo = a;
    $('.algo-btn').removeClass('active');
    $('#algo-' + a).addClass('active');
  };

  window.calcularOptimo = async function () {
    var capital = parseFloat($('#capital-input').val());
    if (!capital || capital < 100) { showToast('Ingresa un capital mínimo de $100', 'error'); return; }

    $('#btn-calcular').html('<span class="spinner"></span> Calculando...').prop('disabled', true);
    $('#results-section').hide();
    $('#algo-metrics').hide();

    try {
      var resp = await apiPost('/calcular', { capital: capital });

      if (resp.ok) {
        var partidos = resp.distribucion.map(function (item) {
          return {
            partido: item.partido,
            resultado: item.resultado,
            momio: item.momio,
            prob: item.prob,
            peso: item.peso
          };
        });
        await apiPost('/guardar', {
          usuario_id: app.currentUser.id,
          jornada: 'Liguilla CL2026 — Cuartos',
          capital: capital,
          ganancia_est: resp.ganancia_estimada,
          partidos: partidos
        });

        app.lastResult = resp;

        var algoKey = 'programacion_dinamica';
        var algoData = resp.comparativa[algoKey];
        var garantia = 'Óptimo ✓';

        var metricas = {
          operaciones: algoData.complejidad,
          tiempo_ms: algoData.tiempo_ms,
          garantia: garantia
        };

        var bets = resp.distribucion.map(function (item) {
          return {
            partido: item.partido,
            resultado: item.resultado,
            momio: item.momio,
            ev: item.ev,
            monto: item.peso,
            ganancia_esperada: item.valor
          };
        });

        renderResults(bets, capital, metricas);
        showToast('Sugerencia guardada en tu historial', 'success');
      } else {
        showToast(resp.detail || 'Error al calcular', 'error');
      }
    } catch (e) {
      showToast('Error de conexión con el servidor', 'error');
    }
    $('#btn-calcular').html('CALCULAR').prop('disabled', false);
  };

  function renderResults(bets, capital, metricas) {
    $('#algo-metrics').css('display', 'grid');
    $('#metric-ops').text(metricas.operaciones);
    $('#metric-time').text(metricas.tiempo_ms + ' ms');
    $('#metric-opt').text(metricas.garantia);

    var html = '';
    $.each(bets, function (i, b) {
      html += '<div class="result-card recommended">' +
        '<div>' +
        '<div class="result-team">' + b.partido + '</div>' +
        '<div class="result-meta">' +
        '<span style="background:rgba(0,230,118,.15);border:1px solid rgba(0,230,118,.4);color:#00e676;padding:.15rem .5rem;border-radius:4px;font-weight:700;margin-right:.5rem;">' +
        '🟢 ' + b.resultado + '</span>' +
        'Momio: ' + b.momio + ' · EV: +' + (parseFloat(b.ev) * 100).toFixed(1) + '%' +
        '</div>' +
        '</div>' +
        '<div class="result-amount">' +
        '<div class="amount-val">$' + b.monto + '</div>' +
        '<div class="amount-lbl">Apostar</div>' +
        '</div>' +
        '<div class="result-gain">' +
        '<div class="gain-val">+$' + parseFloat(b.ganancia_esperada).toFixed(2) + '</div>' +
        '<div class="gain-lbl">Ganancia esp.</div>' +
        '</div>' +
        '</div>';
    });
    $('#results-list').html(html);

    var totalApostado = 0, totalGanancia = 0;
    $.each(bets, function (i, b) {
      totalApostado += parseFloat(b.monto);
      totalGanancia += parseFloat(b.ganancia_esperada);
    });
    $('#summary-bar').html(
      '<div class="summary-item"><div class="summary-val" style="color:var(--gold)">$' + capital + '</div><div class="summary-lbl">Capital Total</div></div>' +
      '<div class="summary-item"><div class="summary-val" style="color:var(--cyan)">$' + totalApostado.toFixed(0) + '</div><div class="summary-lbl">Total Apostado</div></div>' +
      '<div class="summary-item"><div class="summary-val" style="color:var(--text-dim)">$' + (capital - totalApostado).toFixed(0) + '</div><div class="summary-lbl">Capital Libre</div></div>' +
      '<div class="summary-item"><div class="summary-val" style="color:var(--green)">+$' + totalGanancia.toFixed(2) + '</div><div class="summary-lbl">Ganancia Esperada ⚠</div></div>'
    );
    $('#results-section').show();
  }

  async function loadHistory() {
    if (!app.currentUser) return;
    try {
      var data = await apiGet('/historial/' + app.currentUser.id);
      app.history = data.historial.map(function (sug) {
        return {
          id: sug.id,
          fecha: sug.fecha ? sug.fecha.substring(0, 10) : '—',
          capital: sug.capital,
          ganancia_est: sug.ganancia_est,
          algoritmo: 'pd',
          apuestas: (sug.partidos || []).map(function (p) {
            return {
              id: p.id,
              partido: p.partido,
              resultado_sug: p.resultado_sug || '',
              monto: p.apuesta,
              ganancia_esperada: 0,
              resultado: p.acerto === 1 ? 'hit' : p.acerto === 0 ? 'miss' : 'pending'
            };
          })
        };
      });
      updateAccuracyStats(data.pct_aciertos);
      renderHistory();

      // Detectar pendientes
      var anyPending = false;
      for (var i = 0; i < app.history.length; i++) {
        for (var j = 0; j < app.history[i].apuestas.length; j++) {
          if (app.history[i].apuestas[j].resultado === 'pending') {
            anyPending = true;
            break;
          }
        }
        if (anyPending) break;
      }

      if (anyPending && !app.hasPendingBets) {
        app.hasPendingBets = true;
        showMegatronMessage("¡Hola! Tienes una recomendación pendiente por confirmar si se acertó o no. ¡No la dejes pasar!", false);
      }

      // Mostrar mensaje de perfil solo si hay balones, pero con retraso de 3 segundos
      if (app.megatronBalloons > 0) {
        // Limpiar timeout anterior si existe
        if (app.profileMessageTimeout) clearTimeout(app.profileMessageTimeout);
        app.profileMessageTimeout = setTimeout(function () {
          showMegatronMessage("¡Megatron sabe qué tipo de apostador eres!", true);
        }, 3000); // 3 segundos de pausa
      }

      // Actualizar contador visual
      updateBalloonCounter();

    } catch (e) {
      showToast('Error al cargar historial', 'error');
    }
  }

  window.markResult = async function (sesionId, apuestaId, resultado) {
    try {
      var resp = await apiPost('/acierto', {
        detalle_id: apuestaId,
        acerto: resultado === 'hit'
      });
      if (resp.ok) {
        if (resultado === 'hit') {
          app.megatronBalloons++;
          updateBalloonCounter();
          showMegatronMessage("¡Ganaste un balón! Megatron está feliz porque acertaste 🤖⚽", false);
          // Tras marcar acierto, si ya había timeout para el mensaje de perfil, lo cancelamos y reagendamos
          if (app.profileMessageTimeout) clearTimeout(app.profileMessageTimeout);
          app.profileMessageTimeout = setTimeout(function () {
            if (app.megatronBalloons > 0) {
              showMegatronMessage("¡Megatron sabe qué tipo de apostador eres!", true);
            }
          }, 3000);
        } else {
          showMegatronMessage("Megatron está triste... ¡pero la próxima daremos la vuelta! 🤖😢", false);
        }
        await loadHistory();
        showToast(resultado === 'hit' ? '✅ Marcado como acertado' : '❌ Marcado como fallido',
          resultado === 'hit' ? 'success' : 'error');
      } else {
        showToast('Error al marcar resultado', 'error');
      }
    } catch (e) {
      showToast('Error de conexión', 'error');
    }
  };

  function updateAccuracyStats(pctGlobal) {
    var allBets = [];
    $.each(app.history, function (i, entry) { allBets = allBets.concat(entry.apuestas); });

    var decided = allBets.filter(function (b) { return b.resultado !== 'pending'; });
    var hits = decided.filter(function (b) { return b.resultado === 'hit'; }).length;
    var total = allBets.length;
    var pct = pctGlobal !== null && pctGlobal !== undefined ? pctGlobal : 0;

    $('#acc-total').text(total);
    $('#acc-hits').text(hits);
    $('#acc-miss').text(decided.length - hits);
    $('#acc-pct').text(pct + '%');

    var circleLen = 263.89;
    var offset = circleLen - (circleLen * pct / 100);
    $('#accuracy-circle').attr('stroke-dashoffset', offset);
  }

  window.filterHistory = function (f, btn) {
    app.historyFilter = f;
    $('.filter-btn').removeClass('active');
    $(btn).addClass('active');
    renderHistory();
  };

  function renderHistory() {
    var algoLabel = { pd: 'Prog. Dinámica', bf: 'Fuerza Bruta', gr: 'Greedy' };
    if (!app.history.length) {
      $('#history-list').html('<div class="empty-state"><div class="icon">📋</div><p>Aún no tienes recomendaciones guardadas.</p></div>');
      return;
    }

    var html = '';
    $.each(app.history, function (i, entry) {
      var filteredBets = app.historyFilter === 'all'
        ? entry.apuestas
        : entry.apuestas.filter(function (b) { return b.resultado === app.historyFilter; });
      if (!filteredBets.length) return;

      var hits = entry.apuestas.filter(function (b) { return b.resultado === 'hit'; }).length;
      var miss = entry.apuestas.filter(function (b) { return b.resultado === 'miss'; }).length;
      var totalGanancia = parseFloat(entry.ganancia_est || 0);

      var betsHtml = '';
      $.each(filteredBets, function (j, b) {
        var isHit = b.resultado === 'hit';
        var isMiss = b.resultado === 'miss';
        var recTag = b.resultado_sug
          ? '<span style="background:rgba(0,230,118,.12);border:1px solid rgba(0,230,118,.35);color:#00e676;padding:.15rem .55rem;border-radius:4px;font-size:.75rem;font-weight:700;letter-spacing:.5px;white-space:nowrap;">🟢 ' + b.resultado_sug + '</span>'
          : '';
        betsHtml += '<div class="history-match">' +
          '<div style="display:flex;flex-direction:column;gap:.3rem;min-width:0;">' +
          '<span class="history-match-name">' + b.partido + '</span>' +
          recTag +
          '</div>' +
          '<div class="history-match-right">' +
          '<span class="history-amount">$' + b.monto + '</span>' +
          '<div class="mark-btns">' +
          '<button class="mark-btn mark-hit ' + (isHit ? 'marked' : '') + '" ' +
          'onclick="markResult(' + entry.id + ', ' + b.id + ', \'hit\')">✓ Acertó</button>' +
          '<button class="mark-btn mark-miss ' + (isMiss ? 'marked' : '') + '" ' +
          'onclick="markResult(' + entry.id + ', ' + b.id + ', \'miss\')">✗ Falló</button>' +
          '</div>' +
          '</div>' +
          '</div>';
      });

      html += '<div class="history-card">' +
        '<div class="history-card-header">' +
        '<div>' +
        '<span class="badge badge-gold">' + entry.fecha + '</span>' +
        '<span class="badge badge-cyan" style="margin-left:.5rem;">' + (algoLabel[entry.algoritmo] || entry.algoritmo) + '</span>' +
        '</div>' +
        '<div style="font-size:.8rem;color:var(--text-dim)">Capital: <strong style="color:var(--gold);font-family:\'Orbitron\',monospace">$' + entry.capital + '</strong></div>' +
        '</div>' +
        '<div class="history-matches">' + betsHtml + '</div>' +
        '<div class="history-summary-row">' +
        '<span class="history-total">✅ <strong>' + hits + '</strong> acertadas &nbsp; ❌ <strong>' + miss + '</strong> fallidas</span>' +
        '<span class="history-total">Ganancia esp.: <strong style="color:var(--green)">+$' + totalGanancia.toFixed(2) + '</strong></span>' +
        '</div>' +
        '</div>';
    });

    $('#history-list').html(html ||
      '<div class="empty-state"><div class="icon">🔍</div><p>No hay registros con ese filtro.</p></div>');
  }

  // Funciones de Megatron
  function updateBalloonCounter() {
    var balloons = app.megatronBalloons;
    console.log("Actualizando contador de balones:", balloons);
    $('#megatron-ball-count').text(balloons);
    if (balloons > 0) {
      $('#megatron-balloon-counter').show();
    } else {
      $('#megatron-balloon-counter').hide();
    }
    sessionStorage.setItem('megatron_balloons', balloons);
  }

  function showMegatronMessage(msg, showProfileButton = false) {
    var $bubble = $('#megatron-bubble');
    var $msgDiv = $('#megatron-message');
    var $actions = $('#megatron-actions');

    $msgDiv.text(msg);
    if (showProfileButton) {
      $actions.show();
    } else {
      $actions.hide();
    }

    $bubble.removeClass('hidden');
    if (!showProfileButton) {
      setTimeout(function () {
        if (!$bubble.hasClass('hidden')) $bubble.addClass('hidden');
      }, 8000);
    }
  }

  function openProfileModal() {
    var totalHits = 0, totalMiss = 0;
    for (var i = 0; i < app.history.length; i++) {
      for (var j = 0; j < app.history[i].apuestas.length; j++) {
        var res = app.history[i].apuestas[j].resultado;
        if (res === 'hit') totalHits++;
        else if (res === 'miss') totalMiss++;
      }
    }
    var totalDecided = totalHits + totalMiss;
    var percentage = totalDecided === 0 ? 0 : (totalHits / totalDecided) * 100;

    var profileImg = '';
    if (percentage >= 90) profileImg = '/static/imagenes/perfil1.png';
    else if (percentage >= 70) profileImg = '/static/imagenes/perfil2.png';
    else if (percentage >= 50) profileImg = '/static/imagenes/perfil3.png';
    else if (percentage >= 30) profileImg = '/static/imagenes/perfil4.png';
    else profileImg = '/static/imagenes/perfil5.png';

    $('#profile-card-img').attr('src', profileImg);
    $('#profile-modal').addClass('active');
  }

  function closeProfileModal() {
    $('#profile-modal').removeClass('active');
  }

  // Eventos de Megatron
  $('#megatron-widget .megatron-avatar').on('click', function (e) {
    e.stopPropagation();
    var $bubble = $('#megatron-bubble');
    if ($bubble.hasClass('hidden')) {
      if ($('#megatron-actions').is(':visible')) {
        $bubble.removeClass('hidden');
      } else {
        var lastMsg = $('#megatron-message').text();
        if (lastMsg) $bubble.removeClass('hidden');
      }
    } else {
      $bubble.addClass('hidden');
    }
  });

  $(document).on('click', '#btn-show-profile', function (e) {
    e.stopPropagation();
    openProfileModal();
    $('#megatron-bubble').addClass('hidden');
  });

  $(document).on('click', '.modal-overlay, .modal-close', function () {
    closeProfileModal();
  });

  // Inicializar contador de balones
  updateBalloonCounter();

  window.showToast = function (msg, type) {
    type = type || 'info';
    var t = $('#toast');
    t.text(msg).attr('class', 'toast ' + type);
    setTimeout(function () { t.addClass('show'); }, 10);
    setTimeout(function () { t.removeClass('show'); }, 3200);
  };

  $(document).on('keydown', function (e) {
    if (e.key === 'Enter') {
      if ($('#form-login').hasClass('active')) handleLogin();
      if ($('#form-register').hasClass('active')) handleRegister();
    }
  });

});