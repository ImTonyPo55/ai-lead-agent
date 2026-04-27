from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


def ui_page() -> str:
    return """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Lead Agent UI</title>
  <style>
    :root {
      --bg: #081225;
      --panel: #0d1b34;
      --panel-2: #102141;
      --border: #2c4f87;
      --text: #eef4ff;
      --muted: #a9b9d4;
      --blue: #2f8cff;
      --blue-2: #4aa3ff;
      --green: #39d353;
      --red: #ff5d5d;
      --orange: #ff9f43;
      --gray: #8fa4c5;
      --shadow: 0 18px 44px rgba(0, 0, 0, 0.24);
      --radius: 18px;
    }

    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; }
    body {
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at top, rgba(59,130,246,0.16), transparent 28%),
        linear-gradient(180deg, #07111f 0%, #081225 100%);
      color: var(--text);
      min-height: 100vh;
    }

    .wrap {
      max-width: 1240px;
      margin: 0 auto;
      padding: 24px;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 16px;
      margin-bottom: 18px;
    }

    .title h1 {
      margin: 0 0 6px 0;
      font-size: 38px;
      line-height: 1.05;
      letter-spacing: -0.02em;
    }

    .title p {
      margin: 0;
      color: var(--muted);
      font-size: 15px;
    }

    .controls {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    .lang-switch {
      display: inline-flex;
      gap: 6px;
      padding: 4px;
      border-radius: 999px;
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.08);
    }

    .lang-btn,
    button {
      appearance: none;
      border: 0;
      cursor: pointer;
      color: white;
      font-weight: 700;
      transition: 0.18s ease;
    }

    .lang-btn {
      min-width: 42px;
      height: 34px;
      padding: 0 10px;
      border-radius: 999px;
      background: transparent;
      color: var(--muted);
      border: 1px solid transparent;
    }

    .lang-btn.active {
      background: var(--blue);
      color: #fff;
      border-color: rgba(255,255,255,0.16);
      box-shadow: 0 6px 18px rgba(47,140,255,0.32);
    }

    .btn {
      min-height: 40px;
      padding: 10px 14px;
      border-radius: 12px;
      font-size: 14px;
      box-shadow: var(--shadow);
    }

    .btn-blue { background: linear-gradient(180deg, var(--blue-2), var(--blue)); }
    .btn-blue:hover { transform: translateY(-1px); }
    .btn-green { background: linear-gradient(180deg, #46e061, #2ec84a); }
    .btn-red { background: linear-gradient(180deg, #ff7474, #ff4b4b); }
    .btn-gray { background: linear-gradient(180deg, #c6d2e3, #a8b9d2); color: #18304f; }
    .btn-ghost {
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.1);
      color: var(--text);
      box-shadow: none;
    }

    .grid-2 {
      display: grid;
      grid-template-columns: 1.1fr 1fr;
      gap: 18px;
      margin-bottom: 18px;
    }

    .grid-4 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
    }

    .grid-bottom {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
      margin-top: 18px;
    }

    .card {
      background: linear-gradient(180deg, rgba(16,33,65,0.96), rgba(11,24,48,0.96));
      border: 1px solid rgba(95,132,194,0.36);
      border-radius: var(--radius);
      padding: 18px;
      box-shadow: var(--shadow);
    }

    .card h2 {
      margin: 0 0 14px 0;
      font-size: 28px;
      line-height: 1.05;
      letter-spacing: -0.02em;
    }

    .section-title {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      margin-bottom: 14px;
    }

    .section-title h3 {
      margin: 0;
      font-size: 18px;
      line-height: 1.2;
    }

    label {
      display: block;
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 6px;
    }

    input, textarea, pre {
      width: 100%;
      background: rgba(6, 17, 33, 0.46);
      border: 1px solid rgba(115, 148, 204, 0.32);
      color: var(--text);
      border-radius: 12px;
      outline: none;
    }

    input, textarea {
      padding: 12px 14px;
      font-size: 14px;
    }

    textarea {
      min-height: 118px;
      resize: vertical;
      font-family: inherit;
      line-height: 1.45;
    }

    .actions {
      display: flex;
      gap: 10px;
      margin-top: 12px;
      margin-bottom: 14px;
      flex-wrap: wrap;
    }

    .hint {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
      margin-top: 6px;
      margin-bottom: 12px;
    }

    .raw-toggle {
      margin-top: 12px;
    }

    details {
      border: 1px solid rgba(115, 148, 204, 0.28);
      border-radius: 12px;
      background: rgba(6, 17, 33, 0.32);
      overflow: hidden;
    }

    summary {
      list-style: none;
      cursor: pointer;
      padding: 12px 14px;
      font-size: 13px;
      font-weight: 700;
      color: var(--text);
      border-bottom: 1px solid transparent;
    }

    summary::-webkit-details-marker { display: none; }
    details[open] summary {
      border-bottom-color: rgba(115, 148, 204, 0.2);
      background: rgba(255,255,255,0.03);
    }

    pre {
      margin: 0;
      padding: 14px;
      overflow: auto;
      white-space: pre-wrap;
      word-break: break-word;
      font-size: 12px;
      color: #d7e5ff;
      border: 0;
      border-radius: 0;
    }

    .summary-box {
      display: grid;
      gap: 10px;
    }

    .badges {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 4px;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 12px;
      font-weight: 800;
      line-height: 1;
      white-space: nowrap;
    }

    .badge-id { background: rgba(255,255,255,0.08); color: #fff; }
    .badge-green { background: rgba(57,211,83,0.2); color: #9effad; border: 1px solid rgba(57,211,83,0.34); }
    .badge-orange { background: rgba(255,159,67,0.18); color: #ffd39f; border: 1px solid rgba(255,159,67,0.34); }
    .badge-gray { background: rgba(143,164,197,0.16); color: #d1def2; border: 1px solid rgba(143,164,197,0.28); }
    .badge-blue { background: rgba(47,140,255,0.16); color: #bdddff; border: 1px solid rgba(47,140,255,0.32); }

    .kv {
      display: grid;
      grid-template-columns: 180px 1fr;
      gap: 10px;
      align-items: start;
      font-size: 14px;
      line-height: 1.45;
    }

    .kv .k { color: var(--muted); }
    .kv .v { color: var(--text); font-weight: 600; }

    .summary-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 4px;
    }

    .metric {
      background: rgba(7, 18, 36, 0.44);
      border: 1px solid rgba(115,148,204,0.24);
      border-radius: 14px;
      padding: 14px;
    }

    .metric .label {
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 10px;
    }

    .metric .value {
      font-size: 34px;
      line-height: 1;
      font-weight: 800;
      letter-spacing: -0.03em;
    }

    .list {
      display: grid;
      gap: 10px;
    }

    .list-item {
      background: rgba(7,18,36,0.42);
      border: 1px solid rgba(115,148,204,0.24);
      border-radius: 14px;
      padding: 14px;
      display: grid;
      gap: 8px;
    }

    .list-top {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }

    .list-title {
      font-weight: 800;
      font-size: 15px;
    }

    .list-sub {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
    }

    .list-actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .footer {
      margin-top: 18px;
      color: var(--muted);
      font-size: 13px;
      display: flex;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
    }

    .footer-links {
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
    }

    .footer a {
      color: #bdddff;
      text-decoration: none;
    }

    .footer a:hover {
      text-decoration: underline;
    }

    .toast-wrap {
      position: fixed;
      right: 18px;
      bottom: 18px;
      display: grid;
      gap: 10px;
      z-index: 9999;
      max-width: 360px;
    }

    .toast {
      background: rgba(8, 18, 37, 0.96);
      border: 1px solid rgba(115,148,204,0.28);
      color: #fff;
      border-radius: 14px;
      padding: 12px 14px;
      box-shadow: var(--shadow);
      font-size: 13px;
      line-height: 1.45;
    }

    .toast.success { border-color: rgba(57,211,83,0.35); }
    .toast.error { border-color: rgba(255,93,93,0.35); }

    @media (max-width: 1080px) {
      .grid-2, .grid-bottom { grid-template-columns: 1fr; }
      .grid-4 { grid-template-columns: 1fr 1fr; }
      .kv { grid-template-columns: 1fr; gap: 4px; }
    }

    @media (max-width: 720px) {
      .wrap { padding: 14px; }
      .title h1 { font-size: 28px; }
      .grid-4 { grid-template-columns: 1fr; }
      .controls { justify-content: flex-start; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <div class="title">
        <h1 id="pageTitle">ИИ-Агент для лидов</h1>
        <p id="pageSubtitle">Готовый к демо MVP для входящих B2B-лидов, квалификации и передачи.</p>
      </div>

      <div class="controls">
        <div class="lang-switch">
          <button class="lang-btn" data-lang="ru">RU</button>
          <button class="lang-btn" data-lang="en">EN</button>
          <button class="lang-btn" data-lang="es">ES</button>
        </div>

        <button id="loadDemoBtn" class="btn btn-green">Загрузить демо</button>
        <button id="resetDemoBtn" class="btn btn-red">Сбросить демо</button>
      </div>
    </div>

    <div class="grid-2">
      <div class="card">
        <div class="section-title">
          <h3 id="sendSectionTitle">Отправить сообщение</h3>
        </div>

        <input id="leadIdInput" placeholder="lead_id — необязательно для первого сообщения" />
        <div style="height: 10px;"></div>
        <textarea id="messageInput" placeholder="Введите входящее сообщение..."></textarea>

        <div class="actions">
          <button id="sendBtn" class="btn btn-blue">Отправить</button>
          <button id="clearBtn" class="btn btn-gray">Очистить</button>
        </div>

        <div id="sendHint" class="hint">
          После ответа lead_id автоматически подставится в сводку.
        </div>

        <div class="raw-toggle">
          <details>
            <summary id="rawResponseSummary">Сырой ответ</summary>
            <pre id="sendResult">(пусто)</pre>
          </details>
        </div>
      </div>

      <div class="card">
        <div class="section-title">
          <h3 id="summarySectionTitle">Сводка по лиду</h3>
        </div>

        <input id="summaryLeadIdInput" placeholder="Введите lead_id" />
        <div style="height: 10px;"></div>
        <button id="loadSummaryBtn" class="btn btn-blue">Загрузить сводку</button>

        <div style="height: 14px;"></div>

        <div class="summary-box" id="summaryBox">
          <div id="summaryEmpty" class="hint">Пока пусто.</div>
        </div>

        <div class="raw-toggle">
          <details>
            <summary id="rawSummarySummary">Сырой JSON сводки</summary>
            <pre id="summaryResult">(пусто)</pre>
          </details>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="section-title">
        <h3 id="dashboardSectionTitle">Обзор панели</h3>
        <button id="refreshDashboardBtn" class="btn btn-blue">Обновить панель</button>
      </div>

      <div class="grid-4">
        <div class="metric">
          <div class="label" id="metricLeadsLabel">Всего лидов</div>
          <div id="metricLeads" class="value">0</div>
        </div>
        <div class="metric">
          <div class="label" id="metricQualifiedLabel">Квалифицировано</div>
          <div id="metricQualified" class="value">0</div>
        </div>
        <div class="metric">
          <div class="label" id="metricInProgressLabel">Передачи в работе</div>
          <div id="metricInProgress" class="value">0</div>
        </div>
        <div class="metric">
          <div class="label" id="metricDoneLabel">Передачи завершены</div>
          <div id="metricDone" class="value">0</div>
        </div>
      </div>

      <div style="margin-top: 14px;">
        <details>
          <summary id="rawDashboardSummary">Сырой JSON панели</summary>
          <pre id="dashboardResult">(пусто)</pre>
        </details>
      </div>
    </div>

    <div class="grid-bottom">
      <div class="card">
        <div class="section-title">
          <h3 id="leadsSectionTitle">Последние лиды</h3>
          <button id="refreshLeadsBtn" class="btn btn-blue">Обновить</button>
        </div>

        <div id="leadsList" class="list"></div>

        <div style="margin-top: 14px;">
          <details>
            <summary id="rawLeadsSummary">Сырой JSON лидов</summary>
            <pre id="leadsRaw">(пусто)</pre>
          </details>
        </div>
      </div>

      <div class="card">
        <div class="section-title">
          <h3 id="handoffsSectionTitle">Последние передачи</h3>
          <button id="refreshHandoffsBtn" class="btn btn-blue">Обновить</button>
        </div>

        <div id="handoffsList" class="list"></div>

        <div style="margin-top: 14px;">
          <details>
            <summary id="rawHandoffsSummary">Сырой JSON передач</summary>
            <pre id="handoffsRaw">(пусто)</pre>
          </details>
        </div>
      </div>
    </div>

    <div class="footer">
      <div id="footerText">Публичный демо-MVP задеплоен на Render.</div>
      <div class="footer-links">
        <a href="/ui" target="_blank">UI</a>
        <a href="/docs" target="_blank">Docs</a>
        <a href="/health" target="_blank">Health</a>
        <a href="https://github.com/" target="_blank" rel="noreferrer">GitHub</a>
      </div>
    </div>
  </div>

  <div id="toastWrap" class="toast-wrap"></div>

  <script>
    const i18n = {
      ru: {
        pageTitle: 'ИИ-Агент для лидов',
        pageSubtitle: 'Готовый к демо MVP для входящих B2B-лидов, квалификации и передачи.',
        sendSectionTitle: 'Отправить сообщение',
        sendBtn: 'Отправить',
        clearBtn: 'Очистить',
        sendHint: 'После ответа lead_id автоматически подставится в сводку.',
        rawResponseSummary: 'Сырой ответ',
        summarySectionTitle: 'Сводка по лиду',
        loadSummaryBtn: 'Загрузить сводку',
        rawSummarySummary: 'Сырой JSON сводки',
        dashboardSectionTitle: 'Обзор панели',
        refreshDashboardBtn: 'Обновить панель',
        metricLeadsLabel: 'Всего лидов',
        metricQualifiedLabel: 'Квалифицировано',
        metricInProgressLabel: 'Передачи в работе',
        metricDoneLabel: 'Передачи завершены',
        rawDashboardSummary: 'Сырой JSON панели',
        leadsSectionTitle: 'Последние лиды',
        refreshLeadsBtn: 'Обновить',
        rawLeadsSummary: 'Сырой JSON лидов',
        handoffsSectionTitle: 'Последние передачи',
        refreshHandoffsBtn: 'Обновить',
        rawHandoffsSummary: 'Сырой JSON передач',
        loadDemoBtn: 'Загрузить демо',
        resetDemoBtn: 'Сбросить демо',
        footerText: 'Публичный демо-MVP задеплоен на Render.',
        leadIdPlaceholder: 'lead_id — необязательно для первого сообщения',
        summaryLeadIdPlaceholder: 'Введите lead_id',
        messagePlaceholder: 'Введите входящее сообщение...',
        empty: '(пусто)',
        noSummary: 'Пока пусто.',
        noLeads: 'Нет лидов.',
        noHandoffs: 'Нет передач.',
        company: 'Компания',
        role: 'Роль',
        contact: 'Контакт',
        useCase: 'Сценарий использования',
        assignedTo: 'Назначен',
        lastSender: 'Последний отправитель',
        lastIntent: 'Последнее намерение',
        lastText: 'Последний текст',
        notAssigned: 'Не назначен',
        status_new: 'новый',
        status_qualified: 'квалифицирован',
        status_needs_followup: 'требует продолжения',
        status_pending: 'готов к передаче',
        status_in_progress: 'в работе',
        status_done: 'завершено',
        status_unknown: 'неизвестно',
        moveToInProgress: 'Перевести в работу',
        markDone: 'Отметить как завершённую',
        open: 'Открыть',
        toastDemoLoaded: 'Демо-данные загружены.',
        toastDemoReset: 'Демо-данные сброшены.',
        toastMessageSent: 'Сообщение обработано.',
        toastSummaryLoaded: 'Сводка по лиду загружена.',
        toastDashboardRefreshed: 'Панель обновлена.',
        toastLeadsRefreshed: 'Лиды обновлены.',
        toastHandoffsRefreshed: 'Передачи обновлены.',
        toastHandoffUpdated: 'Статус передачи обновлён.',
        toastError: 'Что-то пошло не так.',
        polishedAssistantReply: 'Спасибо. Ключевые данные извлечены, лид квалифицирован и готов к передаче в работу.',
      },
      en: {
        pageTitle: 'AI Lead Agent',
        pageSubtitle: 'Demo-ready MVP for inbound B2B lead intake, qualification, and handoff.',
        sendSectionTitle: 'Send message',
        sendBtn: 'Send',
        clearBtn: 'Clear',
        sendHint: 'After the reply, lead_id will be automatically filled into summary.',
        rawResponseSummary: 'Raw response',
        summarySectionTitle: 'Lead summary',
        loadSummaryBtn: 'Load summary',
        rawSummarySummary: 'Raw summary JSON',
        dashboardSectionTitle: 'Dashboard overview',
        refreshDashboardBtn: 'Refresh dashboard',
        metricLeadsLabel: 'Leads total',
        metricQualifiedLabel: 'Qualified',
        metricInProgressLabel: 'Handoffs in progress',
        metricDoneLabel: 'Handoffs done',
        rawDashboardSummary: 'Raw dashboard JSON',
        leadsSectionTitle: 'Recent leads',
        refreshLeadsBtn: 'Refresh',
        rawLeadsSummary: 'Raw leads JSON',
        handoffsSectionTitle: 'Recent handoffs',
        refreshHandoffsBtn: 'Refresh',
        rawHandoffsSummary: 'Raw handoffs JSON',
        loadDemoBtn: 'Load demo data',
        resetDemoBtn: 'Reset demo',
        footerText: 'Public demo MVP deployed on Render.',
        leadIdPlaceholder: 'lead_id — optional for the first message',
        summaryLeadIdPlaceholder: 'Enter lead_id',
        messagePlaceholder: 'Enter inbound message...',
        empty: '(empty)',
        noSummary: 'Empty.',
        noLeads: 'No leads.',
        noHandoffs: 'No handoffs.',
        company: 'Company',
        role: 'Role',
        contact: 'Contact',
        useCase: 'Use case',
        assignedTo: 'Assigned to',
        lastSender: 'Last sender',
        lastIntent: 'Last intent',
        lastText: 'Last text',
        notAssigned: 'Unassigned',
        status_new: 'new',
        status_qualified: 'qualified',
        status_needs_followup: 'needs follow-up',
        status_pending: 'ready for handoff',
        status_in_progress: 'in progress',
        status_done: 'done',
        status_unknown: 'unknown',
        moveToInProgress: 'Set handoff in progress',
        markDone: 'Set handoff done',
        open: 'Open',
        toastDemoLoaded: 'Demo data loaded.',
        toastDemoReset: 'Demo data reset.',
        toastMessageSent: 'Message processed.',
        toastSummaryLoaded: 'Lead summary loaded.',
        toastDashboardRefreshed: 'Dashboard refreshed.',
        toastLeadsRefreshed: 'Leads refreshed.',
        toastHandoffsRefreshed: 'Handoffs refreshed.',
        toastHandoffUpdated: 'Handoff updated.',
        toastError: 'Something went wrong.',
        polishedAssistantReply: 'Thanks. Key data was extracted, the lead is qualified and ready for handoff.',
      },
      es: {
        pageTitle: 'Agente IA para Leads',
        pageSubtitle: 'MVP listo para demo de leads B2B entrantes, calificación y transferencia.',
        sendSectionTitle: 'Enviar mensaje',
        sendBtn: 'Enviar',
        clearBtn: 'Limpiar',
        sendHint: 'Después de la respuesta, el lead_id se completará automáticamente en el resumen.',
        rawResponseSummary: 'Respuesta bruta',
        summarySectionTitle: 'Resumen del lead',
        loadSummaryBtn: 'Cargar resumen',
        rawSummarySummary: 'JSON bruto del resumen',
        dashboardSectionTitle: 'Resumen del panel',
        refreshDashboardBtn: 'Actualizar panel',
        metricLeadsLabel: 'Leads totales',
        metricQualifiedLabel: 'Calificados',
        metricInProgressLabel: 'Transferencias en progreso',
        metricDoneLabel: 'Transferencias completadas',
        rawDashboardSummary: 'JSON bruto del panel',
        leadsSectionTitle: 'Leads recientes',
        refreshLeadsBtn: 'Actualizar',
        rawLeadsSummary: 'JSON bruto de leads',
        handoffsSectionTitle: 'Transferencias recientes',
        refreshHandoffsBtn: 'Actualizar',
        rawHandoffsSummary: 'JSON bruto de transferencias',
        loadDemoBtn: 'Cargar demo',
        resetDemoBtn: 'Restablecer demo',
        footerText: 'MVP público de demo desplegado en Render.',
        leadIdPlaceholder: 'lead_id — opcional para el primer mensaje',
        summaryLeadIdPlaceholder: 'Ingresa lead_id',
        messagePlaceholder: 'Ingresa el mensaje entrante...',
        empty: '(vacío)',
        noSummary: 'Vacío.',
        noLeads: 'No hay leads.',
        noHandoffs: 'No hay transferencias.',
        company: 'Empresa',
        role: 'Rol',
        contact: 'Contacto',
        useCase: 'Caso de uso',
        assignedTo: 'Asignado a',
        lastSender: 'Último remitente',
        lastIntent: 'Última intención',
        lastText: 'Último texto',
        notAssigned: 'Sin asignar',
        status_new: 'nuevo',
        status_qualified: 'calificado',
        status_needs_followup: 'requiere seguimiento',
        status_pending: 'listo para transferencia',
        status_in_progress: 'en progreso',
        status_done: 'completado',
        status_unknown: 'desconocido',
        moveToInProgress: 'Mover a en progreso',
        markDone: 'Marcar como completada',
        open: 'Abrir',
        toastDemoLoaded: 'Datos demo cargados.',
        toastDemoReset: 'Datos demo restablecidos.',
        toastMessageSent: 'Mensaje procesado.',
        toastSummaryLoaded: 'Resumen del lead cargado.',
        toastDashboardRefreshed: 'Panel actualizado.',
        toastLeadsRefreshed: 'Leads actualizados.',
        toastHandoffsRefreshed: 'Transferencias actualizadas.',
        toastHandoffUpdated: 'Transferencia actualizada.',
        toastError: 'Algo salió mal.',
        polishedAssistantReply: 'Gracias. Los datos clave fueron extraídos, el lead quedó calificado y listo para transferencia.',
      }
    };

    let currentLang = localStorage.getItem('ui_lang') || 'ru';
    let lastSummary = null;
    let lastDashboard = null;
    let lastLeads = [];
    let lastHandoffs = [];

    const $ = (id) => document.getElementById(id);
    const t = (key) => (i18n[currentLang] && i18n[currentLang][key]) || key;

    function showToast(message, kind='success') {
      const wrap = $('toastWrap');
      const toast = document.createElement('div');
      toast.className = `toast ${kind}`;
      toast.textContent = message;
      wrap.appendChild(toast);
      setTimeout(() => toast.remove(), 2600);
    }

    function safeJson(obj) {
      try { return JSON.stringify(obj, null, 2); }
      catch { return String(obj); }
    }

    function setLang(lang) {
      currentLang = lang;
      localStorage.setItem('ui_lang', lang);

      document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
      });

      $('pageTitle').textContent = t('pageTitle');
      $('pageSubtitle').textContent = t('pageSubtitle');
      $('sendSectionTitle').textContent = t('sendSectionTitle');
      $('sendBtn').textContent = t('sendBtn');
      $('clearBtn').textContent = t('clearBtn');
      $('sendHint').textContent = t('sendHint');
      $('rawResponseSummary').textContent = t('rawResponseSummary');
      $('summarySectionTitle').textContent = t('summarySectionTitle');
      $('loadSummaryBtn').textContent = t('loadSummaryBtn');
      $('rawSummarySummary').textContent = t('rawSummarySummary');
      $('dashboardSectionTitle').textContent = t('dashboardSectionTitle');
      $('refreshDashboardBtn').textContent = t('refreshDashboardBtn');
      $('metricLeadsLabel').textContent = t('metricLeadsLabel');
      $('metricQualifiedLabel').textContent = t('metricQualifiedLabel');
      $('metricInProgressLabel').textContent = t('metricInProgressLabel');
      $('metricDoneLabel').textContent = t('metricDoneLabel');
      $('rawDashboardSummary').textContent = t('rawDashboardSummary');
      $('leadsSectionTitle').textContent = t('leadsSectionTitle');
      $('refreshLeadsBtn').textContent = t('refreshLeadsBtn');
      $('rawLeadsSummary').textContent = t('rawLeadsSummary');
      $('handoffsSectionTitle').textContent = t('handoffsSectionTitle');
      $('refreshHandoffsBtn').textContent = t('refreshHandoffsBtn');
      $('rawHandoffsSummary').textContent = t('rawHandoffsSummary');
      $('loadDemoBtn').textContent = t('loadDemoBtn');
      $('resetDemoBtn').textContent = t('resetDemoBtn');
      $('footerText').textContent = t('footerText');

      $('leadIdInput').placeholder = t('leadIdPlaceholder');
      $('summaryLeadIdInput').placeholder = t('summaryLeadIdPlaceholder');
      $('messageInput').placeholder = t('messagePlaceholder');

      if ($('sendResult').textContent === '(пусто)' || $('sendResult').textContent === '(empty)' || $('sendResult').textContent === '(vacío)') {
        $('sendResult').textContent = t('empty');
      }
      if ($('summaryResult').textContent === '(пусто)' || $('summaryResult').textContent === '(empty)' || $('summaryResult').textContent === '(vacío)') {
        $('summaryResult').textContent = t('empty');
      }
      if ($('dashboardResult').textContent === '(пусто)' || $('dashboardResult').textContent === '(empty)' || $('dashboardResult').textContent === '(vacío)') {
        $('dashboardResult').textContent = t('empty');
      }
      if ($('leadsRaw').textContent === '(пусто)' || $('leadsRaw').textContent === '(empty)' || $('leadsRaw').textContent === '(vacío)') {
        $('leadsRaw').textContent = t('empty');
      }
      if ($('handoffsRaw').textContent === '(пусто)' || $('handoffsRaw').textContent === '(empty)' || $('handoffsRaw').textContent === '(vacío)') {
        $('handoffsRaw').textContent = t('empty');
      }

      renderSummary(lastSummary);
      renderDashboard(lastDashboard);
      renderLeads(lastLeads);
      renderHandoffs(lastHandoffs);
    }

    function mapStatus(status) {
      if (!status) return t('status_unknown');
      const key = `status_${String(status).toLowerCase()}`;
      return t(key);
    }

    function badgeClass(status) {
      const s = String(status || '').toLowerCase();
      if (['qualified', 'done'].includes(s)) return 'badge-green';
      if (['pending', 'needs_followup'].includes(s)) return 'badge-orange';
      if (['in_progress'].includes(s)) return 'badge-blue';
      return 'badge-gray';
    }

    function prettyAssistantText(text, sender) {
      const raw = String(text || '').trim();
      if (!raw) return t('empty');

      const normalized = raw.toLowerCase();

      const known = [
        'понял ваш запрос. спасибо, базовую информацию получил.',
        'thanks. basic information received.',
        'gracias. información básica recibida.'
      ];

      if (sender === 'assistant' && known.includes(normalized)) {
        return t('polishedAssistantReply');
      }
      return raw;
    }

    function normalizeSummaryForDisplay(summary) {
      if (!summary || !summary.lead) return summary;

      const clone = JSON.parse(JSON.stringify(summary));
      const lead = clone.lead || {};
      const handoff = clone.handoff || {};
      const conversation = clone.conversation || {};

      if (!handoff.assigned_to) {
        handoff.assigned_to = t('notAssigned');
      }

      conversation.last_text = prettyAssistantText(conversation.last_text, conversation.last_sender);

      clone.lead = lead;
      clone.handoff = handoff;
      clone.conversation = conversation;
      return clone;
    }

    async function fetchJSON(url, options={}) {
      const res = await fetch(url, {
        headers: { 'Content-Type': 'application/json' },
        ...options
      });

      const text = await res.text();
      let data = null;

      try {
        data = text ? JSON.parse(text) : null;
      } catch {
        data = { raw: text };
      }

      if (!res.ok) {
        const errText = data && data.detail ? data.detail : text || res.statusText;
        throw new Error(errText);
      }

      return data;
    }

    function renderSummary(summary) {
      lastSummary = summary;
      const box = $('summaryBox');
      box.innerHTML = '';

      if (!summary || !summary.lead) {
        const empty = document.createElement('div');
        empty.id = 'summaryEmpty';
        empty.className = 'hint';
        empty.textContent = t('noSummary');
        box.appendChild(empty);
        return;
      }

      const data = normalizeSummaryForDisplay(summary);
      const lead = data.lead || {};
      const handoff = data.handoff || {};
      const convo = data.conversation || {};

      const wrap = document.createElement('div');
      wrap.className = 'summary-box';

      const badges = document.createElement('div');
      badges.className = 'badges';
      badges.innerHTML = `
        <span class="badge badge-id">lead_id: ${lead.id ?? '-'}</span>
        <span class="badge ${badgeClass(lead.lead_status)}">${mapStatus(lead.lead_status)}</span>
        <span class="badge ${badgeClass(handoff.handoff_status || 'pending')}">${mapStatus(handoff.handoff_status || 'pending')}</span>
      `;
      wrap.appendChild(badges);

      const rows = [
        [t('company'), lead.company || t('empty')],
        [t('role'), lead.role || t('empty')],
        [t('contact'), lead.contact || t('empty')],
        [t('useCase'), lead.use_case || t('empty')],
        [t('assignedTo'), handoff.assigned_to || t('notAssigned')],
        [t('lastSender'), convo.last_sender || t('empty')],
        [t('lastIntent'), convo.last_intent || t('empty')],
        [t('lastText'), convo.last_text || t('empty')],
      ];

      rows.forEach(([k, v]) => {
        const row = document.createElement('div');
        row.className = 'kv';
        row.innerHTML = `<div class="k">${k}:</div><div class="v">${v}</div>`;
        wrap.appendChild(row);
      });

      const actions = document.createElement('div');
      actions.className = 'summary-actions';
      actions.innerHTML = `
        <button class="btn btn-gray" id="setInProgressBtn">${t('moveToInProgress')}</button>
        <button class="btn btn-green" id="setDoneBtn">${t('markDone')}</button>
      `;
      wrap.appendChild(actions);
      box.appendChild(wrap);

      const leadId = lead.id;
      $('setInProgressBtn').onclick = async () => {
        if (!leadId) return;
        await tryHandoffAction(leadId, 'in_progress');
      };

      $('setDoneBtn').onclick = async () => {
        if (!leadId) return;
        await tryHandoffAction(leadId, 'done');
      };
    }

    function renderDashboard(data) {
      lastDashboard = data;
      $('metricLeads').textContent = data?.leads_total ?? 0;
      $('metricQualified').textContent = data?.qualified_total ?? 0;
      $('metricInProgress').textContent = data?.handoffs_in_progress ?? 0;
      $('metricDone').textContent = data?.handoffs_done ?? 0;
      $('dashboardResult').textContent = data ? safeJson(data) : t('empty');
    }

    function renderLeads(items) {
      lastLeads = Array.isArray(items) ? items : [];
      $('leadsRaw').textContent = lastLeads.length ? safeJson(lastLeads) : t('empty');

      const root = $('leadsList');
      root.innerHTML = '';

      if (!lastLeads.length) {
        const empty = document.createElement('div');
        empty.className = 'hint';
        empty.textContent = t('noLeads');
        root.appendChild(empty);
        return;
      }

      lastLeads.forEach((item) => {
        const el = document.createElement('div');
        el.className = 'list-item';
        el.innerHTML = `
          <div class="list-top">
            <div>
              <div class="list-title">${item.company || item.contact || ('lead_id ' + item.id)}</div>
              <div class="list-sub">${t('role')}: ${item.role || t('empty')} · ${t('contact')}: ${item.contact || t('empty')}</div>
            </div>
            <div class="badges">
              <span class="badge badge-id">lead_id: ${item.id ?? '-'}</span>
              <span class="badge ${badgeClass(item.lead_status)}">${mapStatus(item.lead_status)}</span>
            </div>
          </div>
          <div class="list-sub">${item.use_case || t('empty')}</div>
          <div class="list-actions">
            <button class="btn btn-blue open-lead-btn" data-lead-id="${item.id}">${t('open')}</button>
          </div>
        `;
        root.appendChild(el);
      });

      root.querySelectorAll('.open-lead-btn').forEach(btn => {
        btn.onclick = async () => {
          const id = btn.dataset.leadId;
          $('summaryLeadIdInput').value = id;
          await loadSummary(id);
        };
      });
    }

    function renderHandoffs(items) {
      lastHandoffs = Array.isArray(items) ? items : [];
      $('handoffsRaw').textContent = lastHandoffs.length ? safeJson(lastHandoffs) : t('empty');

      const root = $('handoffsList');
      root.innerHTML = '';

      if (!lastHandoffs.length) {
        const empty = document.createElement('div');
        empty.className = 'hint';
        empty.textContent = t('noHandoffs');
        root.appendChild(empty);
        return;
      }

      lastHandoffs.forEach((item) => {
        const el = document.createElement('div');
        el.className = 'list-item';

        const assigned = item.assigned_to || t('notAssigned');
        const status = item.handoff_status || 'pending';

        el.innerHTML = `
          <div class="list-top">
            <div>
              <div class="list-title">${item.company || item.contact || ('lead_id ' + item.lead_id)}</div>
              <div class="list-sub">${t('assignedTo')}: ${assigned}</div>
            </div>
            <div class="badges">
              <span class="badge badge-id">lead_id: ${item.lead_id ?? '-'}</span>
              <span class="badge ${badgeClass(status)}">${mapStatus(status)}</span>
            </div>
          </div>
          <div class="list-sub">${item.reason || t('empty')}</div>
        `;
        root.appendChild(el);
      });
    }

    async function tryHandoffAction(leadId, action) {
      const endpoints = action === 'in_progress'
        ? [`/handoffs/${leadId}/in-progress`, `/handoffs/${leadId}/start`, `/handoffs/${leadId}/in_progress`]
        : [`/handoffs/${leadId}/done`, `/handoffs/${leadId}/complete`];

      for (const url of endpoints) {
        try {
          await fetchJSON(url, { method: 'POST' });
          showToast(t('toastHandoffUpdated'));
          await refreshAll();
          return;
        } catch (_) {}
      }

      showToast(t('toastError'), 'error');
    }

    async function sendMessage() {
  const leadId = $('leadIdInput').value.trim();
  const messageText = $('messageInput').value.trim();

  if (!messageText) {
    showToast(t('toastError'), 'error');
    return;
  }

  const payload = {
    message: messageText,
    message_text: messageText
  };

  if (leadId) {
    payload.lead_id = Number(leadId);
  }

  try {
    const data = await fetchJSON('/chat/message', {
      method: 'POST',
      body: JSON.stringify(payload)
    });

    $('sendResult').textContent = safeJson(data);

    const newLeadId =
      data?.lead_id ??
      data?.lead?.id ??
      data?.summary?.lead?.id ??
      leadId;

    if (newLeadId) {
      $('leadIdInput').value = String(newLeadId);
      $('summaryLeadIdInput').value = String(newLeadId);
      await loadSummary(String(newLeadId), false);
    }

    await refreshAll(false);
    showToast(t('toastMessageSent'));
  } catch (e) {
    $('sendResult').textContent = String(e.message || e);
    showToast(String(e.message || t('toastError')), 'error');
  }
}

    async function loadSummary(id = null, toast = true) {
      const leadId = id || $('summaryLeadIdInput').value.trim();
      if (!leadId) return;

      try {
        const data = await fetchJSON(`/leads/${leadId}/summary`);
        $('summaryResult').textContent = safeJson(data);
        renderSummary(data);
        if (toast) showToast(t('toastSummaryLoaded'));
      } catch (e) {
        $('summaryResult').textContent = String(e.message || e);
        renderSummary(null);
        showToast(t('toastError'), 'error');
      }
    }

    async function loadDashboard(toast = true) {
      try {
        const data = await fetchJSON('/dashboard/overview');
        renderDashboard(data);
        if (toast) showToast(t('toastDashboardRefreshed'));
      } catch (e) {
        $('dashboardResult').textContent = String(e.message || e);
        showToast(t('toastError'), 'error');
      }
    }

    async function loadLeads(toast = true) {
      try {
        const data = await fetchJSON('/leads');
        renderLeads(data || []);
        if (toast) showToast(t('toastLeadsRefreshed'));
      } catch (e) {
        $('leadsRaw').textContent = String(e.message || e);
        renderLeads([]);
        showToast(t('toastError'), 'error');
      }
    }

    async function loadHandoffs(toast = true) {
      try {
        const data = await fetchJSON('/handoffs');
        renderHandoffs(data || []);
        if (toast) showToast(t('toastHandoffsRefreshed'));
      } catch (e) {
        $('handoffsRaw').textContent = String(e.message || e);
        renderHandoffs([]);
        showToast(t('toastError'), 'error');
      }
    }

    async function refreshAll(toast = false) {
      await Promise.all([
        loadDashboard(toast),
        loadLeads(toast),
        loadHandoffs(toast)
      ]);
    }

    async function loadDemo() {
      const candidates = ['/demo/load', '/demo/load-data', '/demo/seed'];

      for (const url of candidates) {
        try {
          const data = await fetchJSON(url, { method: 'POST' });
          $('sendResult').textContent = safeJson(data);
          await refreshAll(false);
          showToast(t('toastDemoLoaded'));
          return;
        } catch (_) {}
      }

      showToast(t('toastError'), 'error');
    }

    async function resetDemo() {
      const candidates = ['/demo/reset', '/demo/reset-data'];

      for (const url of candidates) {
        try {
          const data = await fetchJSON(url, { method: 'POST' });
          $('sendResult').textContent = safeJson(data);
          $('leadIdInput').value = '';
          $('summaryLeadIdInput').value = '';
          $('messageInput').value = '';
          $('summaryResult').textContent = t('empty');
          renderSummary(null);
          await refreshAll(false);
          showToast(t('toastDemoReset'));
          return;
        } catch (_) {}
      }

      showToast(t('toastError'), 'error');
    }

    function clearForm() {
      $('leadIdInput').value = '';
      $('messageInput').value = '';
      $('sendResult').textContent = t('empty');
    }

    document.addEventListener('DOMContentLoaded', async () => {
      document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => setLang(btn.dataset.lang));
      });

      $('sendBtn').addEventListener('click', sendMessage);
      $('clearBtn').addEventListener('click', clearForm);
      $('loadSummaryBtn').addEventListener('click', () => loadSummary());
      $('refreshDashboardBtn').addEventListener('click', () => loadDashboard());
      $('refreshLeadsBtn').addEventListener('click', () => loadLeads());
      $('refreshHandoffsBtn').addEventListener('click', () => loadHandoffs());
      $('loadDemoBtn').addEventListener('click', loadDemo);
      $('resetDemoBtn').addEventListener('click', resetDemo);

      $('sendResult').textContent = t('empty');
      $('summaryResult').textContent = t('empty');
      $('dashboardResult').textContent = t('empty');
      $('leadsRaw').textContent = t('empty');
      $('handoffsRaw').textContent = t('empty');

      setLang(currentLang);
      renderSummary(null);
      renderDashboard(null);
      renderLeads([]);
      renderHandoffs([]);

      await refreshAll(false);
    });
  </script>
</body>
</html>
"""


@router.get("/ui", response_class=HTMLResponse)
async def ui():
    return HTMLResponse(ui_page())
