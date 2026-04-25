// ─────────────────────────────────────────────────────────────────────────────
// SORA MX — Frontend adaptado a FastAPI
// Todas las llamadas van a http://localhost:8000
// ─────────────────────────────────────────────────────────────────────────────

const API = 'http://localhost:8000';

// Helper para llamadas POST a FastAPI (JSON)
async function apiPost(endpoint, body) {
  const res = await fetch(API + endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  return res.json();
}

// Helper para llamadas GET a FastAPI
async function apiGet(endpoint) {
  const res = await fetch(API + endpoint);
  return res.json();
}

$(document).ready(function () {

  /* ─── APP STATE ─────────────────────────────── */
  var app = {
    currentUser: null,
    selectedAlgo: 'pd',
    historyFilter: 'all',
    matches: [],
    history: [],
    lastResult: null
  };

  // Restaurar sesión desde sessionStorage
  var savedUser = sessionStorage.getItem('sora_user');
  if (savedUser) {
    try { app.currentUser = JSON.parse(savedUser); } catch (e) { }
  }

  // Detectar en qué página estamos y ejecutar la lógica correspondiente
  var currentPage = location.pathname.split('/').pop();

  // Si estamos en pantalla1/2/3 sin sesión → redirigir a login
  // ✅ BIEN — usa pathname completo
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

  /* ─── NAVEGACIÓN ─────────────────────────────── */
  window.goTo = function (n) {
    var pages = { 1: '/partidos-page', 2: '/optimizar-page', 3: '/historial-page' };
    if (pages[n]) location.href = pages[n];
  };

  /* ─── LOGIN TABS ─────────────────────────────── */
  window.switchLoginTab = function (tab) {
    $('.tab-btn').removeClass('active');
    $('.login-form').removeClass('active');
    $('#btn-tab-' + tab).addClass('active');
    $('#form-' + tab).addClass('active');
  };

  /* ══════════════════════════════════════════════
     LOGIN — POST /login
  ══════════════════════════════════════════════ */
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

  /* ══════════════════════════════════════════════
     REGISTRO — POST /registro
  ══════════════════════════════════════════════ */
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
    sessionStorage.setItem('sora_user', JSON.stringify(app.currentUser));
    showToast('¡Bienvenido, ' + app.currentUser.nombre + '!', 'success');
    setTimeout(function () { location.href = '/partidos-page'; }, 800);
  }

  window.handleLogout = function () {
    sessionStorage.removeItem('sora_user');
    app.currentUser = null;
    showToast('Sesión cerrada', 'info');
    setTimeout(function () { location.href = '/login'; }, 600);
  };

  /* ══════════════════════════════════════════════
     SCREEN 1 — PARTIDOS — GET /partidos
  ══════════════════════════════════════════════ */
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
    $('#stat-total').text(app.matches.length);
    $('#stat-positivos').text(positivos.length);

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

  /* ══════════════════════════════════════════════
     SCREEN 2 — CALCULAR — POST /calcular + POST /guardar
  ══════════════════════════════════════════════ */
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
        // Guardar automáticamente en MySQL
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
          jornada: 'Jornada 15',
          capital: capital,
          ganancia_est: resp.ganancia_estimada,
          partidos: partidos
        });

        app.lastResult = resp;

        // Siempre se usa Programación Dinámica como algoritmo del sistema
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
            resultado: item.resultado,   // ← resultado recomendado
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
        '<span style="background:rgba(0,230,118,.15);border:1px solid ' +
        'rgba(0,230,118,.4);color:#00e676;padding:.15rem .5rem;' +
        'border-radius:4px;font-weight:700;margin-right:.5rem;">' +
        '🟢 ' + b.resultado + '</span>' +
        'Momio: ' + b.momio + ' · EV: +' +
        (parseFloat(b.ev) * 100).toFixed(1) + '%' +
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

  /* ══════════════════════════════════════════════
     SCREEN 3 — HISTORIAL — GET /historial/{id}
  ══════════════════════════════════════════════ */
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
              monto: p.apuesta,
              ganancia_esperada: 0,
              resultado: p.acerto === 1 ? 'hit' : p.acerto === 0 ? 'miss' : 'pending'
            };
          })
        };
      });
      updateAccuracyStats(data.pct_aciertos);
      renderHistory();
    } catch (e) {
      showToast('Error al cargar historial', 'error');
    }
  }

  // POST /acierto
  window.markResult = async function (sesionId, apuestaId, resultado) {
    try {
      var resp = await apiPost('/acierto', {
        detalle_id: apuestaId,
        acerto: resultado === 'hit'
      });
      if (resp.ok) {
        loadHistory();
        showToast(resultado === 'hit' ? '✅ Marcado como acertado' : '❌ Marcado como fallido',
          resultado === 'hit' ? 'success' : 'error');
      }
    } catch (e) {
      showToast('Error al marcar resultado', 'error');
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
      // ✅ PONER ESTA LÍNEA
      var totalGanancia = parseFloat(entry.ganancia_est || 0);

      var betsHtml = '';
      $.each(filteredBets, function (j, b) {
        var isHit = b.resultado === 'hit';
        var isMiss = b.resultado === 'miss';
        betsHtml += '<div class="history-match">' +
          '<span class="history-match-name">' + b.partido + '</span>' +
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

  /* ─── TOAST ─────────────────────────────────── */
  window.showToast = function (msg, type) {
    type = type || 'info';
    var t = $('#toast');
    t.text(msg).attr('class', 'toast ' + type);
    setTimeout(function () { t.addClass('show'); }, 10);
    setTimeout(function () { t.removeClass('show'); }, 3200);
  };

  /* ─── ENTER en login ─────────────────────────── */
  $(document).on('keydown', function (e) {
    if (e.key === 'Enter') {
      if ($('#form-login').hasClass('active')) handleLogin();
      if ($('#form-register').hasClass('active')) handleRegister();
    }
  });

}); // end document.ready