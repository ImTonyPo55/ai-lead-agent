# MechanicFlow AI Client Demo Script

## 30-Second Explanation

MechanicFlow AI is an AI intake agent for companies selling gamified marketing campaigns. It reads inbound campaign requests, extracts the key business details, recommends the best game mechanic, qualifies whether the lead is ready, and prepares a CRM-ready handoff package for the sales or delivery team.

## 2-Minute Demo Flow

1. Open the MechanicFlow AI UI.
2. Start with the dashboard: show campaign leads, qualified, in progress, and completed counters.
3. Paste a ready lead example such as UrbanFit, then send it with Lead ID empty.
4. Open the generated lead summary and show status, score, company, contact, campaign need, best game mechanic, tier, owner, and next action.
5. Show the Campaign handoff package: summary, why qualified, CRM payload preview, Export to CRM, Copy package, and Move to work.
6. Click Move to work only if you want to demonstrate lifecycle. The handoff should become in progress and stop looking like a new handoff.
7. Optionally show the NoContactFit example to explain the follow-up workflow without creating a handoff.

## What to Show First

- The dark MechanicFlow AI workspace and dashboard counters.
- A ready campaign lead summary.
- The game mechanic recommendation and why it fits.
- The CRM-ready handoff package and payload preview.
- The event timeline as proof that the workflow is tracked.

## What Not to Click During Client Demo

- Do not use reset unless you intentionally want to clear all local demo data.
- Do not open raw Technical JSON unless the client asks about API payloads.
- Do not present CRM export as a live HubSpot/Salesforce integration. It is an MVP export simulation and payload preview.
- Do not test Telegram live unless environment variables are already confirmed.

## Explaining Follow-Up vs Ready Handoff

- Follow-up package means the lead is useful but missing a critical field, usually contact or campaign objective. MechanicFlow AI generates one clear next question and a copy-ready follow-up.
- Campaign handoff package means the lead has enough data for sales or delivery to act: company, contact, campaign need, goal or mechanic, client type, recommended tier, owner, and next action.

## Explaining the CRM-Ready Package

The CRM-ready package is the structured sales brief. It includes the lead summary, qualification reason, recommended game mechanic, tier, next action, owner/team routing, and a clean payload that can later be connected to HubSpot, Salesforce, Pipedrive, or another CRM.
