from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import Lead, Handoff
from app.db.session import get_db
from app.services.handoff_package_service import build_handoff_package

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _latest_handoff(db: Session, lead_id: int) -> Handoff | None:
    return (
        db.query(Handoff)
        .filter(Handoff.lead_id == lead_id)
        .order_by(Handoff.id.desc())
        .first()
    )


@router.get("/overview")
def dashboard_overview(db: Session = Depends(get_db)) -> dict:
    leads = db.query(Lead).all()
    total_leads = len(leads)
    lead_packages = [
        (lead, build_handoff_package(lead, latest_handoff=_latest_handoff(db, lead.id)))
        for lead in leads
    ]
    qualified_leads = sum(
        1 for _, package in lead_packages
        if package["qualification_status"] == "ready_to_handoff"
    )
    needs_followup_leads = sum(
        1 for _, package in lead_packages
        if package["qualification_status"] in {"needs_followup", "needs_follow_up"}
    )

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
    recent_lead_packages = [
        (lead, build_handoff_package(lead, latest_handoff=_latest_handoff(db, lead.id)))
        for lead in recent_leads
    ]

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
                "lead_status": package["qualification_status"],
                "status": package["qualification_status"],
                "qualification_status": package["qualification_status"],
                "missing_fields": package["missing_fields"],
                "score": package["score"],
                "priority": package["priority"],
                "created_at": str(lead.created_at),
            }
            for lead, package in recent_lead_packages
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
