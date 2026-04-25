# AI Lead Agent

Demo-ready MVP для входящих B2B-запросов.

## Что умеет

- принимает входящее сообщение в свободной форме
- извлекает company, role, contact, use_case
- создаёт или обновляет lead
- переводит lead в qualified
- автоматически создаёт handoff
- поддерживает handoff lifecycle: pending -> in_progress -> done
- показывает dashboard overview
- поддерживает demo reset и demo seed
- имеет UI на `/ui`

## Основные endpoint'ы

- `POST /chat/message`
- `GET /leads`
- `GET /leads/{lead_id}`
- `PATCH /leads/{lead_id}`
- `GET /leads/{lead_id}/messages`
- `GET /leads/{lead_id}/summary`
- `GET /handoffs`
- `GET /handoffs/{handoff_id}`
- `PATCH /handoffs/{handoff_id}`
- `GET /dashboard/overview`
- `POST /demo/reset`
- `POST /demo/seed`
- `GET /ui`
- `GET /health`

## Как запустить

```bash
cd ~/Desktop/python_tony
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload