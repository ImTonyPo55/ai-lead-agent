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
  <title>MechanicFlow AI</title>
  <style>
    :root {
      --bg: #202428;
      --panel: #2A2F35;
      --panel-2: rgba(255,255,255,0.06);
      --border: rgba(255,255,255,0.14);
      --text: #F5F7FA;
      --muted: #B8C0CC;
      --muted-2: #7D8794;
      --green: #33FF00;
      --red: #FF3300;
      --orange: #FFB84D;
      --gray: #7D8794;
      --button-text: #111418;
      --shadow: 0 20px 50px rgba(0, 0, 0, 0.28);
      --radius: 18px;
    }

    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; }
    body {
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 18% 0%, rgba(255,255,255,0.08), transparent 28%),
        linear-gradient(180deg, #2A2F35 0%, #202428 52%, #1A1E22 100%);
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
      background: #F5F7FA;
      color: #111418;
      border-color: rgba(255,255,255,0.16);
      box-shadow: 0 8px 22px rgba(0,0,0,0.24);
    }

    .btn {
      min-height: 40px;
      padding: 10px 14px;
      border-radius: 12px;
      font-size: 14px;
      box-shadow: var(--shadow);
    }

    .btn-action {
      background: #33FF00;
      color: var(--button-text);
      box-shadow: 0 0 0 1px rgba(51,255,0,0.28), 0 14px 34px rgba(51,255,0,0.18);
    }
    .btn-action:hover { transform: translateY(-1px); box-shadow: 0 0 0 1px rgba(51,255,0,0.42), 0 18px 42px rgba(51,255,0,0.22); }
    .btn-green {
      background: #33FF00;
      color: var(--button-text);
      box-shadow: 0 0 0 1px rgba(51,255,0,0.28), 0 14px 34px rgba(51,255,0,0.18);
    }
    .btn-red {
      background: #FF3300;
      color: var(--button-text);
      box-shadow: 0 0 0 1px rgba(255,51,0,0.30), 0 14px 34px rgba(255,51,0,0.18);
    }
    .btn-gray { background: rgba(255,255,255,0.10); color: var(--text); border: 1px solid var(--border); }
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
      background: var(--panel-2);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 18px;
      box-shadow: var(--shadow);
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
      background: rgba(255,255,255,0.045);
      border: 1px solid var(--border);
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

    .example-panel {
      margin-top: 10px;
      margin-bottom: 12px;
      padding: 12px;
      border: 1px solid var(--border);
      border-radius: 14px;
      background: rgba(255,255,255,0.035);
    }

    .example-title {
      color: var(--muted-2);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 8px;
    }

    .field-label {
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      margin-bottom: 7px;
    }

    .field-help {
      color: var(--muted-2);
      font-size: 12px;
      line-height: 1.4;
      margin-top: 6px;
    }

    .example-grid {
      display: grid;
      gap: 8px;
    }

    .example-pill {
      width: 100%;
      text-align: left;
      padding: 10px 12px;
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,0.12);
      background: rgba(255,255,255,0.055);
      color: var(--text);
      box-shadow: none;
      font-size: 12px;
      line-height: 1.35;
    }

    details {
      border: 1px solid var(--border);
      border-radius: 12px;
      background: rgba(255,255,255,0.035);
      overflow: hidden;
      margin-top: 12px;
    }

    summary {
      list-style: none;
      cursor: pointer;
      padding: 10px 12px;
      font-size: 12px;
      font-weight: 700;
      color: var(--muted);
      border-bottom: 1px solid transparent;
    }

    summary::-webkit-details-marker { display: none; }

    details[open] summary {
      border-bottom-color: var(--border);
      background: rgba(255,255,255,0.03);
    }

    pre {
      margin: 0;
      padding: 14px;
      overflow: auto;
      white-space: pre-wrap;
      word-break: break-word;
      font-size: 11px;
      color: var(--muted);
      border: 0;
      border-radius: 0;
      max-height: 320px;
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
    .badge-green { background: rgba(51,255,0,0.15); color: #33FF00; border: 1px solid rgba(51,255,0,0.38); }
    .badge-orange { background: rgba(255,184,77,0.16); color: var(--orange); border: 1px solid rgba(255,184,77,0.34); }
    .badge-gray { background: rgba(125,135,148,0.18); color: #D5DBE3; border: 1px solid rgba(125,135,148,0.34); }
    .badge-graphite { background: rgba(245,247,250,0.14); color: var(--text); border: 1px solid rgba(245,247,250,0.30); }

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
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--border);
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
      background: rgba(255,255,255,0.045);
      border: 1px solid var(--border);
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

    .lifecycle-note {
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,0.12);
      background: rgba(255,255,255,0.04);
      color: var(--text);
      padding: 10px 12px;
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
      color: var(--text);
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
      background: rgba(32,36,40,0.96);
      border: 1px solid var(--border);
      color: #fff;
      border-radius: 14px;
      padding: 12px 14px;
      box-shadow: var(--shadow);
      font-size: 13px;
      line-height: 1.45;
    }

    .toast.success { border-color: rgba(51,255,0,0.42); }
    .toast.error { border-color: rgba(255,51,0,0.42); }

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
        <h1 id="pageTitle">MechanicFlow AI</h1>
        <p id="pageSubtitle">AI intake agent for gamified campaign leads, mechanic recommendation, qualification, CRM-ready handoff.</p>
      </div>

      <div class="controls">
        <div class="lang-switch">
          <button class="lang-btn" data-lang="ru">RU</button>
          <button class="lang-btn" data-lang="en">EN</button>
          <button class="lang-btn" data-lang="es">ES</button>
        </div>

        <button id="loadDemoBtn" class="btn btn-green">Загрузить примеры</button>
        <button id="resetDemoBtn" class="btn btn-red">Очистить данные</button>
      </div>
    </div>

    <div class="grid-2">
      <div class="card">
        <div class="section-title">
          <h3 id="sendSectionTitle">Отправить сообщение</h3>
        </div>

        <div id="leadIdLabel" class="field-label">lead_id</div>
        <input id="leadIdInput" placeholder="Оставьте пустым для нового лида" />
        <div id="leadIdHelp" class="field-help">Укажите существующий lead_id только если продолжаете текущий диалог.</div>
        <div style="height: 10px;"></div>
        <div id="messageLabel" class="field-label">Входящее сообщение</div>
        <textarea id="messageInput" placeholder="Например: We are UrbanFit. Need a spin-to-win campaign for Shopify lead capture. Contact @urbanfit_cmo"></textarea>
        <div class="example-panel">
          <div id="demoExamplesTitle" class="example-title">Campaign examples</div>
          <div id="demoExamples" class="example-grid"></div>
        </div>

        <div class="actions">
          <button id="sendBtn" class="btn btn-action">Отправить</button>
          <button id="clearBtn" class="btn btn-gray">Очистить</button>
        </div>

        <div id="sendHint" class="hint">
          После ответа lead_id автоматически подставится в сводку.
        </div>

        <details>
          <summary id="rawResponseSummary">Технический ответ</summary>
          <pre id="sendResult">—</pre>
        </details>
      </div>

      <div class="card">
        <div class="section-title">
          <h3 id="summarySectionTitle">Сводка лида кампании</h3>
        </div>

        <input id="summaryLeadIdInput" placeholder="Введите lead_id" />
        <div style="height: 10px;"></div>
        <button id="loadSummaryBtn" class="btn btn-action">Загрузить сводку</button>

        <div style="height: 14px;"></div>

        <div class="summary-box" id="summaryBox">
          <div id="summaryEmpty" class="hint">Пока пусто.</div>
        </div>

        <details>
          <summary id="rawSummarySummary">Технический JSON сводки</summary>
          <pre id="summaryResult">—</pre>
        </details>
      </div>
    </div>

    <div class="card">
      <div class="section-title">
        <h3 id="dashboardSectionTitle">Обзор панели</h3>
        <button id="refreshDashboardBtn" class="btn btn-action">Обновить панель</button>
      </div>

      <div class="grid-4">
        <div class="metric">
          <div class="label" id="metricLeadsLabel">Лиды кампаний</div>
          <div id="metricLeads" class="value">0</div>
        </div>
        <div class="metric">
          <div class="label" id="metricQualifiedLabel">Готовы к передаче</div>
          <div id="metricQualified" class="value">0</div>
        </div>
        <div class="metric">
          <div class="label" id="metricInProgressLabel">В работе</div>
          <div id="metricInProgress" class="value">0</div>
        </div>
        <div class="metric">
          <div class="label" id="metricDoneLabel">Завершены</div>
          <div id="metricDone" class="value">0</div>
        </div>
      </div>

      <div style="margin-top: 14px;">
        <details>
          <summary id="rawDashboardSummary">Технический JSON панели</summary>
          <pre id="dashboardResult">—</pre>
        </details>
      </div>
    </div>

    <div class="grid-bottom">
      <div class="card">
        <div class="section-title">
          <h3 id="leadsSectionTitle">Последние лиды кампаний</h3>
          <button id="refreshLeadsBtn" class="btn btn-action">Обновить</button>
        </div>

        <div id="leadsList" class="list"></div>

        <div style="margin-top: 14px;">
          <details>
            <summary id="rawLeadsSummary">Технический JSON лидов</summary>
            <pre id="leadsRaw">—</pre>
          </details>
        </div>
      </div>

      <div class="card">
        <div class="section-title">
          <h3 id="handoffsSectionTitle">Последние передачи</h3>
          <button id="refreshHandoffsBtn" class="btn btn-action">Обновить</button>
        </div>

        <div id="handoffsList" class="list"></div>

        <div style="margin-top: 14px;">
          <details>
            <summary id="rawHandoffsSummary">Технический JSON передач</summary>
            <pre id="handoffsRaw">—</pre>
          </details>
        </div>
      </div>
    </div>

    <div class="footer">
      <div id="footerText">MechanicFlow AI operational workspace for campaign lead qualification and handoff.</div>
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
        pageTitle: 'MechanicFlow AI',
        pageSubtitle: 'AI intake agent for gamified campaign leads, mechanic recommendation, qualification, CRM-ready handoff.',
        sendSectionTitle: 'Отправить сообщение',
        sendBtn: 'Отправить',
        clearBtn: 'Очистить',
        sendHint: 'Оставьте lead_id пустым для нового лида или укажите существующий lead_id, чтобы продолжить диалог.',
        demoExamplesTitle: 'Примеры входящих запросов',
        demoExamples: [
          'We are Bloom Retail. Need a holiday promo game to collect emails and boost repeat purchases. Contact @bloom_growth',
          'We are UrbanFit. Need a spin-to-win campaign for Shopify lead capture. Contact @urbanfit_cmo',
          'We are FreshBox. Need a retention campaign with rewards for returning customers. Contact @freshbox_growth',
          'We are Nova Agency. Need a branded Advent Calendar campaign for a client. Contact @nova_agency',
          'We are GameLaunch Studio. Need a quiz lead magnet for a new product launch. Contact @gamelaunch_cmo',
        ],
        rawResponseSummary: 'Технический ответ',
        summarySectionTitle: 'Сводка лида кампании',
        loadSummaryBtn: 'Загрузить сводку',
        rawSummarySummary: 'Технический JSON сводки',
        dashboardSectionTitle: 'Обзор панели',
        refreshDashboardBtn: 'Обновить панель',
        metricLeadsLabel: 'Лиды кампаний',
        metricQualifiedLabel: 'Готовы к передаче',
        metricInProgressLabel: 'В работе',
        metricDoneLabel: 'Завершены',
        rawDashboardSummary: 'Технический JSON панели',
        leadsSectionTitle: 'Последние лиды кампаний',
        refreshLeadsBtn: 'Обновить',
        rawLeadsSummary: 'Технический JSON лидов',
        handoffsSectionTitle: 'Последние передачи',
        refreshHandoffsBtn: 'Обновить',
        rawHandoffsSummary: 'Технический JSON передач',
        loadDemoBtn: 'Загрузить примеры',
        resetDemoBtn: 'Очистить данные',
        footerText: 'MechanicFlow AI operational workspace for campaign lead qualification and handoff.',
        leadIdLabel: 'lead_id',
        leadIdHelp: 'Укажите существующий lead_id только если продолжаете текущий диалог.',
        messageLabel: 'Входящее сообщение',
        leadIdPlaceholder: 'Оставьте пустым для нового лида',
        summaryLeadIdPlaceholder: 'Введите lead_id',
        messagePlaceholder: 'Например: We are UrbanFit. Need a spin-to-win campaign for Shopify lead capture. Contact @urbanfit_cmo',
        empty: '—',
        noSummary: 'Выберите лид или отправьте новое входящее сообщение.',
        noLeads: 'Лидов кампаний пока нет.',
        noHandoffs: 'Передач пока нет.',
        leadId: 'lead_id',
        company: 'Компания',
        role: 'Роль',
        contact: 'Контакт',
        useCase: 'Запрос кампании',
        clientType: 'Тип клиента',
        campaignGoal: 'Цель кампании',
        platform: 'Платформа',
        campaignIntelligence: 'Аналитика кампании',
        recommendedMechanic: 'Лучшая игра для кампании',
        mechanicName: 'Игровая механика',
        mechanicReason: 'Почему подходит',
        pricingTier: 'Тариф',
        qualificationStatus: 'Статус квалификации',
        missingFields: 'Недостающие поля',
        recommendedPackage: 'Рекомендованный пакет',
        suggestedTier: 'Рекомендуемый тариф',
        copyReadyFollowup: 'Готовый follow-up',
        copyFollowup: 'Скопировать follow-up',
        score: 'Оценка',
        priority: 'Приоритет',
        eventTimeline: 'История событий',
        noEvents: 'Событий пока нет.',
        crmEvent: 'Событие CRM',
        handoffPackage: 'Пакет передачи кампании',
        followupPackage: 'Пакет follow-up',
        packageSummary: 'Резюме',
        qualificationReason: 'Причина квалификации',
        recommendedNextAction: 'Следующее действие',
        recommendedMechanicSection: 'Рекомендованная игровая механика',
        crmPayloadPreview: 'CRM payload',
        exportCrm: 'Экспорт в CRM',
        copyPackage: 'Скопировать пакет',
        handoffStatus: 'Статус передачи',
        lifecycleReady: 'Лид готов к передаче: CRM export, копирование пакета и перевод в работу доступны.',
        lifecycleActive: 'Передача уже взята в работу. Новый handoff не создаётся повторно.',
        lifecycleCompleted: 'Передача завершена. CRM export повторно не предлагается.',
        lifecycleFollowup: 'Лид требует уточнения. Доступен только follow-up без CRM export.',
        ownerSection: 'Ответственный',
        team: 'Команда',
        routingReason: 'Причина назначения',
        actionSection: 'Следующее действие',
        actionStatus: 'Статус',
        actionNext: 'Следующее действие',
        actionReason: 'Причина',
        actionLabel: 'Действие',
        actionContacted: 'Связаться',
        actionWaitingReply: 'Ждём ответ',
        actionClosed: 'Закрыть действие',
        actionStatus_new: 'Новое',
        actionStatus_contacted: 'Связались',
        actionStatus_waiting_reply: 'Ждём ответ',
        actionStatus_closed: 'Закрыто',
        assignTony: 'Назначить Tony',
        assignSales: 'Назначить Sales',
        assignSupport: 'Назначить Support',
        assignedTo: 'Назначен',
        lastSender: 'Последний отправитель',
        lastIntent: 'Последнее намерение',
        lastText: 'Последний текст',
        notAssigned: 'Не назначен',
        status_new: 'новый',
        status_qualified: 'квалифицирован',
        status_ready_to_handoff: 'готов к передаче',
        status_active_handoff: 'в работе',
        status_completed_handoff: 'завершено',
        status_needs_followup: 'требует уточнения',
        status_needs_follow_up: 'требует уточнения',
        status_pending: 'готов к передаче',
        status_in_progress: 'в работе',
        status_done: 'завершено',
        status_completed: 'завершено',
        status_unknown: 'неизвестно',
        moveToInProgress: 'Перевести в работу',
        markDone: 'Завершить передачу',
        open: 'Открыть',
        toastDemoLoaded: 'Примеры загружены.',
        toastDemoReset: 'Данные очищены.',
        toastMessageSent: 'Сообщение обработано.',
        toastSummaryLoaded: 'Сводка по лиду загружена.',
        toastDashboardRefreshed: 'Панель обновлена.',
        toastLeadsRefreshed: 'Лиды обновлены.',
        toastHandoffsRefreshed: 'Передачи обновлены.',
        toastHandoffUpdated: 'Статус передачи обновлён.',
        toastCrmExported: 'CRM-экспорт подготовлен.',
        toastPackageCopied: 'Пакет скопирован.',
        toastFollowupCopied: 'Follow-up скопирован.',
        toastOwnerAssigned: 'Ответственный назначен.',
        toastActionUpdated: 'Статус действия обновлён.',
        toastError: 'Что-то пошло не так.',
        polishedAssistantReply: 'Спасибо. Лид кампании квалифицирован, механика подобрана и пакет передачи готов.',
      },
      en: {
        pageTitle: 'MechanicFlow AI',
        pageSubtitle: 'AI intake agent for gamified campaign leads, mechanic recommendation, qualification, CRM-ready handoff.',
        sendSectionTitle: 'Send message',
        sendBtn: 'Send',
        clearBtn: 'Clear',
        sendHint: 'Try a campaign example or send an inbound request from a brand, eCommerce team, or agency.',
        demoExamplesTitle: 'Campaign examples',
        demoExamples: [
          'We are Bloom Retail. Need a holiday promo game to collect emails and boost repeat purchases. Contact @bloom_growth',
          'We are UrbanFit. Need a spin-to-win campaign for Shopify lead capture. Contact @urbanfit_cmo',
          'We are FreshBox. Need a retention campaign with rewards for returning customers. Contact @freshbox_growth',
          'We are Nova Agency. Need a branded Advent Calendar campaign for a client. Contact @nova_agency',
          'We are GameLaunch Studio. Need a quiz lead magnet for a new product launch. Contact @gamelaunch_cmo',
        ],
        rawResponseSummary: 'Technical response',
        summarySectionTitle: 'Campaign lead summary',
        loadSummaryBtn: 'Load summary',
        rawSummarySummary: 'Technical summary JSON',
        dashboardSectionTitle: 'Dashboard overview',
        refreshDashboardBtn: 'Refresh dashboard',
        metricLeadsLabel: 'Campaign leads',
        metricQualifiedLabel: 'Qualified',
        metricInProgressLabel: 'In progress',
        metricDoneLabel: 'Completed',
        rawDashboardSummary: 'Technical dashboard JSON',
        leadsSectionTitle: 'Recent campaign leads',
        refreshLeadsBtn: 'Refresh',
        rawLeadsSummary: 'Technical leads JSON',
        handoffsSectionTitle: 'Recent handoffs',
        refreshHandoffsBtn: 'Refresh',
        rawHandoffsSummary: 'Technical handoffs JSON',
        loadDemoBtn: 'Load examples',
        resetDemoBtn: 'Clear data',
        footerText: 'MechanicFlow AI operational workspace for campaign lead qualification and handoff.',
        leadIdLabel: 'lead_id',
        leadIdHelp: 'Use an existing lead_id only when continuing an active conversation.',
        messageLabel: 'Inbound message',
        leadIdPlaceholder: 'Leave empty to create a new lead',
        summaryLeadIdPlaceholder: 'Enter lead_id',
        messagePlaceholder: 'Example: We are UrbanFit. Need a spin-to-win campaign for Shopify lead capture. Contact @urbanfit_cmo',
        empty: '—',
        noSummary: 'Select a lead or send a new inbound message.',
        noLeads: 'No campaign leads yet.',
        noHandoffs: 'No handoffs yet.',
        leadId: 'lead_id',
        company: 'Company',
        role: 'Role',
        contact: 'Contact',
        useCase: 'Campaign need',
        clientType: 'Client type',
        campaignGoal: 'Campaign goal',
        platform: 'Platform',
        campaignIntelligence: 'Campaign Intelligence',
        recommendedMechanic: 'Best game for this campaign',
        mechanicName: 'Recommended game mechanic',
        mechanicReason: 'Why it fits',
        pricingTier: 'Pricing tier',
        qualificationStatus: 'Qualification status',
        missingFields: 'Missing fields',
        recommendedPackage: 'Recommended package',
        suggestedTier: 'Suggested tier',
        copyReadyFollowup: 'Copy-ready follow-up',
        copyFollowup: 'Copy follow-up',
        score: 'Score',
        priority: 'Priority',
        eventTimeline: 'Event timeline',
        noEvents: 'No events yet.',
        crmEvent: 'CRM event',
        handoffPackage: 'Campaign handoff package',
        followupPackage: 'Follow-up package',
        packageSummary: 'Summary',
        qualificationReason: 'Qualification reason',
        recommendedNextAction: 'Recommended next action',
        recommendedMechanicSection: 'Recommended game mechanic',
        crmPayloadPreview: 'CRM payload preview',
        exportCrm: 'Export to CRM',
        copyPackage: 'Copy package',
        handoffStatus: 'Handoff status',
        lifecycleReady: 'This lead is ready for handoff: CRM export, package copy, and move-to-work are available.',
        lifecycleActive: 'This handoff is already in work. A duplicate handoff will not be created.',
        lifecycleCompleted: 'This handoff is completed. CRM export is not offered again.',
        lifecycleFollowup: 'This lead needs follow-up. Only follow-up copy is available; CRM export is blocked.',
        ownerSection: 'Owner',
        team: 'Team',
        routingReason: 'Assignment reason',
        actionSection: 'Next action',
        actionStatus: 'Status',
        actionNext: 'Next action',
        actionReason: 'Reason',
        actionLabel: 'Action',
        actionContacted: 'Contact',
        actionWaitingReply: 'Waiting reply',
        actionClosed: 'Close action',
        actionStatus_new: 'New',
        actionStatus_contacted: 'Contacted',
        actionStatus_waiting_reply: 'Waiting reply',
        actionStatus_closed: 'Closed',
        assignTony: 'Assign Tony',
        assignSales: 'Assign Sales',
        assignSupport: 'Assign Support',
        assignedTo: 'Assigned to',
        lastSender: 'Last sender',
        lastIntent: 'Last intent',
        lastText: 'Last text',
        notAssigned: 'Unassigned',
        status_new: 'new',
        status_qualified: 'qualified',
        status_ready_to_handoff: 'ready for handoff',
        status_active_handoff: 'in progress',
        status_completed_handoff: 'completed',
        status_needs_followup: 'needs follow-up',
        status_needs_follow_up: 'needs follow-up',
        status_pending: 'ready for handoff',
        status_in_progress: 'in progress',
        status_done: 'done',
        status_completed: 'completed',
        status_unknown: 'unknown',
        moveToInProgress: 'Move to work',
        markDone: 'Complete handoff',
        open: 'Open',
        toastDemoLoaded: 'Examples loaded.',
        toastDemoReset: 'Data cleared.',
        toastMessageSent: 'Message processed.',
        toastSummaryLoaded: 'Lead summary loaded.',
        toastDashboardRefreshed: 'Dashboard refreshed.',
        toastLeadsRefreshed: 'Leads refreshed.',
        toastHandoffsRefreshed: 'Handoffs refreshed.',
        toastHandoffUpdated: 'Handoff updated.',
        toastCrmExported: 'CRM export prepared.',
        toastPackageCopied: 'Package copied.',
        toastFollowupCopied: 'Follow-up copied.',
        toastOwnerAssigned: 'Owner assigned.',
        toastActionUpdated: 'Action status updated.',
        toastError: 'Something went wrong.',
        polishedAssistantReply: 'Thanks. The campaign lead is qualified, the mechanic is recommended, and the handoff package is ready.',
      },
      es: {
        pageTitle: 'MechanicFlow AI',
        pageSubtitle: 'AI intake agent for gamified campaign leads, mechanic recommendation, qualification, CRM-ready handoff.',
        sendSectionTitle: 'Enviar mensaje',
        sendBtn: 'Enviar',
        clearBtn: 'Limpiar',
        sendHint: 'Prueba un ejemplo de campaña o envía una solicitud de una marca, eCommerce o agencia.',
        demoExamplesTitle: 'Campaign examples',
        demoExamples: [
          'We are Bloom Retail. Need a holiday promo game to collect emails and boost repeat purchases. Contact @bloom_growth',
          'We are UrbanFit. Need a spin-to-win campaign for Shopify lead capture. Contact @urbanfit_cmo',
          'We are FreshBox. Need a retention campaign with rewards for returning customers. Contact @freshbox_growth',
          'We are Nova Agency. Need a branded Advent Calendar campaign for a client. Contact @nova_agency',
          'We are GameLaunch Studio. Need a quiz lead magnet for a new product launch. Contact @gamelaunch_cmo',
        ],
        rawResponseSummary: 'Respuesta técnica',
        summarySectionTitle: 'Resumen del campaign lead',
        loadSummaryBtn: 'Cargar resumen',
        rawSummarySummary: 'JSON técnico del resumen',
        dashboardSectionTitle: 'Resumen del panel',
        refreshDashboardBtn: 'Actualizar panel',
        metricLeadsLabel: 'Campaign leads',
        metricQualifiedLabel: 'Calificados',
        metricInProgressLabel: 'En progreso',
        metricDoneLabel: 'Completados',
        rawDashboardSummary: 'JSON técnico del panel',
        leadsSectionTitle: 'Campaign leads recientes',
        refreshLeadsBtn: 'Actualizar',
        rawLeadsSummary: 'JSON técnico de leads',
        handoffsSectionTitle: 'Transferencias recientes',
        refreshHandoffsBtn: 'Actualizar',
        rawHandoffsSummary: 'JSON técnico de transferencias',
        loadDemoBtn: 'Cargar ejemplos',
        resetDemoBtn: 'Limpiar datos',
        footerText: 'MechanicFlow AI operational workspace for campaign lead qualification and handoff.',
        leadIdLabel: 'lead_id',
        leadIdHelp: 'Usa un lead_id existente solo si continúas una conversación activa.',
        messageLabel: 'Mensaje entrante',
        leadIdPlaceholder: 'Déjalo vacío para crear un nuevo lead',
        summaryLeadIdPlaceholder: 'Ingresa lead_id',
        messagePlaceholder: 'Ejemplo: We are UrbanFit. Need a spin-to-win campaign for Shopify lead capture. Contact @urbanfit_cmo',
        empty: '—',
        noSummary: 'Selecciona un lead o envía un nuevo mensaje entrante.',
        noLeads: 'Aún no hay leads de campaña.',
        noHandoffs: 'Aún no hay transferencias.',
        leadId: 'lead_id',
        company: 'Empresa',
        role: 'Rol',
        contact: 'Contacto',
        useCase: 'Necesidad de campaña',
        clientType: 'Tipo de cliente',
        campaignGoal: 'Objetivo de campaña',
        platform: 'Plataforma',
        campaignIntelligence: 'Campaign Intelligence',
        recommendedMechanic: 'Mejor juego para esta campaña',
        mechanicName: 'Mecánica de juego recomendada',
        mechanicReason: 'Por qué encaja',
        pricingTier: 'Plan',
        qualificationStatus: 'Estado de calificación',
        missingFields: 'Campos faltantes',
        recommendedPackage: 'Paquete recomendado',
        suggestedTier: 'Plan sugerido',
        copyReadyFollowup: 'Copy-ready follow-up',
        copyFollowup: 'Copy follow-up',
        score: 'Puntuación',
        priority: 'Prioridad',
        eventTimeline: 'Historial de eventos',
        noEvents: 'Aún no hay eventos.',
        crmEvent: 'Evento CRM',
        handoffPackage: 'Campaign handoff package',
        followupPackage: 'Follow-up package',
        packageSummary: 'Resumen',
        qualificationReason: 'Razón de calificación',
        recommendedNextAction: 'Siguiente acción',
        recommendedMechanicSection: 'Recommended game mechanic',
        crmPayloadPreview: 'Vista previa de CRM payload',
        exportCrm: 'Exportar a CRM',
        copyPackage: 'Copiar paquete',
        handoffStatus: 'Estado de transferencia',
        lifecycleReady: 'Este lead está listo para transferencia: CRM export, copia del paquete y mover a trabajo están disponibles.',
        lifecycleActive: 'Esta transferencia ya está en trabajo. No se creará una transferencia duplicada.',
        lifecycleCompleted: 'Esta transferencia está completada. CRM export no se ofrece de nuevo.',
        lifecycleFollowup: 'Este lead requiere seguimiento. Solo está disponible el follow-up; CRM export está bloqueado.',
        ownerSection: 'Responsable',
        team: 'Equipo',
        routingReason: 'Razón de asignación',
        actionSection: 'Siguiente acción',
        actionStatus: 'Estado',
        actionNext: 'Siguiente acción',
        actionReason: 'Razón',
        actionLabel: 'Acción',
        actionContacted: 'Contactar',
        actionWaitingReply: 'Esperando respuesta',
        actionClosed: 'Cerrar acción',
        actionStatus_new: 'Nueva',
        actionStatus_contacted: 'Contactado',
        actionStatus_waiting_reply: 'Esperando respuesta',
        actionStatus_closed: 'Cerrada',
        assignTony: 'Asignar Tony',
        assignSales: 'Asignar Sales',
        assignSupport: 'Asignar Support',
        assignedTo: 'Asignado a',
        lastSender: 'Último remitente',
        lastIntent: 'Última intención',
        lastText: 'Último texto',
        notAssigned: 'Sin asignar',
        status_new: 'nuevo',
        status_qualified: 'calificado',
        status_ready_to_handoff: 'listo para transferencia',
        status_active_handoff: 'en progreso',
        status_completed_handoff: 'completado',
        status_needs_followup: 'requiere seguimiento',
        status_needs_follow_up: 'requiere seguimiento',
        status_pending: 'listo para transferencia',
        status_in_progress: 'en progreso',
        status_done: 'completado',
        status_completed: 'completado',
        status_unknown: 'desconocido',
        moveToInProgress: 'Mover a trabajo',
        markDone: 'Completar transferencia',
        open: 'Abrir',
        toastDemoLoaded: 'Ejemplos cargados.',
        toastDemoReset: 'Datos limpiados.',
        toastMessageSent: 'Mensaje procesado.',
        toastSummaryLoaded: 'Resumen del lead cargado.',
        toastDashboardRefreshed: 'Panel actualizado.',
        toastLeadsRefreshed: 'Leads actualizados.',
        toastHandoffsRefreshed: 'Transferencias actualizadas.',
        toastHandoffUpdated: 'Transferencia actualizada.',
        toastCrmExported: 'CRM export preparado.',
        toastPackageCopied: 'Paquete copiado.',
        toastFollowupCopied: 'Follow-up copiado.',
        toastOwnerAssigned: 'Responsable asignado.',
        toastActionUpdated: 'Estado de acción actualizado.',
        toastError: 'Algo salió mal.',
        polishedAssistantReply: 'Gracias. El campaign lead quedó calificado, la mecánica fue recomendada y el paquete está listo.',
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

    function displayValue(value) {
      if (value === null || value === undefined || value === '') return '—';
      return String(value);
    }

    function displayList(value) {
      if (!value) return '—';
      if (Array.isArray(value)) return value.length ? value.join(', ') : '—';
      return String(value);
    }

    function renderDemoExamples() {
      const root = $('demoExamples');
      if (!root) return;

      const examples = Array.isArray(t('demoExamples')) ? t('demoExamples') : [];
      root.innerHTML = '';
      examples.forEach((example) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'example-pill';
        btn.textContent = example;
        btn.onclick = () => {
          $('messageInput').value = example;
          $('messageInput').focus();
        };
        root.appendChild(btn);
      });
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
      $('demoExamplesTitle').textContent = t('demoExamplesTitle');
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

      $('leadIdLabel').textContent = t('leadIdLabel');
      $('leadIdHelp').textContent = t('leadIdHelp');
      $('messageLabel').textContent = t('messageLabel');
      $('leadIdInput').placeholder = t('leadIdPlaceholder');
      $('summaryLeadIdInput').placeholder = t('summaryLeadIdPlaceholder');
      $('messageInput').placeholder = t('messagePlaceholder');

      if (['(пусто)', '(empty)', '(vacío)', '—'].includes($('sendResult').textContent)) $('sendResult').textContent = t('empty');
      if (['(пусто)', '(empty)', '(vacío)', '—'].includes($('summaryResult').textContent)) $('summaryResult').textContent = t('empty');
      if (['(пусто)', '(empty)', '(vacío)', '—'].includes($('dashboardResult').textContent)) $('dashboardResult').textContent = t('empty');
      if (['(пусто)', '(empty)', '(vacío)', '—'].includes($('leadsRaw').textContent)) $('leadsRaw').textContent = t('empty');
      if (['(пусто)', '(empty)', '(vacío)', '—'].includes($('handoffsRaw').textContent)) $('handoffsRaw').textContent = t('empty');

      renderSummary(lastSummary);
      renderDashboard(lastDashboard);
      renderLeads(lastLeads);
      renderHandoffs(lastHandoffs);
      renderDemoExamples();
    }

    function mapStatus(status) {
      const normalized = normalizeHandoffStatus(status);
      if (!normalized) return t('status_unknown');
      const key = `status_${normalized}`;
      return t(key);
    }

    function mapActionStatus(status, fallback='') {
      const normalized = String(status || '').toLowerCase();
      if (!normalized) return displayValue(fallback);
      const key = `actionStatus_${normalized}`;
      const translated = t(key);
      return translated === key ? displayValue(fallback || status) : translated;
    }

    function badgeClass(status) {
      const s = normalizeHandoffStatus(status);
      if (['qualified', 'ready_to_handoff', 'completed_handoff'].includes(s)) return 'badge-green';
      if (['pending', 'needs_followup', 'needs_follow_up'].includes(s)) return 'badge-orange';
      if (['active_handoff'].includes(s)) return 'badge-graphite';
      return 'badge-gray';
    }

    function normalizeHandoffStatus(status) {
      const value = String(status || '').toLowerCase();
      if (value === 'in_progress') return 'active_handoff';
      if (value === 'done' || value === 'completed') return 'completed_handoff';
      if (value === 'needs_followup') return 'needs_follow_up';
      return value;
    }

    function getHandoffStatus(item) {
      return normalizeHandoffStatus(
        item?.handoff_status ||
        item?.handoff?.handoff_status ||
        item?.handoff?.status ||
        (item?.reason !== undefined || item?.assigned_to !== undefined ? item?.status : null) ||
        null
      );
    }

    function lifecycleText(status, hasMissingFields=false) {
      const normalized = normalizeHandoffStatus(status);
      if (hasMissingFields || normalized === 'needs_follow_up') return t('lifecycleFollowup');
      if (normalized === 'ready_to_handoff' || normalized === 'pending') return t('lifecycleReady');
      if (normalized === 'active_handoff') return t('lifecycleActive');
      if (normalized === 'completed_handoff') return t('lifecycleCompleted');
      return '';
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

    function formatEventPayload(payload) {
      if (!payload) return '';

      let text = '';
      if (typeof payload === 'string') {
        text = payload;
      } else {
        text = Object.entries(payload)
          .filter(([, value]) => value !== null && value !== undefined && value !== '')
          .map(([key, value]) => `${key}: ${value}`)
          .join(' · ');
      }

      return text.length > 140 ? `${text.slice(0, 137)}...` : text;
    }

    function normalizeSummaryForDisplay(summary) {
      if (!summary || !summary.lead) return summary;

      const clone = JSON.parse(JSON.stringify(summary));
      const handoff = clone.handoff || {};
      const conversation = clone.conversation || {};

      if (!handoff.assigned_to) {
        handoff.assigned_to = t('notAssigned');
      }

      conversation.last_text = prettyAssistantText(conversation.last_text, conversation.last_sender);

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
        const errText = data && data.detail ? JSON.stringify(data.detail) : text || res.statusText;
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
      const handoffPackage = data.handoff_package || null;
      const ownerRouting = data.owner_routing || handoffPackage || {};
      const actionQueue = data.action_queue || {
        status: handoffPackage?.action_status || 'new',
        label: handoffPackage?.action_status || 'new',
        next_action: handoffPackage?.next_action || '',
        reason: '',
        owner: ownerRouting.owner,
        team: ownerRouting.team,
      };
      const actionStatus = actionQueue.status || 'new';

      const effectiveHandoffStatus = getHandoffStatus({ handoff });
      const qualificationStatus = normalizeHandoffStatus(
        handoffPackage?.qualification_status || lead.qualification_status || lead.lead_status
      );
      const missingFields = handoffPackage?.missing_fields || lead.missing_fields || [];
      const hasMissingFields = Array.isArray(missingFields)
        ? missingFields.length > 0
        : Boolean(missingFields);
      const isReadyPackage = handoffPackage
        && ['ready_to_handoff', 'active_handoff', 'completed_handoff'].includes(qualificationStatus)
        && !hasMissingFields;
      const isFollowupPackage = handoffPackage
        && (qualificationStatus === 'needs_follow_up' || hasMissingFields);
      const lifecycleStatus = effectiveHandoffStatus || qualificationStatus || lead.lead_status;

      const wrap = document.createElement('div');
      wrap.className = 'summary-box';

      const badges = document.createElement('div');
      badges.className = 'badges';
      badges.innerHTML = `
        <span class="badge badge-id">lead_id: ${lead.id ?? '-'}</span>
        <span class="badge ${badgeClass(lead.lead_status)}">${mapStatus(lead.lead_status)}</span>
        ${effectiveHandoffStatus && !isFollowupPackage ? `<span class="badge ${badgeClass(effectiveHandoffStatus)}">${mapStatus(effectiveHandoffStatus)}</span>` : ''}
      `;
      wrap.appendChild(badges);

      const rows = [
        [t('leadId'), lead.id ?? t('empty')],
        [t('qualificationStatus'), mapStatus(qualificationStatus)],
        [t('handoffStatus'), mapStatus(lifecycleStatus)],
        [t('score'), data.score ?? t('empty')],
        [t('priority'), data.priority || t('empty')],
        [t('missingFields'), displayList(missingFields)],
        [t('company'), lead.company || t('empty')],
        [t('role'), lead.role || t('empty')],
        [t('contact'), lead.contact || t('empty')],
        [t('useCase'), lead.use_case || t('empty')],
        [t('clientType'), handoffPackage?.client_type || lead.client_type || t('empty')],
        [t('campaignGoal'), handoffPackage?.campaign_goal || lead.campaign_goal || t('empty')],
        [t('platform'), handoffPackage?.platform || lead.platform || t('empty')],
        [t('recommendedMechanic'), handoffPackage?.recommended_mechanic || lead.recommended_mechanic || t('empty')],
        [t('mechanicReason'), handoffPackage?.mechanic_reason || lead.mechanic_reason || t('empty')],
        [t('pricingTier'), handoffPackage?.pricing_tier || lead.pricing_tier || t('empty')],
        [t('recommendedNextAction'), handoffPackage?.recommended_next_action || lead.recommended_next_action || t('empty')],
        [t('assignedTo'), ownerRouting.owner && ownerRouting.owner !== 'Unassigned' ? ownerRouting.owner : t('notAssigned')],
        [t('team'), ownerRouting.team || t('empty')],
      ];

      rows.forEach(([k, v]) => {
        const row = document.createElement('div');
        row.className = 'kv';
        row.innerHTML = `<div class="k">${k}:</div><div class="v">${v}</div>`;
        wrap.appendChild(row);
      });

      const ownerBox = document.createElement('div');
      ownerBox.className = 'list-item';
      ownerBox.innerHTML = `
        <div class="list-title">${t('ownerSection')}</div>
        <div class="list-sub">${t('assignedTo')}: ${displayValue(ownerRouting.owner)}</div>
        <div class="list-sub">${t('team')}: ${displayValue(ownerRouting.team)}</div>
        <div class="list-sub">${t('routingReason')}: ${displayValue(ownerRouting.reason || ownerRouting.routing_reason)}</div>
        ${handoff.id && !isFollowupPackage ? `
          <div class="list-actions">
            <button class="btn btn-gray assign-owner-btn" data-owner="Tony" data-team="Sales">${t('assignTony')}</button>
            <button class="btn btn-gray assign-owner-btn" data-owner="Sales Manager" data-team="Sales">${t('assignSales')}</button>
            <button class="btn btn-gray assign-owner-btn" data-owner="Support Lead" data-team="Customer Success">${t('assignSupport')}</button>
          </div>
        ` : ''}
      `;
      wrap.appendChild(ownerBox);

      if (handoffPackage) {
        const mechanicBox = document.createElement('div');
        mechanicBox.className = 'list-item';
        mechanicBox.innerHTML = `
          <div class="list-title">${t('campaignIntelligence')}</div>
          <div class="list-sub">${t('clientType')}: ${displayValue(handoffPackage.client_type)}</div>
          <div class="list-sub">${t('campaignGoal')}: ${displayValue(handoffPackage.campaign_goal)}</div>
          <div class="list-sub">${t('platform')}: ${displayValue(handoffPackage.platform)}</div>
          <div class="list-sub">${t('mechanicName')}: ${displayValue(handoffPackage.recommended_mechanic)}</div>
          <div class="list-sub">${t('mechanicReason')}: ${displayValue(handoffPackage.mechanic_reason || handoffPackage.recommended_mechanic_reason)}</div>
          <div class="list-sub">${t('suggestedTier')}: ${displayValue(handoffPackage.pricing_tier)}</div>
          <div class="list-sub">${t('qualificationStatus')}: ${mapStatus(handoffPackage.qualification_status)}</div>
          <div class="list-sub">${t('missingFields')}: ${displayList(missingFields)}</div>
          <div class="list-sub">${t('recommendedNextAction')}: ${displayValue(handoffPackage.recommended_next_action)}</div>
          <div class="list-sub"><strong>${t('copyReadyFollowup')}:</strong> ${displayValue(handoffPackage.copy_text)}</div>
        `;
        wrap.appendChild(mechanicBox);
      }

      const actionButtons = [];
      if (handoff.id && actionStatus === 'new') {
        actionButtons.push(`<button class="btn btn-action action-status-btn" data-action-status="contacted">${t('actionContacted')}</button>`);
      } else if (handoff.id && actionStatus === 'contacted') {
        actionButtons.push(`<button class="btn btn-gray action-status-btn" data-action-status="waiting_reply">${t('actionWaitingReply')}</button>`);
        actionButtons.push(`<button class="btn btn-green action-status-btn" data-action-status="closed">${t('actionClosed')}</button>`);
      } else if (handoff.id && actionStatus === 'waiting_reply') {
        actionButtons.push(`<button class="btn btn-green action-status-btn" data-action-status="closed">${t('actionClosed')}</button>`);
      }

      const actionBox = document.createElement('div');
      actionBox.className = 'list-item';
      actionBox.innerHTML = `
        <div class="list-title">${t('actionSection')}</div>
        <div class="list-sub">${t('actionStatus')}: ${mapActionStatus(actionQueue.status, actionQueue.label)}</div>
        <div class="list-sub">${t('actionNext')}: ${displayValue(actionQueue.next_action)}</div>
        <div class="list-sub">${t('actionReason')}: ${displayValue(actionQueue.reason)}</div>
        <div class="list-sub">${t('assignedTo')}: ${displayValue(actionQueue.owner || ownerRouting.owner)}</div>
        <div class="list-sub">${t('team')}: ${displayValue(actionQueue.team || ownerRouting.team)}</div>
        ${actionButtons.length ? `<div class="list-actions">${actionButtons.join('')}</div>` : ''}
      `;
      if (handoff.id && !isFollowupPackage) {
        wrap.appendChild(actionBox);
      }

      if (isReadyPackage) {
        const payload = handoffPackage.crm_payload || {};
        const packageBox = document.createElement('div');
        packageBox.className = 'list-item';
        const packageActions = [];
        const copyPackageAction = (handoffPackage.package_copy_text || handoffPackage.copy_text)
          ? `<button class="btn btn-gray" id="copyPackageBtn">${t('copyPackage')}</button>`
          : '';

        if (qualificationStatus === 'ready_to_handoff' && handoff.id) {
          packageActions.push(`<button class="btn btn-action" id="exportCrmBtn">${t('exportCrm')}</button>`);
          if (copyPackageAction) packageActions.push(copyPackageAction);
          packageActions.push(`<button class="btn btn-gray" id="setInProgressBtn">${t('moveToInProgress')}</button>`);
        } else if (qualificationStatus === 'active_handoff' && handoff.id) {
          packageActions.push(`<button class="btn btn-green" id="setDoneBtn">${t('markDone')}</button>`);
          if (copyPackageAction) packageActions.push(copyPackageAction);
        } else if (copyPackageAction) {
          packageActions.push(copyPackageAction);
        }

        const payloadRows = [
          [t('company'), payload.company],
          [t('contact'), payload.contact],
          [t('role'), payload.role],
          [t('clientType'), payload.client_type],
          [t('campaignGoal'), payload.campaign_goal],
          [t('platform'), payload.platform],
          [t('useCase'), payload.campaign_need || payload.use_case],
          [t('recommendedMechanic'), payload.recommended_mechanic],
          [t('pricingTier'), payload.pricing_tier],
          [t('qualificationStatus'), mapStatus(payload.qualification_status)],
          [t('score'), payload.score],
          [t('priority'), payload.priority],
          [t('assignedTo'), payload.owner],
          [t('team'), payload.team],
          [t('actionNext'), payload.next_action],
          ['handoff_id', payload.handoff_id],
          ['created_at', payload.created_at],
        ];

        packageBox.innerHTML = `
          <div class="list-title">${t('handoffPackage')}</div>
          <div class="lifecycle-note">${lifecycleText(lifecycleStatus, hasMissingFields)}</div>
          <div class="list-sub"><strong>${t('packageSummary')}:</strong> ${displayValue(handoffPackage.summary)}</div>
          <div class="list-sub"><strong>${t('qualificationReason')}:</strong> ${displayValue(handoffPackage.qualification_reason)}</div>
          <div class="list-sub"><strong>${t('recommendedNextAction')}:</strong> ${displayValue(handoffPackage.recommended_next_action)}</div>
          <div class="list-sub"><strong>${t('crmPayloadPreview')}:</strong></div>
          ${payloadRows.map(([label, value]) => `<div class="list-sub">${label}: ${displayValue(value)}</div>`).join('')}
          ${packageActions.length ? `<div class="list-actions">${packageActions.join('')}</div>` : ''}
        `;
        wrap.appendChild(packageBox);
      } else if (isFollowupPackage) {
        const followupBox = document.createElement('div');
        followupBox.className = 'list-item';
        followupBox.innerHTML = `
          <div class="list-title">${t('followupPackage')}</div>
          <div class="lifecycle-note">${lifecycleText(lifecycleStatus, hasMissingFields)}</div>
          <div class="list-sub"><strong>${t('missingFields')}:</strong> ${displayList(missingFields)}</div>
          <div class="list-sub"><strong>${t('recommendedNextAction')}:</strong> ${displayValue(handoffPackage.next_question || handoffPackage.recommended_next_action)}</div>
          <div class="list-sub"><strong>${t('copyReadyFollowup')}:</strong> ${displayValue(handoffPackage.copy_text)}</div>
          ${handoffPackage.copy_text ? `<div class="list-actions"><button class="btn btn-gray" id="copyFollowupBtn">${t('copyFollowup')}</button></div>` : ''}
        `;
        wrap.appendChild(followupBox);
      }

      const events = Array.isArray(data.events) ? data.events.slice(0, 8) : [];
      const timeline = document.createElement('div');
      timeline.className = 'list-item';

      const timelineTitle = document.createElement('div');
      timelineTitle.className = 'list-title';
      timelineTitle.textContent = t('eventTimeline');
      timeline.appendChild(timelineTitle);

      if (!events.length) {
        const emptyEvent = document.createElement('div');
        emptyEvent.className = 'list-sub';
        emptyEvent.textContent = t('noEvents');
        timeline.appendChild(emptyEvent);
      } else {
        events.forEach((event) => {
          const row = document.createElement('div');
          const details = event.details || '';
          row.className = 'list-sub';
          row.textContent = [
            event.label || t('crmEvent'),
            details,
            event.created_at || '',
          ].filter(Boolean).join(' · ');
          timeline.appendChild(row);
        });
      }

      wrap.appendChild(timeline);

      box.appendChild(wrap);

      const leadId = lead.id;
      document.querySelectorAll('.assign-owner-btn').forEach(btn => {
        btn.onclick = async () => {
          if (!leadId) return;
          await assignOwner(leadId, btn.dataset.owner, btn.dataset.team);
        };
      });

      document.querySelectorAll('.action-status-btn').forEach(btn => {
        btn.onclick = async () => {
          if (!leadId) return;
          await updateActionStatus(leadId, btn.dataset.actionStatus);
        };
      });

      const exportCrmBtn = $('exportCrmBtn');
      if (exportCrmBtn) exportCrmBtn.onclick = async () => {
        if (!leadId) return;
        await exportCrm(leadId);
      };

      const copyPackageBtn = $('copyPackageBtn');
      if (copyPackageBtn) copyPackageBtn.onclick = async () => {
        await copyHandoffPackage(handoffPackage.package_copy_text || handoffPackage.copy_text);
      };

      const copyFollowupBtn = $('copyFollowupBtn');
      if (copyFollowupBtn) copyFollowupBtn.onclick = async () => {
        await copyHandoffPackage(handoffPackage.copy_text, t('toastFollowupCopied'));
      };

      const setInProgressBtn = $('setInProgressBtn');
      if (setInProgressBtn) setInProgressBtn.onclick = async () => {
        if (!leadId) return;
        await tryHandoffAction(leadId, 'in_progress');
      };

      const setDoneBtn = $('setDoneBtn');
      if (setDoneBtn) setDoneBtn.onclick = async () => {
        if (!leadId) return;
        await tryHandoffAction(leadId, 'done');
      };
    }

    function renderDashboard(data) {
  lastDashboard = data;

  const leadsFromList = Array.isArray(lastLeads) ? lastLeads.length : 0;
  const qualifiedFromList = Array.isArray(lastLeads)
    ? lastLeads.filter(item => {
        const status = normalizeHandoffStatus(
          item.qualification_status ?? item.lead_status ?? item.status ?? item.lead?.lead_status
        );
        return status === 'ready_to_handoff';
      }).length
    : 0;

  const inProgressFromList = Array.isArray(lastHandoffs)
    ? lastHandoffs.filter(item => {
        const status = getHandoffStatus(item);
        return status === 'active_handoff';
      }).length
    : 0;

  const doneFromList = Array.isArray(lastHandoffs)
    ? lastHandoffs.filter(item => {
        const status = getHandoffStatus(item);
        return status === 'completed_handoff';
      }).length
    : 0;

  let leadsTotal =
    data?.leads_total ??
    data?.total_leads ??
    data?.leads?.total ??
    data?.counts?.leads_total ??
    data?.counts?.total_leads ??
    data?.summary?.leads_total ??
    0;

  let qualifiedTotal =
    data?.qualified_total ??
    data?.qualified_leads ??
    data?.leads?.qualified ??
    data?.counts?.qualified_total ??
    data?.counts?.qualified_leads ??
    data?.summary?.qualified_total ??
    0;

  let inProgress =
    data?.handoffs_in_progress ??
    data?.in_progress ??
    data?.handoffs?.in_progress ??
    data?.counts?.handoffs_in_progress ??
    data?.summary?.handoffs_in_progress ??
    0;

  let done =
    data?.handoffs_done ??
    data?.handoffs?.done ??
    data?.handoffs_completed ??
    data?.counts?.handoffs_done ??
    data?.counts?.handoffs_completed ??
    data?.summary?.handoffs_done ??
    0;

  if (leadsTotal === 0 && leadsFromList > 0) leadsTotal = leadsFromList;
  if (qualifiedTotal === 0 && qualifiedFromList > 0) qualifiedTotal = qualifiedFromList;
  if (inProgress === 0 && inProgressFromList > 0) inProgress = inProgressFromList;
  if (done === 0 && doneFromList > 0) done = doneFromList;

  $('metricLeads').textContent = leadsTotal;
  $('metricQualified').textContent = qualifiedTotal;
  $('metricInProgress').textContent = inProgress;
  $('metricDone').textContent = done;
  $('dashboardResult').textContent = data ? safeJson(data) : t('empty');
	}
	
    function calculateLeadScore(item) {
	      const lead = item.lead || item || {};
	      if (item.score !== undefined && item.score !== null) return Number(item.score) || 0;
	      if (lead.score !== undefined && lead.score !== null) return Number(lead.score) || 0;
	      let score = 0;
	
	      if (lead.company || item.company) score += 25;
	      if (lead.contact || item.contact) score += 25;
	      if (lead.use_case || item.use_case) score += 25;
	      if (lead.role || item.role) score += 10;
	
	      const status = lead.lead_status || lead.status || item.lead_status || item.status || '';
	      if (['qualified', 'ready_to_handoff', 'active_handoff', 'completed_handoff'].includes(normalizeHandoffStatus(status))) score += 15;
	
	      return Math.min(score, 100);
	    }
	
	    function calculateLeadPriority(score) {
	      if (score >= 75) return 'High';
	      if (score >= 40) return 'Medium';
	      return 'Low';
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
        const leadId = item.id ?? item.lead_id ?? item.lead?.id ?? '-';
        const company = item.company ?? item.lead?.company ?? item.name ?? item.contact ?? ('lead_id ' + leadId);
	        const role = item.role ?? item.lead?.role ?? t('empty');
	        const contact = item.contact ?? item.lead?.contact ?? t('empty');
		        const useCase = item.use_case ?? item.lead?.use_case ?? t('empty');
		        const score = calculateLeadScore(item);
		        const priority = item.priority || item.lead?.priority || calculateLeadPriority(score);
		        const mechanic = item.recommended_mechanic ?? item.handoff_package?.recommended_mechanic ?? t('empty');
		        const actionQueue = item.action_queue || {};
		        const actionText = mapActionStatus(
		          actionQueue.status || item.action_status,
		          actionQueue.label || item.action_label
		        );
		
			        let leadStatus = item.qualification_status ?? item.lead_status ?? item.status ?? item.lead?.lead_status ?? null;
			        const handoffStatus = getHandoffStatus(item);
		        if (!leadStatus) leadStatus = handoffStatus || 'new';

        const el = document.createElement('div');
        el.className = 'list-item';
        el.innerHTML = `
	          <div class="list-top">
	            <div>
		              <div class="list-title">${company}</div>
		              <div class="list-sub">${t('score')}: ${score} · ${t('priority')}: ${priority}</div>
		              <div class="list-sub">${t('recommendedMechanic')}: ${mechanic}</div>
		              <div class="list-sub">${t('actionLabel')}: ${actionText}</div>
		              <div class="list-sub">${t('role')}: ${role} · ${t('contact')}: ${contact}</div>
		            </div>
	            <div class="badges">
	              <span class="badge badge-id">lead_id: ${leadId}</span>
	              <span class="badge ${badgeClass(leadStatus)}">${mapStatus(leadStatus)}</span>
	              ${handoffStatus ? `<span class="badge ${badgeClass(handoffStatus)}">${mapStatus(handoffStatus)}</span>` : ''}
	            </div>
          </div>
          <div class="list-sub">${useCase}</div>
          <div class="list-actions">
            <button class="btn btn-action open-lead-btn" data-lead-id="${leadId}">${t('open')}</button>
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
        const leadId = item.lead_id ?? item.id ?? '-';
	        const assigned = item.assigned_to || t('notAssigned');
	        const status = getHandoffStatus(item) || 'pending';
	        const reason = item.reason || item.notes || t('empty');
	        const actionQueue = item.action_queue || {};
	        const actionText = mapActionStatus(
	          actionQueue.status || item.action_status,
	          actionQueue.label || item.action_label
	        );

	        const el = document.createElement('div');
        el.className = 'list-item';
        el.innerHTML = `
          <div class="list-top">
	            <div>
	              <div class="list-title">lead_id ${leadId}</div>
	              <div class="list-sub">${t('assignedTo')}: ${assigned}</div>
	              <div class="list-sub">${t('actionLabel')}: ${actionText}</div>
	            </div>
            <div class="badges">
              <span class="badge badge-id">lead_id: ${leadId}</span>
              <span class="badge ${badgeClass(status)}">${mapStatus(status)}</span>
            </div>
          </div>
          <div class="list-sub">${reason}</div>
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
          await refreshAll(false);
          await loadSummary(String(leadId), false);
          return;
        } catch (_) {}
      }

      showToast(t('toastError'), 'error');
    }

    async function updateActionStatus(leadId, actionStatus) {
      const paths = {
        contacted: 'contacted',
        waiting_reply: 'waiting-reply',
        closed: 'closed',
      };
      const path = paths[actionStatus];
      if (!path) {
        showToast(t('toastError'), 'error');
        return;
      }

      try {
        await fetchJSON(`/handoffs/${leadId}/action/${path}`, { method: 'POST' });
        showToast(t('toastActionUpdated'));
        await refreshAll(false);
        await loadSummary(String(leadId), false);
      } catch (e) {
        showToast(String(e.message || t('toastError')), 'error');
      }
    }

    async function exportCrm(leadId) {
      try {
        await fetchJSON(`/handoffs/${leadId}/export-crm`, { method: 'POST' });
        showToast(t('toastCrmExported'));
        await refreshAll(false);
        await loadSummary(String(leadId), false);
      } catch (e) {
        showToast(String(e.message || t('toastError')), 'error');
      }
    }

    async function assignOwner(leadId, owner, team) {
      try {
        await fetchJSON(`/handoffs/${leadId}/assign`, {
          method: 'POST',
          body: JSON.stringify({ owner, team })
        });
        showToast(t('toastOwnerAssigned'));
        await refreshAll(false);
        await loadSummary(String(leadId), false);
      } catch (e) {
        showToast(String(e.message || t('toastError')), 'error');
      }
    }

    async function copyHandoffPackage(text, toastMessage=null) {
      if (!text) return;

      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(text);
        } else {
          const area = document.createElement('textarea');
          area.value = text;
          area.style.position = 'fixed';
          area.style.opacity = '0';
          document.body.appendChild(area);
          area.focus();
          area.select();
          document.execCommand('copy');
          area.remove();
        }
        showToast(toastMessage || t('toastPackageCopied'));
      } catch (e) {
        showToast(String(e.message || t('toastError')), 'error');
      }
    }

    async function sendMessage() {
      const leadId = $('leadIdInput').value.trim();
      const messageText = $('messageInput').value.trim();

      if (!messageText) {
        showToast(t('toastError'), 'error');
        return;
      }

      const payload = { message: messageText };
      if (leadId) payload.lead_id = Number(leadId);

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
        renderDashboard(lastDashboard);
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
        renderDashboard(lastDashboard);
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
