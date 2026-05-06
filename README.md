# MechanicFlow AI

**AI intake and lead qualification agent for gamified campaign leads.**

MechanicFlow AI turns messy inbound campaign requests into structured, qualified leads, recommends the best campaign mechanic, assigns a pricing tier, and prepares a CRM-ready handoff package for sales and delivery teams.

---

## Live Demo

- **App UI:** https://ai-lead-agent-mz5s.onrender.com/
- **Portfolio / Case Study:** https://ai-lead-agent-mz5s.onrender.com/portfolio

> Note: the demo is hosted on Render free tier, so the first request may take a few seconds if the service is sleeping.

---

## Problem

Inbound campaign requests often arrive as unstructured free-text messages from websites, Telegram, WhatsApp, email, or sales conversations.

Sales and delivery teams need to manually understand:

- who the client is;
- what campaign they need;
- what platform they use;
- which mechanic fits the request;
- whether the lead is qualified;
- who should handle it next;
- what should be sent to CRM or delivery.

This creates slow lead triage, inconsistent qualification, and messy handoff between sales and delivery.

---

## Solution

MechanicFlow AI automates the first layer of lead intake and qualification.

The agent receives an inbound message, extracts key business fields, classifies the request, recommends a campaign mechanic, prepares follow-up for incomplete leads, and creates a structured CRM-ready handoff package for qualified leads.

---

## What the MVP Does

- Accepts inbound lead messages in free-text format
- Extracts company, contact, role, campaign need, campaign goal, and platform
- Detects client type and campaign intent
- Recommends the best gamified campaign mechanic
- Assigns pricing tier and next action
- Routes ownership to the right owner/team
- Generates follow-up guidance for incomplete leads
- Builds a CRM-ready handoff summary for qualified leads
- Tracks lead lifecycle status
- Provides a clean demo UI for testing and presentation
- Includes dashboard and portfolio/case-study pages
- Supports Telegram notification integration when environment variables are configured

---

## Core Workflow

```text
Inbound message
   ↓
Field extraction
   ↓
Campaign intelligence
   ↓
Lead qualification
   ↓
Owner / team routing
   ↓
CRM-ready handoff package
   ↓
Lifecycle tracking
