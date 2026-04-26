from textwrap import dedent

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["ui"])


@router.get("/ui", response_class=HTMLResponse)
def ui_page() -> str:
    return dedent(
        """
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <title>AI Lead Agent</title>
          <style>
            * { box-sizing: border-box; }

            :root {
              --bg: #0f172a;
              --panel: #14213d;
              --panel-2: #172554;
              --border: #334155;
              --text: #e2e8f0;
              --muted: #94a3b8;
              --accent: #3b82f6;
              --accent-hover: #2563eb;
              --secondary: #475569;
              --secondary-hover: #334155;
              --success: #22c55e;
              --success-hover: #16a34a;
              --danger: #ef4444;
              --danger-hover: #dc2626;
              --warning: #f59e0b;
              --cyan: #7dd3fc;
            }

            body {
              margin: 0;
              font-family: Arial, sans-serif;
              background: var(--bg);
              color: var(--text);
            }

            .wrap {
              max-width: 1280px;
              margin: 0 auto;
              padding: 22px;
            }

            .section-title {
              display: flex;
              justify-content: space-between;
              align-items: flex-start;
              gap: 18px;
              flex-wrap: wrap;
              margin-bottom: 18px;
            }

            h1 {
              margin: 0 0 8px 0;
              font-size: 24px;
              line-height: 1.15;
            }

            h2 {
              margin: 0 0 14px 0;
              font-size: 18px;
              line-height: 1.2;
            }

            .muted {
              color: var(--muted);
              font-size: 13px;
              line-height: 1.4;
            }

            .header-actions {
              display: flex;
              align-items: center;
              justify-content: flex-end;
              gap: 12px;
              flex-wrap: wrap;
            }

            .lang-switch {
              display: flex;
              gap: 6px;
              align-items: center;
            }

            .grid {
              display: grid;
              grid-template-columns: 1fr 1fr;
              gap: 16px;
              margin-bottom: 16px;
            }

            .card {
              background: linear-gradient(180deg, rgba(20,33,61,0.95) 0%, rgba(15,23,42,0.98) 100%);
              border: 1px solid var(--border);
              border-radius: 14px;
              padding: 16px;
              box-shadow: 0 6px 24px rgba(0,0,0,0.18);
            }

            .full-width {
              margin-bottom: 16px;
            }

            .section-row {
              display: flex;
              justify-content: space-between;
              align-items: center;
              gap: 12px;
              flex-wrap: wrap;
              margin-bottom: 14px;
            }

            input,
            textarea,
            pre {
              width: 100%;
              border: 1px solid #475569;
              background: rgba(15,23,42,0.8);
              color: var(--text);
              border-radius: 10px;
            }

            input,
            textarea {
              padding: 12px 14px;
              font-size: 14px;
              outline: none;
              transition: border-color 0.15s ease, box-shadow 0.15s ease;
            }

            input:focus,
            textarea:focus {
              border-color: var(--cyan);
              box-shadow: 0 0 0 3px rgba(125, 211, 252, 0.15);
            }

            textarea {
              min-height: 118px;
              resize: vertical;
              margin-top: 10px;
            }

            button {
              border: 0;
              cursor: pointer;
              color: white;
              background: var(--accent);
              border-radius: 10px;
              padding: 10px 14px;
              font-size: 14px;
              font-weight: 700;
              transition: transform 0.04s ease, background 0.15s ease, opacity 0.15s ease;
            }

            button:hover { background: var(--accent-hover); }
            button:active { transform: translateY(1px); }
            button:disabled { opacity: 0.65; cursor: not-allowed; }

            .secondary-btn {
              background: var(--secondary);
            }

            .secondary-btn:hover {
              background: var(--secondary-hover);
            }

            .success-btn {
              background: var(--success);
            }

            .success-btn:hover {
              background: var(--success-hover);
            }

            .danger-btn {
              background: var(--danger);
            }

            .danger-btn:hover {
              background: var(--danger-hover);
            }

            .small-btn,
            .lang-btn {
              width: auto;
              margin: 0;
              padding: 6px 10px;
              font-size: 12px;
              border-radius: 8px;
            }

            .lang-btn.active {
              outline: 2px solid var(--cyan);
              outline-offset: 1px;
            }

            .top-actions {
              display: flex;
              gap: 10px;
              margin-top: 12px;
              margin-bottom: 18px;
              align-items: center;
              flex-wrap: wrap;
            }

            .top-actions button {
              width: auto;
              margin: 0;
              padding: 10px 14px;
            }

            .hint {
              display: block;
              padding-top: 16px;
              font-size: 13px;
              color: var(--muted);
              line-height: 1.4;
            }

            .stats {
              display: grid;
              grid-template-columns: repeat(4, 1fr);
              gap: 14px;
              margin-bottom: 14px;
            }

            .stat {
              border: 1px solid var(--border);
              background: rgba(15,23,42,0.7);
              border-radius: 12px;
              padding: 14px;
            }

            .stat-label {
              color: var(--muted);
              font-size: 12px;
              margin-bottom: 8px;
            }

            .stat-value {
              font-size: 32px;
              font-weight: 700;
              line-height: 1;
            }

            .pill {
              display: inline-block;
              padding: 4px 10px;
              border-radius: 999px;
              font-size: 12px;
              font-weight: 700;
              margin-right: 6px;
              margin-bottom: 6px;
            }

            .pill-neutral { background: #1e293b; color: #e2e8f0; }
            .pill-qualified { background: #166534; color: #dcfce7; }
            .pill-followup { background: #92400e; color: #fef3c7; }
            .pill-pending { background: #9a3412; color: #ffedd5; }
            .pill-progress { background: #1d4ed8; color: #dbeafe; }
            .pill-done { background: #15803d; color: #dcfce7; }

            .summary-box,
            .table-wrap {
              border: 1px solid var(--border);
              background: rgba(15,23,42,0.42);
              border-radius: 12px;
              padding: 12px;
            }

            .summary-box.empty,
            .table-wrap.empty {
              color: var(--muted);
            }

            .summary-row {
              margin: 8px 0;
              line-height: 1.45;
            }

            .summary-key {
              color: var(--muted);
              display: inline-block;
              min-width: 118px;
            }

            table {
              width: 100%;
              border-collapse: collapse;
            }

            th,
            td {
              text-align: left;
              padding: 10px 8px;
              border-bottom: 1px solid rgba(148,163,184,0.18);
              vertical-align: middle;
              font-size: 14px;
            }

            th {
              color: var(--muted);
              font-size: 12px;
              font-weight: 700;
              text-transform: uppercase;
              letter-spacing: 0.04em;
            }

            tr:last-child td {
              border-bottom: 0;
            }

            details {
              margin-top: 14px;
              border: 1px solid var(--border);
              border-radius: 12px;
              background: rgba(15,23,42,0.35);
              overflow: hidden;
            }

            summary {
              list-style: none;
              cursor: pointer;
              padding: 12px 14px;
              font-size: 13px;
              font-weight: 700;
              color: var(--text);
              background: rgba(2,6,23,0.25);
            }

            summary::-webkit-details-marker {
              display: none;
            }

            pre {
              margin: 0;
              padding: 12px;
              overflow: auto;
              white-space: pre-wrap;
              word-break: break-word;
              font-size: 12px;
              color: #cbd5e1;
            }

            .mono {
              font-family: Menlo, Monaco, Consolas, monospace;
              font-size: 12px;
            }

            @media (max-width: 980px) {
              .grid {
                grid-template-columns: 1fr;
              }

              .stats {
                grid-template-columns: 1fr 1fr;
              }
            }

            @media (max-width: 640px) {
              .wrap {
                padding: 14px;
              }

              .stats {
                grid-template-columns: 1fr;
              }

              .section-title {
                margin-bottom: 14px;
              }

              h1 {
                font-size: 22px;
              }
            }
          </style>
        </head>
        <body>
          <div class="wrap">
            <div class="section-title">
              <div>
                <h1 id="appTitle">AI Lead Agent</h1>
                <div class="muted" id="subtitle">Demo-ready MVP for inbound B2B lead intake, qualification, and handoff.</div>
              </div>

              <div class="header-actions">
                <div class="lang-switch">
                  <button id="langRu" class="secondary-btn lang-btn" onclick="setLang('ru')">RU</button>
                  <button id="langEn" class="secondary-btn lang-btn" onclick="setLang('en')">EN</button>
                  <button id="langEs" class="secondary-btn lang-btn" onclick="setLang('es')">ES</button>
                </div>

                <div class="top-actions" style="margin: 0;">
                  <button id="btnLoadDemo" class="success-btn" onclick="seedDemo()">Load demo data</button>
                  <button id="btnResetDemo" class="danger-btn" onclick="resetDemo()">Reset demo</button>
                </div>
              </div>
            </div>

            <div class="grid">
              <div class="card">
                <h2 id="sendTitle">Send message</h2>
                <input id="leadIdInput" placeholder="lead_id — optional for the first message" />
                <textarea id="messageInput" placeholder="Enter inbound message..."></textarea>

                <div class="top-actions">
                  <button id="btnSend" onclick="sendMessage()">Send</button>
                  <button id="btnClear" class="secondary-btn" onclick="clearMessageForm()">Clear</button>
                </div>

                <div class="hint" id="sendHint">After the reply, lead_id will be automatically filled into summary.</div>

                <details>
                  <summary id="rawResponseLabel">Raw response</summary>
                  <pre id="sendResult">Empty.</pre>
                </details>
              </div>

              <div class="card" id="summaryCard">
                <h2 id="summaryTitle">Lead summary</h2>
                <input id="summaryLeadId" placeholder="Enter lead_id" />

                <div class="top-actions">
                  <button id="btnLoadSummary" onclick="loadLeadSummary()">Load summary</button>
                </div>

                <div id="summaryCards" class="summary-box empty">Empty.</div>
                <div id="summaryActions" class="top-actions"></div>

                <details>
                  <summary id="rawSummaryLabel">Raw summary JSON</summary>
                  <pre id="summaryResult">Empty.</pre>
                </details>
              </div>
            </div>

            <div class="card full-width">
              <div class="section-row">
                <h2 id="dashboardTitle">Dashboard overview</h2>
                <button id="btnRefreshDashboard" class="small-btn" onclick="loadDashboard()">Refresh dashboard</button>
              </div>

              <div class="stats">
                <div class="stat">
                  <div class="stat-label" id="statLeadsLabel">Leads total</div>
                  <div class="stat-value" id="statLeads">0</div>
                </div>
                <div class="stat">
                  <div class="stat-label" id="statQualifiedLabel">Qualified</div>
                  <div class="stat-value" id="statQualified">0</div>
                </div>
                <div class="stat">
                  <div class="stat-label" id="statInProgressLabel">Handoffs in progress</div>
                  <div class="stat-value" id="statInProgress">0</div>
                </div>
                <div class="stat">
                  <div class="stat-label" id="statDoneLabel">Handoffs done</div>
                  <div class="stat-value" id="statDone">0</div>
                </div>
              </div>

              <details>
                <summary id="rawDashboardLabel">Raw dashboard JSON</summary>
                <pre id="dashboardResult">Empty.</pre>
              </details>
            </div>

            <div class="grid">
              <div class="card">
                <div class="section-row">
                  <h2 id="recentLeadsTitle">Recent leads</h2>
                  <button id="btnRefreshLeads" class="small-btn" onclick="loadLeads()">Refresh</button>
                </div>

                <div id="leadsTable" class="table-wrap empty">No leads.</div>

                <details>
                  <summary id="rawLeadsLabel">Raw leads JSON</summary>
                  <pre id="leadsRaw">Empty.</pre>
                </details>
              </div>

              <div class="card">
                <div class="section-row">
                  <h2 id="recentHandoffsTitle">Recent handoffs</h2>
                  <button id="btnRefreshHandoffs" class="small-btn" onclick="loadHandoffs()">Refresh</button>
                </div>

                <div id="handoffsTable" class="table-wrap empty">No handoffs.</div>

                <details>
                  <summary id="rawHandoffsLabel">Raw handoffs JSON</summary>
                  <pre id="handoffsRaw">Empty.</pre>
                </details>
              </div>
            </div>
          </div>

          <script>
            const STATE = {
              lang: 'en',
              dashboard: null,
              leads: [],
              handoffs: [],
              summary: null,
              lastSendResponse: null
            };

            const I18N = {
              en: {
                subtitle: 'Demo-ready MVP for inbound B2B lead intake, qualification, and handoff.',
                sendTitle: 'Send message',
                leadIdPlaceholder: 'lead_id — optional for the first message',
                messagePlaceholder: 'Enter inbound message...',
                btnSend: 'Send',
                btnClear: 'Clear',
                sendHint: 'After the reply, lead_id will be automatically filled into summary.',
                rawResponseLabel: 'Raw response',
                empty: 'Empty.',
                summaryTitle: 'Lead summary',
                summaryLeadPlaceholder: 'Enter lead_id',
                btnLoadSummary: 'Load summary',
                rawSummaryLabel: 'Raw summary JSON',
                dashboardTitle: 'Dashboard overview',
                btnRefreshDashboard: 'Refresh dashboard',
                statLeadsLabel: 'Leads total',
                statQualifiedLabel: 'Qualified',
                statInProgressLabel: 'Handoffs in progress',
                statDoneLabel: 'Handoffs done',
                rawDashboardLabel: 'Raw dashboard JSON',
                recentLeadsTitle: 'Recent leads',
                recentHandoffsTitle: 'Recent handoffs',
                btnRefresh: 'Refresh',
                rawLeadsLabel: 'Raw leads JSON',
                rawHandoffsLabel: 'Raw handoffs JSON',
                noLeads: 'No leads.',
                noHandoffs: 'No handoffs.',
                btnLoadDemo: 'Load demo data',
                btnResetDemo: 'Reset demo',
                tableId: 'ID',
                tableCompany: 'Company',
                tableRole: 'Role',
                tableStatus: 'Status',
                tableLeadId: 'Lead ID',
                tableAssigned: 'Assigned',
                tableAction: 'Action',
                btnOpen: 'Open',
                btnOpenLead: 'Open lead',
                btnSetInProgress: 'Set handoff in progress',
                btnSetDone: 'Set handoff done',
                unassigned: 'Unassigned',
                company: 'Company',
                role: 'Role',
                contact: 'Contact',
                useCase: 'Use case',
                assignedTo: 'Assigned to',
                lastSender: 'Last sender',
                lastIntent: 'Last intent',
                lastText: 'Last text',
                noSummary: 'Empty.',
                status_new: 'new',
                status_qualified: 'qualified',
                status_needs_followup: 'needs follow-up',
                status_pending: 'pending',
                status_in_progress: 'in progress',
                status_done: 'done',
                status_unknown: 'unknown'
              },
              ru: {
                subtitle: 'Готовый к демо MVP для входящих B2B-лидов, квалификации и передачи.',
                sendTitle: 'Отправить сообщение',
                leadIdPlaceholder: 'lead_id — необязательно для первого сообщения',
                messagePlaceholder: 'Введите входящее сообщение...',
                btnSend: 'Отправить',
                btnClear: 'Очистить',
                sendHint: 'После ответа lead_id автоматически подставится в summary.',
                rawResponseLabel: 'Raw response',
                empty: 'Пока пусто.',
                summaryTitle: 'Сводка по лиду',
                summaryLeadPlaceholder: 'Введите lead_id',
                btnLoadSummary: 'Загрузить summary',
                rawSummaryLabel: 'Raw summary JSON',
                dashboardTitle: 'Обзор dashboard',
                btnRefreshDashboard: 'Обновить dashboard',
                statLeadsLabel: 'Всего лидов',
                statQualifiedLabel: 'Qualified',
                statInProgressLabel: 'Handoffs в работе',
                statDoneLabel: 'Handoffs завершены',
                rawDashboardLabel: 'Raw dashboard JSON',
                recentLeadsTitle: 'Последние лиды',
                recentHandoffsTitle: 'Последние handoffs',
                btnRefresh: 'Обновить',
                rawLeadsLabel: 'Raw leads JSON',
                rawHandoffsLabel: 'Raw handoffs JSON',
                noLeads: 'Нет лидов.',
                noHandoffs: 'Нет handoff.',
                btnLoadDemo: 'Загрузить демо',
                btnResetDemo: 'Сбросить демо',
                tableId: 'ID',
                tableCompany: 'Компания',
                tableRole: 'Роль',
                tableStatus: 'Статус',
                tableLeadId: 'Lead ID',
                tableAssigned: 'Ответственный',
                tableAction: 'Действие',
                btnOpen: 'Открыть',
                btnOpenLead: 'Открыть lead',
                btnSetInProgress: 'Перевести в in progress',
                btnSetDone: 'Перевести в done',
                unassigned: 'Не назначен',
                company: 'Компания',
                role: 'Роль',
                contact: 'Контакт',
                useCase: 'Use case',
                assignedTo: 'Assigned to',
                lastSender: 'Last sender',
                lastIntent: 'Last intent',
                lastText: 'Last text',
                noSummary: 'Пока пусто.',
                status_new: 'new',
                status_qualified: 'qualified',
                status_needs_followup: 'needs_followup',
                status_pending: 'pending',
                status_in_progress: 'in_progress',
                status_done: 'done',
                status_unknown: 'unknown'
              },
              es: {
                subtitle: 'MVP listo para demo para leads B2B entrantes, calificación y handoff.',
                sendTitle: 'Enviar mensaje',
                leadIdPlaceholder: 'lead_id — opcional para el primer mensaje',
                messagePlaceholder: 'Ingresa el mensaje entrante...',
                btnSend: 'Enviar',
                btnClear: 'Limpiar',
                sendHint: 'Después de la respuesta, el lead_id se completará automáticamente en el summary.',
                rawResponseLabel: 'Respuesta raw',
                empty: 'Vacío.',
                summaryTitle: 'Resumen del lead',
                summaryLeadPlaceholder: 'Ingresa lead_id',
                btnLoadSummary: 'Cargar summary',
                rawSummaryLabel: 'Raw summary JSON',
                dashboardTitle: 'Resumen del dashboard',
                btnRefreshDashboard: 'Actualizar dashboard',
                statLeadsLabel: 'Leads totales',
                statQualifiedLabel: 'Calificados',
                statInProgressLabel: 'Handoffs en progreso',
                statDoneLabel: 'Handoffs completados',
                rawDashboardLabel: 'Raw dashboard JSON',
                recentLeadsTitle: 'Leads recientes',
                recentHandoffsTitle: 'Handoffs recientes',
                btnRefresh: 'Actualizar',
                rawLeadsLabel: 'Raw leads JSON',
                rawHandoffsLabel: 'Raw handoffs JSON',
                noLeads: 'No hay leads.',
                noHandoffs: 'No hay handoffs.',
                btnLoadDemo: 'Cargar demo',
                btnResetDemo: 'Resetear demo',
                tableId: 'ID',
                tableCompany: 'Empresa',
                tableRole: 'Rol',
                tableStatus: 'Estado',
                tableLeadId: 'Lead ID',
                tableAssigned: 'Asignado',
                tableAction: 'Acción',
                btnOpen: 'Abrir',
                btnOpenLead: 'Abrir lead',
                btnSetInProgress: 'Poner handoff en progreso',
                btnSetDone: 'Marcar handoff como done',
                unassigned: 'Sin asignar',
                company: 'Empresa',
                role: 'Rol',
                contact: 'Contacto',
                useCase: 'Caso de uso',
                assignedTo: 'Asignado a',
                lastSender: 'Último remitente',
                lastIntent: 'Último intent',
                lastText: 'Último texto',
                noSummary: 'Vacío.',
                status_new: 'new',
                status_qualified: 'qualified',
                status_needs_followup: 'needs_followup',
                status_pending: 'pending',
                status_in_progress: 'in_progress',
                status_done: 'done',
                status_unknown: 'unknown'
              }
            };

            function t(key) {
              return (I18N[STATE.lang] && I18N[STATE.lang][key]) || (I18N.en && I18N.en[key]) || key;
            }

            function escapeHtml(value) {
              return String(value ?? '')
                .replaceAll('&', '&amp;')
                .replaceAll('<', '&lt;')
                .replaceAll('>', '&gt;')
                .replaceAll('"', '&quot;')
                .replaceAll("'", '&#039;');
            }

            function pretty(value) {
              return JSON.stringify(value, null, 2);
            }

            function getStatusClass(status) {
              const s = String(status || '').toLowerCase();
              if (s === 'qualified') return 'pill-qualified';
              if (s === 'needs_followup' || s === 'needs-followup' || s === 'needs followup') return 'pill-followup';
              if (s === 'pending') return 'pill-pending';
              if (s === 'in_progress' || s === 'in progress') return 'pill-progress';
              if (s === 'done') return 'pill-done';
              return 'pill-neutral';
            }

            function translateStatus(status) {
              const s = String(status || '').toLowerCase().replaceAll('-', '_').replaceAll(' ', '_');
              return t('status_' + s) || status || t('status_unknown');
            }

            async function api(path, options = {}) {
              const response = await fetch(path, {
                headers: { 'Content-Type': 'application/json' },
                ...options
              });

              const text = await response.text();
              let data = null;

              try {
                data = text ? JSON.parse(text) : null;
              } catch {
                data = text;
              }

              if (!response.ok) {
                throw new Error(typeof data === 'string' ? data : pretty(data));
              }

              return data;
            }

            function setText(id, value) {
              const el = document.getElementById(id);
              if (el) el.textContent = value;
            }

            function setPlaceholder(id, value) {
              const el = document.getElementById(id);
              if (el) el.placeholder = value;
            }

            function setLang(lang) {
              if (!I18N[lang]) return;

              STATE.lang = lang;
              localStorage.setItem('ui_lang', lang);

              setText('subtitle', t('subtitle'));
              setText('sendTitle', t('sendTitle'));
              setPlaceholder('leadIdInput', t('leadIdPlaceholder'));
              setPlaceholder('messageInput', t('messagePlaceholder'));
              setText('btnSend', t('btnSend'));
              setText('btnClear', t('btnClear'));
              setText('sendHint', t('sendHint'));
              setText('rawResponseLabel', t('rawResponseLabel'));

              setText('summaryTitle', t('summaryTitle'));
              setPlaceholder('summaryLeadId', t('summaryLeadPlaceholder'));
              setText('btnLoadSummary', t('btnLoadSummary'));
              setText('rawSummaryLabel', t('rawSummaryLabel'));

              setText('dashboardTitle', t('dashboardTitle'));
              setText('btnRefreshDashboard', t('btnRefreshDashboard'));
              setText('statLeadsLabel', t('statLeadsLabel'));
              setText('statQualifiedLabel', t('statQualifiedLabel'));
              setText('statInProgressLabel', t('statInProgressLabel'));
              setText('statDoneLabel', t('statDoneLabel'));
              setText('rawDashboardLabel', t('rawDashboardLabel'));

              setText('recentLeadsTitle', t('recentLeadsTitle'));
              setText('recentHandoffsTitle', t('recentHandoffsTitle'));
              setText('btnRefreshLeads', t('btnRefresh'));
              setText('btnRefreshHandoffs', t('btnRefresh'));
              setText('rawLeadsLabel', t('rawLeadsLabel'));
              setText('rawHandoffsLabel', t('rawHandoffsLabel'));
              setText('btnLoadDemo', t('btnLoadDemo'));
              setText('btnResetDemo', t('btnResetDemo'));

              document.getElementById('langRu')?.classList.toggle('active', lang === 'ru');
              document.getElementById('langEn')?.classList.toggle('active', lang === 'en');
              document.getElementById('langEs')?.classList.toggle('active', lang === 'es');

              if (!STATE.lastSendResponse) {
                document.getElementById('sendResult').textContent = t('empty');
              }

              if (!STATE.summary) {
                document.getElementById('summaryCards').textContent = t('noSummary');
                document.getElementById('summaryCards').className = 'summary-box empty';
                document.getElementById('summaryResult').textContent = t('empty');
              }

              if (!STATE.dashboard) {
                document.getElementById('dashboardResult').textContent = t('empty');
              }

              renderLeads(STATE.leads);
              renderHandoffs(STATE.handoffs);
              renderDashboard(STATE.dashboard);
              renderSummary(STATE.summary);
            }

            function renderDashboard(data) {
              STATE.dashboard = data;

              const total = data?.leads_total ?? data?.total_leads ?? data?.total ?? 0;
              const qualified = data?.qualified ?? data?.qualified_count ?? 0;
              const inProgress = data?.handoffs_in_progress ?? data?.in_progress ?? 0;
              const done = data?.handoffs_done ?? data?.done ?? 0;

              document.getElementById('statLeads').textContent = total;
              document.getElementById('statQualified').textContent = qualified;
              document.getElementById('statInProgress').textContent = inProgress;
              document.getElementById('statDone').textContent = done;

              document.getElementById('dashboardResult').textContent = data ? pretty(data) : t('empty');
            }

            function renderSummary(data) {
              STATE.summary = data;

              const box = document.getElementById('summaryCards');
              const actions = document.getElementById('summaryActions');
              const raw = document.getElementById('summaryResult');

              if (!data) {
                box.className = 'summary-box empty';
                box.textContent = t('noSummary');
                actions.innerHTML = '';
                raw.textContent = t('empty');
                return;
              }

              const leadId = data.lead_id ?? data.id ?? '';
              const leadStatus = data.status ?? data.lead_status ?? '';
              const handoffStatus = data.handoff_status ?? data.handoff?.status ?? '';
              const handoffId = data.handoff_id ?? data.handoff?.id ?? null;
              const company = data.company ?? '—';
              const role = data.role ?? '—';
              const contact = data.contact ?? '—';
              const useCase = data.use_case ?? data.usecase ?? '—';
              const assignedTo = data.assigned_to ?? data.assignee ?? data.assigned ?? '—';
              const lastSender = data.last_sender ?? '—';
              const lastIntent = data.last_intent ?? '—';
              const lastText = data.last_text ?? '—';

              const pills = [
                leadId ? `<span class="pill pill-neutral">lead_id: ${escapeHtml(leadId)}</span>` : '',
                leadStatus ? `<span class="pill ${getStatusClass(leadStatus)}">${escapeHtml(translateStatus(leadStatus))}</span>` : '',
                handoffStatus ? `<span class="pill ${getStatusClass(handoffStatus)}">${escapeHtml(translateStatus(handoffStatus))}</span>` : ''
              ].join('');

              box.className = 'summary-box';
              box.innerHTML = `
                <div>${pills}</div>
                <div class="summary-row"><span class="summary-key">${escapeHtml(t('company'))}:</span> ${escapeHtml(company)}</div>
                <div class="summary-row"><span class="summary-key">${escapeHtml(t('role'))}:</span> ${escapeHtml(role)}</div>
                <div class="summary-row"><span class="summary-key">${escapeHtml(t('contact'))}:</span> ${escapeHtml(contact)}</div>
                <div class="summary-row"><span class="summary-key">${escapeHtml(t('useCase'))}:</span> ${escapeHtml(useCase)}</div>
                <div class="summary-row"><span class="summary-key">${escapeHtml(t('assignedTo'))}:</span> ${escapeHtml(assignedTo)}</div>
                <div class="summary-row"><span class="summary-key">${escapeHtml(t('lastSender'))}:</span> ${escapeHtml(lastSender)}</div>
                <div class="summary-row"><span class="summary-key">${escapeHtml(t('lastIntent'))}:</span> ${escapeHtml(lastIntent)}</div>
                <div class="summary-row"><span class="summary-key">${escapeHtml(t('lastText'))}:</span> ${escapeHtml(lastText)}</div>
              `;

              const buttons = [];
              if (handoffId && handoffStatus !== 'in_progress') {
                buttons.push(`<button class="secondary-btn small-btn" onclick="setHandoffStatus(${handoffId}, 'in_progress')">${escapeHtml(t('btnSetInProgress'))}</button>`);
              }
              if (handoffId && handoffStatus !== 'done') {
                buttons.push(`<button class="success-btn small-btn" onclick="setHandoffStatus(${handoffId}, 'done')">${escapeHtml(t('btnSetDone'))}</button>`);
              }

              actions.innerHTML = buttons.join('');
              raw.textContent = pretty(data);
            }

            function renderLeads(data) {
              STATE.leads = Array.isArray(data) ? data : (Array.isArray(data?.items) ? data.items : []);

              const wrap = document.getElementById('leadsTable');
              const raw = document.getElementById('leadsRaw');

              raw.textContent = STATE.leads.length ? pretty(STATE.leads) : t('empty');

              if (!STATE.leads.length) {
                wrap.className = 'table-wrap empty';
                wrap.textContent = t('noLeads');
                return;
              }

              wrap.className = 'table-wrap';
              wrap.innerHTML = `
                <table>
                  <thead>
                    <tr>
                      <th>${escapeHtml(t('tableId'))}</th>
                      <th>${escapeHtml(t('tableCompany'))}</th>
                      <th>${escapeHtml(t('tableRole'))}</th>
                      <th>${escapeHtml(t('tableStatus'))}</th>
                      <th>${escapeHtml(t('tableAction'))}</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${STATE.leads.map((lead) => {
                      const id = lead.id ?? lead.lead_id ?? '';
                      const company = lead.company ?? '—';
                      const role = lead.role ?? '—';
                      const status = lead.status ?? lead.lead_status ?? '';
                      return `
                        <tr>
                          <td>${escapeHtml(id)}</td>
                          <td>${escapeHtml(company)}</td>
                          <td>${escapeHtml(role)}</td>
                          <td><span class="pill ${getStatusClass(status)}">${escapeHtml(translateStatus(status))}</span></td>
                          <td><button class="small-btn" onclick="openLead(${id})">${escapeHtml(t('btnOpen'))}</button></td>
                        </tr>
                      `;
                    }).join('')}
                  </tbody>
                </table>
              `;
            }

            function renderHandoffs(data) {
              STATE.handoffs = Array.isArray(data) ? data : (Array.isArray(data?.items) ? data.items : []);

              const wrap = document.getElementById('handoffsTable');
              const raw = document.getElementById('handoffsRaw');

              raw.textContent = STATE.handoffs.length ? pretty(STATE.handoffs) : t('empty');

              if (!STATE.handoffs.length) {
                wrap.className = 'table-wrap empty';
                wrap.textContent = t('noHandoffs');
                return;
              }

              wrap.className = 'table-wrap';
              wrap.innerHTML = `
                <table>
                  <thead>
                    <tr>
                      <th>${escapeHtml(t('tableId'))}</th>
                      <th>${escapeHtml(t('tableLeadId'))}</th>
                      <th>${escapeHtml(t('tableAssigned'))}</th>
                      <th>${escapeHtml(t('tableStatus'))}</th>
                      <th>${escapeHtml(t('tableAction'))}</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${STATE.handoffs.map((handoff) => {
                      const id = handoff.id ?? '';
                      const leadId = handoff.lead_id ?? '';
                      const assigned = handoff.assigned_to ?? handoff.assignee ?? t('unassigned');
                      const status = handoff.status ?? '';
                      return `
                        <tr>
                          <td>${escapeHtml(id)}</td>
                          <td>${escapeHtml(leadId)}</td>
                          <td>${escapeHtml(assigned)}</td>
                          <td><span class="pill ${getStatusClass(status)}">${escapeHtml(translateStatus(status))}</span></td>
                          <td><button class="small-btn" onclick="openLead(${leadId})">${escapeHtml(t('btnOpenLead'))}</button></td>
                        </tr>
                      `;
                    }).join('')}
                  </tbody>
                </table>
              `;
            }

            async function sendMessage() {
              const leadIdValue = document.getElementById('leadIdInput').value.trim();
              const message = document.getElementById('messageInput').value.trim();

              if (!message) return;

              try {
                const payload = {
                  lead_id: leadIdValue ? Number(leadIdValue) : null,
                  message
                };

                const data = await api('/chat/message', {
                  method: 'POST',
                  body: JSON.stringify(payload)
                });

                STATE.lastSendResponse = data;
                document.getElementById('sendResult').textContent = pretty(data);

                const newLeadId = data?.lead_id ?? data?.id ?? payload.lead_id;
                if (newLeadId) {
                  document.getElementById('leadIdInput').value = String(newLeadId);
                  document.getElementById('summaryLeadId').value = String(newLeadId);
                  await loadLeadSummary();
                }

                await Promise.all([loadDashboard(), loadLeads(), loadHandoffs()]);
              } catch (error) {
                document.getElementById('sendResult').textContent = String(error);
              }
            }

            function clearMessageForm() {
              document.getElementById('leadIdInput').value = '';
              document.getElementById('messageInput').value = '';
            }

            async function loadLeadSummary() {
              const leadId = document.getElementById('summaryLeadId').value.trim();
              if (!leadId) return;

              try {
                const data = await api(`/leads/${leadId}/summary`);
                renderSummary(data);
              } catch (error) {
                document.getElementById('summaryResult').textContent = String(error);
              }
            }

            async function loadDashboard() {
              try {
                const data = await api('/dashboard/overview');
                renderDashboard(data);
              } catch (error) {
                document.getElementById('dashboardResult').textContent = String(error);
              }
            }

            async function loadLeads() {
              try {
                const data = await api('/leads');
                renderLeads(data);
              } catch (error) {
                document.getElementById('leadsRaw').textContent = String(error);
              }
            }

            async function loadHandoffs() {
              try {
                const data = await api('/handoffs');
                renderHandoffs(data);
              } catch (error) {
                document.getElementById('handoffsRaw').textContent = String(error);
              }
            }

            async function setHandoffStatus(handoffId, status) {
              try {
                await api(`/handoffs/${handoffId}`, {
                  method: 'PATCH',
                  body: JSON.stringify({ status })
                });

                await Promise.all([loadHandoffs(), loadDashboard()]);
                const leadId = document.getElementById('summaryLeadId').value.trim();
                if (leadId) {
                  await loadLeadSummary();
                }
              } catch (error) {
                document.getElementById('summaryResult').textContent = String(error);
              }
            }

            async function seedDemo() {
              try {
                await api('/demo/seed', { method: 'POST', body: JSON.stringify({}) });
                await refreshAll();
              } catch (error) {
                document.getElementById('sendResult').textContent = String(error);
              }
            }

            async function resetDemo() {
              try {
                await api('/demo/reset', { method: 'POST', body: JSON.stringify({}) });

                STATE.summary = null;
                STATE.lastSendResponse = null;
                document.getElementById('leadIdInput').value = '';
                document.getElementById('messageInput').value = '';
                document.getElementById('summaryLeadId').value = '';
                document.getElementById('sendResult').textContent = t('empty');
                document.getElementById('summaryResult').textContent = t('empty');
                document.getElementById('dashboardResult').textContent = t('empty');
                document.getElementById('leadsRaw').textContent = t('empty');
                document.getElementById('handoffsRaw').textContent = t('empty');

                renderSummary(null);
                renderDashboard(null);
                renderLeads([]);
                renderHandoffs([]);
                await refreshAll();
              } catch (error) {
                document.getElementById('sendResult').textContent = String(error);
              }
            }

            function openLead(leadId) {
              document.getElementById('summaryLeadId').value = String(leadId);
              document.getElementById('leadIdInput').value = String(leadId);
              loadLeadSummary();
            }

            async function refreshAll() {
              await Promise.all([loadDashboard(), loadLeads(), loadHandoffs()]);
            }

            document.addEventListener('DOMContentLoaded', async () => {
              setLang(localStorage.getItem('ui_lang') || 'en');
              document.getElementById('sendResult').textContent = t('empty');
              document.getElementById('summaryResult').textContent = t('empty');
              document.getElementById('dashboardResult').textContent = t('empty');
              document.getElementById('leadsRaw').textContent = t('empty');
              document.getElementById('handoffsRaw').textContent = t('empty');
              renderSummary(null);
              renderDashboard(null);
              renderLeads([]);
              renderHandoffs([]);
              await refreshAll();
            });
          </script>
        </body>
        </html>
        """
    )
