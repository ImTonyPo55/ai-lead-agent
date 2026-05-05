# MechanicFlow AI MVP Acceptance Checklist

MechanicFlow AI is an AI intake workflow for inbound gamified campaign leads. It extracts campaign details, recommends a game mechanic, qualifies the lead, creates a CRM-ready handoff package, and tracks the lifecycle from follow-up to handoff, work in progress, and completion.

## Included in This MVP

- Campaign lead intake from a free-form message.
- Company, contact, role, campaign need, client type, campaign goal, platform, mechanic, tier, owner, and next action extraction.
- Game mechanic recommendation for common campaign needs such as Spin-to-Win, Advent Calendar, Rewards Campaign, Quiz / Lead Magnet, and discovery packages.
- Qualification status handling for `needs_followup`, `ready_to_handoff`, `active_handoff`, and `completed_handoff`.
- CRM-ready handoff package with payload preview and copy-ready sales brief.
- Follow-up package for incomplete leads.
- Handoff lifecycle actions: move to work and complete handoff.
- Dashboard counters for campaign leads, qualified leads, in-progress handoffs, and completed handoffs.
- Event timeline and Telegram notifications when configured.
- Production UI routes for `/`, `/ui`, `/ui/`, and `/health`.

## Not Included Yet

- Authentication.
- Billing or subscriptions.
- Multi-client workspaces.
- Real CRM OAuth or native HubSpot/Salesforce sync.
- User roles and permissions.
- Full production analytics warehouse.

## Acceptance Test Scenarios

1. UrbanFit ready lead: send `We are UrbanFit. Need a spin-to-win campaign for Shopify lead capture. Contact @urbanfit_cmo`. Expected result: ready for handoff, Shopify, lead capture, Spin-to-Win, DIY Tier, owner Tony / Sales, CRM payload available.
2. NoContactFit follow-up lead: send `We are NoContactFit. Need a spin-to-win campaign for Shopify lead capture.`. Expected result: needs follow-up, missing contact, no handoff, no CRM export button.
3. Nova Agency ready lead: send `We are Nova Agency. Need a branded Advent Calendar campaign for a client. Contact @nova_agency`. Expected result: agency, holiday promo, Advent Calendar, Done-With-You Tier, ready for handoff.
4. FreshBox ready lead: send `We are FreshBox. Need a retention campaign with rewards for returning customers. Contact @freshbox_growth`. Expected result: ecommerce brand, retention, Rewards Campaign, Done-With-You Tier, ready for handoff.
5. GameLaunch Studio ready lead: send `We are GameLaunch Studio. Need a quiz lead magnet for a new product launch. Contact @gamelaunch_cmo`. Expected result: gaming studio, product launch, Quiz / Lead Magnet, Done-With-You Tier, ready for handoff.

## Production URL Note

Use the Render primary URL for client review and demos. The app must serve the UI from `/`, `/ui`, and `/ui/`, and health status from `/health`.

## Known Limitations

- No authentication yet.
- No multi-client workspace isolation yet.
- No real CRM OAuth or direct CRM writeback yet.
- Telegram notification delivery depends on environment variables being configured.
- The CRM export is an MVP simulation that returns a clean payload for integration planning.
