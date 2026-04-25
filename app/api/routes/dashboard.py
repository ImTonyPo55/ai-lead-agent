from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import Lead, Handoff
from app.db.session import get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview")
def dashboard_overview(db: Session = Depends(get_db)) -> dict:
    total_leads = db.query(Lead).count()
    qualified_leads = db.query(Lead).filter(Lead.status == "qualified").count()
    needs_followup_leads = db.query(Lead).filter(
        Lead.status == "needs_followup").count()

    total_handoffs = db.query(Handoff).count()
    pending_handoffs = db.query(Handoff).filter(
        Handoff.status == "pending").count()
    in_progress_handoffs = db.query(Handoff).filter(
        Handoff.status == "in_progress").count()
    done_handoffs = db.query(Handoff).filter(Handoff.status == "done").count()

    recent_leads = (
        db.query(Lead)
        .order_by(Lead.id.desc())
        .limit(5)
        .all()
    )

    recent_handoffs = (
        db.query(Handoff)
        .order_by(Handoff.id.desc())
        .limit(5)
        .all()
    )

    return {
        "status": "ok",
        "leads": {
            "total": total_leads,
            "qualified": qualified_leads,
            "needs_followup": needs_followup_leads,
        },
        "handoffs": {
            "total": total_handoffs,
            "pending": pending_handoffs,
            "in_progress": in_progress_handoffs,
            "done": done_handoffs,
        },
        "recent_leads": [
            {
                "id": lead.id,
                "company": lead.company,
                "role": lead.role,
                "contact": lead.contact,
                "use_case": lead.use_case,
                "lead_status": lead.status,
                "created_at": str(lead.created_at),
            }
            for lead in recent_leads
        ],
        "recent_handoffs": [
            {
                "id": handoff.id,
                "lead_id": handoff.lead_id,
                "reason": handoff.reason,
                "assigned_to": handoff.assigned_to,
                "handoff_status": handoff.status,
                "created_at": str(handoff.created_at),
            }
            for handoff in recent_handoffs
        ],
    }
