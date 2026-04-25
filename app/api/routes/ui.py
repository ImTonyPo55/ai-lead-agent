from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["ui"])


@router.get("/ui", response_class=HTMLResponse)
def ui_page() -> str:
    return """
<!doctype html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Lead Agent UI</title>
  <style>
    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #0f172a;
      color: #e2e8f0;
    }

    .wrap {
      max-width: 1440px;
      margin: 0 auto;
      padding: 20px;
    }

    h1, h2, h3 {
      margin: 0 0 12px 0;
    }

    .muted {
      color: #94a3b8;
      font-size: 13px;
      margin-bottom: 18px;
    }

    .grid {
      display: grid;
      grid-template-columns: 1.15fr 1fr;
      gap: 16px;
    }

    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-top: 16px;
    }

    .grid-4 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-top: 12px;
    }

    .card {
      background: #111827;
      border: 1px solid #334155;
      border-radius: 14px;
      padding: 16px;
      box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    }

    .metric {
      background: #0b1220;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 14px;
      min-height: 86px;
    }

    .metric-title {
      color: #94a3b8;
      font-size: 12px;
      margin-bottom: 8px;
    }

    .metric-value {
      font-size: 24px;
      font-weight: 700;
    }

    input, textarea, button {
      width: 100%;
      margin-top: 8px;
      margin-bottom: 12px;
      padding: 11px 12px;
      border-radius: 10px;
      border: 1px solid #475569;
      background: #0b1220;
      color: #e2e8f0;
      font-size: 14px;
    }

    textarea {
      min-height: 110px;
      resize: vertical;
    }

    button {
      background: #2563eb;
      border: none;
      cursor: pointer;
      font-weight: 700;
    }

    button:hover {
      background: #1d4ed8;
    }

    .secondary-btn {
      background: #1e293b;
    }

    .secondary-btn:hover {
      background: #334155;
    }

    .success-btn {
      background: #15803d;
    }

    .success-btn:hover {
      background: #166534;
    }

    .warn-btn {
      background: #b45309;
    }

    .warn-btn:hover {
      background: #92400e;
    }

    .danger-btn {
      background: #991b1b;
    }

    .danger-btn:hover {
      background: #7f1d1d;
    }

    .small-btn {
      width: auto;
      margin: 0;
      padding: 6px 10px;
      font-size: 12px;
      border-radius: 8px;
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

    .pill {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      background: #1e293b;
      color: #e2e8f0;
      margin-right: 8px;
      margin-bottom: 8px;
    }

    .ok { background: #14532d; }
    .warn { background: #78350f; }
    .info { background: #1e3a8a; }

    .summary-line {
      margin-bottom: 8px;
      color: #e2e8f0;
    }

    .table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 8px;
      font-size: 13px;
    }

    .table th, .table td {
      border-bottom: 1px solid #334155;
      padding: 10px 8px;
      text-align: left;
      vertical-align: top;
    }

    .table th {
      color: #94a3b8;
      font-weight: 700;
    }

    .empty {
      color: #94a3b8;
      padding: 12px 0;
    }

    .section-title {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .activity-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 8px;
    }

    .activity-item {
      border: 1px solid #334155;
      background: #0b1220;
      border-radius: 10px;
      padding: 10px 12px;
      font-size: 13px;
    }

    .activity-time {
      color: #94a3b8;
      font-size: 12px;
      margin-bottom: 4px;
    }

    .activity-ok { border-color: #14532d; }
    .activity-warn { border-color: #78350f; }
    .activity-info { border-color: #1e3a8a; }

    details {
      margin-top: 12px;
      border: 1px solid #334155;
      border-radius: 10px;
      background: #020617;
      overflow: hidden;
    }

    summary {
      cursor: pointer;
      padding: 10px 12px;
      color: #cbd5e1;
      font-size: 13px;
      font-weight: 700;
      list-style: none;
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

    .hint {
  display: block;
  padding-top: 16px;
  font-size: 13px;
  color: #94a3b8;
  line-height: 1.4;
}

    @media (max-width: 980px) {
      .grid, .grid-2, .grid-4 {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="section-title">
      <div>
 <h1>AI Lead Agent</h1>
<div class="muted">Demo-ready MVP for inbound B2B lead intake, qualification, and handoff.</div>
</div>
<div class="top-actions">
  <button class="success-btn" onclick="seedDemo()">Load demo data</button>
  <button class="danger-btn" onclick="resetDemo()">Reset demo</button>
</div>
</div>
    <div class="grid">
      <div class="card">
     <h2>Send message</h2>
<input id="leadIdInput" placeholder="lead_id — optional for the first message" />
<textarea id="messageInput" placeholder="Enter inbound message..."></textarea>
<div class="top-actions">
  <button onclick="sendMessage()">Send</button>
  <button class="secondary-btn" onclick="clearMessageForm()">Clear</button>
</div>
<div class="hint">After the reply, lead_id will be automatically filled into summary.</div>

<details>
  <summary>Raw response</summary>
  <pre id="sendResult">Empty.</pre>
</details> 
        
      </div>

      <div class="card" id="summaryCard">
        <h2>Lead summary</h2>
        <input id="summaryLeadId" placeholder="Enter lead_id" />
        <div class="top-actions">
          <button onclick="loadLeadSummary()">Load summary</button>
        </div>

        <div id="summaryCards" class="empty">Empty.</div>
        <div id="summaryActions" class="top-actions"></div>

        <details>
          <summary>Raw summary JSON</summary>
          <pre id="summaryResult">Empty.</pre>
        </details>
      </div>
    </div>

    <div class="card" style="margin-top:16px;">
      <div class="section-title">
        <h2>Dashboard overview</h2>
        <div class="top-actions">
          <button onclick="loadDashboard(true)">Обновить dashboard</button>
        </div>
      </div>

      <div class="grid-4">
        <div class="metric">
          <div class="metric-title">Leads total</div>
          <div class="metric-value" id="metricLeadsTotal">—</div>
        </div>
        <div class="metric">
          <div class="metric-title">Qualified</div>
          <div class="metric-value" id="metricLeadsQualified">—</div>
        </div>
        <div class="metric">
          <div class="metric-title">Handoffs in progress</div>
          <div class="metric-value" id="metricHandoffsProgress">—</div>
        </div>
        <div class="metric">
          <div class="metric-title">Handoffs done</div>
          <div class="metric-value" id="metricHandoffsDone">—</div>
        </div>
      </div>

      <details>
        <summary>Raw dashboard JSON</summary>
        <pre id="dashboardResult">Пока пусто.</pre>
      </details>
    </div>

    <div class="grid-2">
      <div class="card">
        <div class="section-title">
          <h2>Recent leads</h2>
          <button onclick="loadLeads()">Обновить</button>
        </div>
        <div id="leadsTableWrap" class="empty">Пока пусто.</div>

        <details>
          <summary>Raw leads JSON</summary>
          <pre id="leadsResult">Пока пусто.</pre>
        </details>
      </div>

      <div class="card">
        <div class="section-title">
          <h2>Recent handoffs</h2>
          <button onclick="loadHandoffs()">Обновить</button>
        </div>
        <div id="handoffsTableWrap" class="empty">Пока пусто.</div>

        <details>
          <summary>Raw handoffs JSON</summary>
          <pre id="handoffsResult">Пока пусто.</pre>
        </details>
      </div>
    </div>

    <div class="card" style="margin-top:16px;">
      <div class="section-title">
        <h2>Activity log</h2>
        <div class="top-actions">
          <button class="secondary-btn" onclick="clearActivity()">Очистить log</button>
        </div>
      </div>
      <div id="activityList" class="activity-list">
        <div class="empty">Пока пусто.</div>
      </div>
    </div>
  </div>

  <script>
    let currentSummary = null;
    let activityItems = [];

    function pretty(data) {
      return JSON.stringify(data, null, 2);
    }

    function nowTime() {
      const d = new Date();
      return d.toLocaleTimeString();
    }

    function addActivity(text, type = "info") {
      activityItems.unshift({
        time: nowTime(),
        text,
        type
      });
      activityItems = activityItems.slice(0, 12);
      renderActivity();
    }

    function clearActivity() {
      activityItems = [];
      renderActivity();
    }

    function renderActivity() {
      const box = document.getElementById("activityList");

      if (activityItems.length === 0) {
        box.innerHTML = '<div class="empty">Пока пусто.</div>';
        return;
      }

      box.innerHTML = activityItems.map(item => `
        <div class="activity-item activity-${item.type}">
          <div class="activity-time">${item.time}</div>
          <div>${item.text}</div>
        </div>
      `).join("");
    }

    function statusPill(status) {
      if (!status) return '<span class="pill">none</span>';
      if (status === "qualified" || status === "done") return '<span class="pill ok">' + status + '</span>';
      if (status === "needs_followup" || status === "pending") return '<span class="pill warn">' + status + '</span>';
      return '<span class="pill info">' + status + '</span>';
    }

    function clearMessageForm() {
      document.getElementById("messageInput").value = "";
    }

    function resetSummaryBlock() {
      currentSummary = null;
      document.getElementById("summaryLeadId").value = "";
      document.getElementById("summaryCards").innerHTML = '<div class="empty">Пока пусто.</div>';
      document.getElementById("summaryActions").innerHTML = "";
      document.getElementById("summaryResult").textContent = "Пока пусто.";
    }
async function seedDemo() {
  const confirmed = window.confirm("Загрузить готовые demo-данные? Текущие данные будут заменены.");
  if (!confirmed) {
    return;
  }

  const sendResult = document.getElementById("sendResult");

  try {
    const response = await fetch("/demo/seed", {
      method: "POST"
    });
    const data = await response.json();

    sendResult.textContent = pretty(data);

    document.getElementById("leadIdInput").value = "";
    document.getElementById("messageInput").value = "";
    resetSummaryBlock();

    clearActivity();
    addActivity("Demo data загружены.", "ok");

    await loadDashboard(false);
    await loadLeads();
    await loadHandoffs();

    if (data.seeded_lead_ids && data.seeded_lead_ids.length > 0) {
      await loadLeadSummaryById(data.seeded_lead_ids[0]);
    }
  } catch (error) {
    sendResult.textContent = "Ошибка: " + error;
    addActivity("Ошибка при загрузке demo data.", "warn");
  }
}
    async function resetDemo() {
      const confirmed = window.confirm("Точно удалить все demo-данные?");
      if (!confirmed) {
        return;
      }

      const sendResult = document.getElementById("sendResult");

      try {
        const response = await fetch("/demo/reset", {
          method: "POST"
        });
        const data = await response.json();

        sendResult.textContent = pretty(data);

        document.getElementById("leadIdInput").value = "";
        document.getElementById("messageInput").value = "";
        resetSummaryBlock();

        clearActivity();
        addActivity("Demo data очищены.", "ok");

        await loadDashboard(false);
        await loadLeads();
        await loadHandoffs();
      } catch (error) {
        sendResult.textContent = "Ошибка: " + error;
        addActivity("Ошибка при очистке demo data.", "warn");
      }
    }

    async function loadLeadSummaryById(id) {
      document.getElementById("summaryLeadId").value = id;
      await loadLeadSummary();
      document.getElementById("summaryCard").scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function renderSummaryActions(data) {
      const actions = document.getElementById("summaryActions");
      actions.innerHTML = "";

      if (!data || data.status !== "ok" || !data.lead || !data.lead.id) {
        return;
      }

      const lead = data.lead;
      const handoff = data.handoff || {};

      if (lead.lead_status !== "qualified") {
        actions.innerHTML += '<button class="warn-btn" onclick="markLeadQualified()">Mark qualified</button>';
      }

      if (handoff.id && handoff.handoff_status !== "in_progress") {
        actions.innerHTML += '<button class="secondary-btn" onclick="markHandoffInProgress()">Set handoff in progress</button>';
      }

      if (handoff.id && handoff.handoff_status !== "done") {
        actions.innerHTML += '<button class="success-btn" onclick="markHandoffDone()">Set handoff done</button>';
      }
    }

    async function markLeadQualified() {
      if (!currentSummary || !currentSummary.lead || !currentSummary.lead.id) return;

      const leadId = currentSummary.lead.id;
      const result = document.getElementById("sendResult");

      try {
        const response = await fetch(`/leads/${leadId}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ status: "qualified" })
        });
        const data = await response.json();
        result.textContent = pretty(data);

        addActivity(`Lead ${leadId} переведён в qualified.`, "ok");

        await loadLeadSummary();
        await loadDashboard(false);
        await loadLeads();
        await loadHandoffs();
      } catch (error) {
        result.textContent = "Ошибка: " + error;
        addActivity(`Ошибка при переводе lead ${leadId} в qualified.`, "warn");
      }
    }

    async function markHandoffInProgress() {
      if (!currentSummary || !currentSummary.handoff || !currentSummary.handoff.id) return;

      const handoffId = currentSummary.handoff.id;
      const result = document.getElementById("sendResult");

      try {
        const response = await fetch(`/handoffs/${handoffId}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            assigned_to: "Tony",
            status: "in_progress"
          })
        });
        const data = await response.json();
        result.textContent = pretty(data);

        addActivity(`Handoff ${handoffId} переведён в in_progress.`, "info");

        await loadLeadSummary();
        await loadDashboard(false);
        await loadLeads();
        await loadHandoffs();
      } catch (error) {
        result.textContent = "Ошибка: " + error;
        addActivity(`Ошибка при обновлении handoff ${handoffId}.`, "warn");
      }
    }

    async function markHandoffDone() {
      if (!currentSummary || !currentSummary.handoff || !currentSummary.handoff.id) return;

      const handoffId = currentSummary.handoff.id;
      const result = document.getElementById("sendResult");

      try {
        const response = await fetch(`/handoffs/${handoffId}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            assigned_to: "Tony",
            status: "done"
          })
        });
        const data = await response.json();
        result.textContent = pretty(data);

        addActivity(`Handoff ${handoffId} закрыт со статусом done.`, "ok");

        await loadLeadSummary();
        await loadDashboard(false);
        await loadLeads();
        await loadHandoffs();
      } catch (error) {
        result.textContent = "Ошибка: " + error;
        addActivity(`Ошибка при закрытии handoff ${handoffId}.`, "warn");
      }
    }

    async function sendMessage() {
      const leadIdRaw = document.getElementById("leadIdInput").value.trim();
      const message = document.getElementById("messageInput").value.trim();
      const result = document.getElementById("sendResult");

      if (!message) {
        result.textContent = "Введите сообщение.";
        return;
      }

      const payload = { message };
      if (leadIdRaw) {
        payload.lead_id = Number(leadIdRaw);
      }

      try {
        const response = await fetch("/chat/message", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await response.json();
        result.textContent = pretty(data);

        if (data.lead_id) {
          document.getElementById("summaryLeadId").value = data.lead_id;
          document.getElementById("leadIdInput").value = data.lead_id;
          await loadLeadSummary();
          addActivity(`Сообщение обработано. Lead ${data.lead_id} обновлён.`, "ok");
        } else {
          addActivity("Сообщение обработано.", "info");
        }

        await loadDashboard(false);
        await loadLeads();
        await loadHandoffs();
      } catch (error) {
        result.textContent = "Ошибка: " + error;
        addActivity("Ошибка при отправке сообщения.", "warn");
      }
    }

    async function loadDashboard(withLog = true) {
      const result = document.getElementById("dashboardResult");
      try {
        const response = await fetch("/dashboard/overview");
        const data = await response.json();
        result.textContent = pretty(data);

        document.getElementById("metricLeadsTotal").textContent = data.leads?.total ?? "—";
        document.getElementById("metricLeadsQualified").textContent = data.leads?.qualified ?? "—";
        document.getElementById("metricHandoffsProgress").textContent = data.handoffs?.in_progress ?? "—";
        document.getElementById("metricHandoffsDone").textContent = data.handoffs?.done ?? "—";

        if (withLog) {
          addActivity("Dashboard обновлён.", "info");
        }
      } catch (error) {
        result.textContent = "Ошибка: " + error;
        addActivity("Ошибка загрузки dashboard.", "warn");
      }
    }

    async function loadLeadSummary() {
      const leadId = document.getElementById("summaryLeadId").value.trim();
      const result = document.getElementById("summaryResult");
      const cards = document.getElementById("summaryCards");

      if (!leadId) {
        result.textContent = "Введите lead_id.";
        cards.innerHTML = '<div class="empty">Введите lead_id.</div>';
        document.getElementById("summaryActions").innerHTML = "";
        return;
      }

      try {
        const response = await fetch(`/leads/${leadId}/summary`);
        const data = await response.json();
        currentSummary = data;
        result.textContent = pretty(data);

        if (data.status !== "ok") {
          cards.innerHTML = '<div class="empty">Lead не найден.</div>';
          document.getElementById("summaryActions").innerHTML = "";
          addActivity(`Lead ${leadId} не найден.`, "warn");
          return;
        }

        const lead = data.lead || {};
        const handoff = data.handoff || {};
        const conversation = data.conversation || {};

        cards.innerHTML = `
          <div>
            <span class="pill">lead_id: ${lead.id ?? "—"}</span>
            ${statusPill(lead.lead_status)}
            ${statusPill(handoff.handoff_status)}
          </div>
          <div class="summary-line"><strong>Компания:</strong> ${lead.company ?? "—"}</div>
          <div class="summary-line"><strong>Роль:</strong> ${lead.role ?? "—"}</div>
          <div class="summary-line"><strong>Контакт:</strong> ${lead.contact ?? "—"}</div>
          <div class="summary-line"><strong>Use case:</strong> ${lead.use_case ?? "—"}</div>
          <div class="summary-line"><strong>Assigned to:</strong> ${handoff.assigned_to ?? "—"}</div>
          <div class="summary-line"><strong>Last sender:</strong> ${conversation.last_sender ?? "—"}</div>
          <div class="summary-line"><strong>Last intent:</strong> ${conversation.last_intent ?? "—"}</div>
          <div class="summary-line"><strong>Last text:</strong> ${conversation.last_text ?? "—"}</div>
        `;

        renderSummaryActions(data);
        addActivity(`Открыт summary для lead ${leadId}.`, "info");
      } catch (error) {
        result.textContent = "Ошибка: " + error;
        cards.innerHTML = '<div class="empty">Ошибка загрузки.</div>';
        document.getElementById("summaryActions").innerHTML = "";
        addActivity(`Ошибка загрузки summary для lead ${leadId}.`, "warn");
      }
    }

    async function loadLeads() {
      const result = document.getElementById("leadsResult");
      const wrap = document.getElementById("leadsTableWrap");

      try {
        const response = await fetch("/leads");
        const data = await response.json();
        result.textContent = pretty(data);

        if (!Array.isArray(data) || data.length === 0) {
          wrap.innerHTML = '<div class="empty">Нет лидов.</div>';
          return;
        }

        wrap.innerHTML = `
          <table class="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Company</th>
                <th>Role</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              ${data.slice(0, 8).map(item => `
                <tr>
                  <td>${item.id ?? "—"}</td>
                  <td>${item.company ?? "—"}</td>
                  <td>${item.role ?? "—"}</td>
                  <td>${statusPill(item.status)}</td>
                  <td><button class="small-btn" onclick="loadLeadSummaryById(${item.id})">Open</button></td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        `;
      } catch (error) {
        result.textContent = "Ошибка: " + error;
        wrap.innerHTML = '<div class="empty">Ошибка загрузки.</div>';
        addActivity("Ошибка загрузки leads.", "warn");
      }
    }

    async function loadHandoffs() {
      const result = document.getElementById("handoffsResult");
      const wrap = document.getElementById("handoffsTableWrap");

      try {
        const response = await fetch("/handoffs");
        const data = await response.json();
        result.textContent = pretty(data);

        if (!Array.isArray(data) || data.length === 0) {
          wrap.innerHTML = '<div class="empty">Нет handoff.</div>';
          return;
        }

        wrap.innerHTML = `
          <table class="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Lead ID</th>
                <th>Assigned</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              ${data.slice(0, 8).map(item => `
                <tr>
                  <td>${item.id ?? "—"}</td>
                  <td>${item.lead_id ?? "—"}</td>
                  <td>${item.assigned_to ?? "—"}</td>
                  <td>${statusPill(item.status)}</td>
                  <td><button class="small-btn" onclick="loadLeadSummaryById(${item.lead_id})">Open lead</button></td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        `;
      } catch (error) {
        result.textContent = "Ошибка: " + error;
        wrap.innerHTML = '<div class="empty">Ошибка загрузки.</div>';
        addActivity("Ошибка загрузки handoffs.", "warn");
      }
    }

    async function initPage() {
      addActivity("UI загружен.", "info");
      await loadDashboard(false);
      await loadLeads();
      await loadHandoffs();
    }

    initPage();
  </script>
</body>
</html>
"""
