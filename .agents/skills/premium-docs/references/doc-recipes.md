# Document Recipes & Outlines

Use these recipes to structure deliverable documents. Every document starts with a `:::tldr` executive summary and ends with a **Next Steps** section.

---

## 1. Technical Report
- **Tone**: Authoritative, analytical, objective.
- **Recommended Theme**: `aurora` or `slate`.
- **Key Components**: `:::tldr`, `:::stats`, `:::cards`, `:::compare`, responsive tables.
- **Section Order**:
  1. `:::tldr` (Key findings, numbers, and recommendations)
  2. Background & Problem Statement
  3. Performance & Impact Metrics (`:::stats`)
  4. Core Findings & Analysis
  5. Evaluated Alternatives (`:::compare`)
  6. Resource & Cost Implications (`:::kv`)
  7. Next Steps & Recommended Actions

---

## 2. Product Requirements Document (PRD / Feature Spec)
- **Tone**: Structured, user-centric, precise.
- **Recommended Theme**: `aurora`.
- **Key Components**: `:::tldr`, `:::cards`, `:::steps`, `:::tabs`, task checklists.
- **Section Order**:
  1. `:::tldr` (Problem solved, target user, target ship date)
  2. Motivation & Business Goals
  3. User Personas & Core Use Cases (`:::cards`)
  4. Functional Requirements & User Stories (with task checklists)
  5. User Flow & Technical Interaction (`:::steps`)
  6. Configuration & API Surface (`:::tabs`)
  7. Non-Functional Requirements (Latency, Privacy, Accessibility)
  8. Next Steps & Launch Milestones (`:::progress`)

---

## 3. Architecture Design Document (ADD / ADR)
- **Tone**: Principled, technical, long-term perspective.
- **Recommended Theme**: `slate` or `aurora`.
- **Key Components**: `:::tldr`, `:::cards`, `:::compare`, `:::filetree`, code blocks with titles.
- **Section Order**:
  1. `:::tldr` (Architectural decision summary, chosen stack, primary trade-off)
  2. Context & Requirements
  3. System Architecture & Components (`:::cards`)
  4. Architecture Decision Records (ADRs with `:::compare` for alternatives considered)
  5. Repository & Module Layout (`:::filetree`)
  6. Data Flow & Interface Contracts (Code blocks with titles)
  7. Failure Modes & Resilience Strategies (`:::callout`)
  8. Next Steps & Rollout Phases

---

## 4. Project README / High-Level Overview
- **Tone**: Welcoming, crisp, developer-friendly.
- **Recommended Theme**: `aurora`.
- **Key Components**: `:::tldr`, `:::stats`, `:::filetree`, code blocks with copy button.
- **Section Order**:
  1. `:::tldr` (What the project does, key differentiators, quickstart summary)
  2. Key Value Proposition (`:::cards`)
  3. Quickstart & Installation (Code blocks with filenames)
  4. Architecture & Repository Structure (`:::filetree`)
  5. Core Features & Supported Platforms (`:::tabs`)
  6. Configuration Parameters (`:::kv`)
  7. Next Steps & Contributing Links

---

## 5. Tutorial / Step-by-Step How-To
- **Tone**: Instructive, patient, clear.
- **Recommended Theme**: `paper` or `aurora`.
- **Key Components**: `:::tldr`, `:::steps`, `:::tip`, `:::tabs`.
- **Section Order**:
  1. `:::tldr` (What you will build, estimated completion time, prerequisites)
  2. Prerequisites & Environment Setup (`:::tabs` for OS variations)
  3. Sequential Implementation Walkthrough (`:::steps`)
  4. Code Explanations with inline tips (`:::tip`)
  5. Verification & Testing Instructions
  6. Common Gotchas & Troubleshooting (`:::faq`)
  7. Next Steps & Further Reading

---

## 6. Runbook / Standard Operating Procedure (SOP)
- **Tone**: Urgent, unambiguous, checklist-driven.
- **Recommended Theme**: `slate`.
- **Key Components**: `:::tldr`, `:::danger`, `:::steps`, `:::kv`.
- **Section Order**:
  1. `:::tldr` (Trigger condition, severity level, escalation contact, rollback command)
  2. Triage & Incident Verification (`:::callout-danger`)
  3. System Health Dashboard & Metrics (`:::stats`)
  4. Remediation Procedure (`:::steps` with exact commands)
  5. Rollback Procedure
  6. Post-Remediation Verification Checklist
  7. Next Steps & Incident Follow-Up

---

## 7. Incident Post-Mortem
- **Tone**: Blameless, rigorous, root-cause focused.
- **Recommended Theme**: `slate` or `paper`.
- **Key Components**: `:::tldr`, `:::stats`, `:::timeline`, `:::callout-warning`.
- **Section Order**:
  1. `:::tldr` (Impact summary, duration, root cause category, customer effect)
  2. Impact & Incident Metrics (`:::stats` for MTTR, affected users, data loss)
  3. Incident Timeline (`:::timeline`)
  4. Detailed Root Cause Analysis (5 Whys)
  5. What Went Well vs What Went Wrong (`:::compare`)
  6. Corrective Actions & Prevention Items (task checklists with owners)
  7. Next Steps & Review Schedule

---

## 8. Meeting Notes & Action Record
- **Tone**: Concise, executive, accountable.
- **Recommended Theme**: `paper` or `slate`.
- **Key Components**: `:::tldr`, `:::cards`, `:::kv`, checklists.
- **Section Order**:
  1. `:::tldr` (Meeting objective, key decisions ratified, top 3 action items)
  2. Attendees, Date & Context (`:::kv`)
  3. Key Discussion Topics & Perspectives (`:::cards`)
  4. Decisions Ratified
  5. Action Items & Assignees (Task checklist)
  6. Open Questions
  7. Next Steps & Follow-Up Date

---

## 9. Decision Memo / Options Comparison
- **Tone**: Neutral, comparative, evidence-backed.
- **Recommended Theme**: `slate` or `paper`.
- **Key Components**: `:::tldr`, `:::compare`, responsive comparison table.
- **Section Order**:
  1. `:::tldr` (Recommendation, key trade-off, cost/benefit summary)
  2. Decision Context & Business Constraint
  3. Option A vs Option B Comparison (`:::compare`)
  4. Multi-Dimensional Comparison Matrix (Responsive table)
  5. Stakeholder Perspectives & Risks
  6. Recommended Choice & Rationale
  7. Next Steps & Implementation Plan

---

## 10. Release Notes
- **Tone**: Celebratory, informative, changelog-structured.
- **Recommended Theme**: `aurora`.
- **Key Components**: `:::tldr`, `:::cards`, `:::callout-warning`, code snippets.
- **Section Order**:
  1. `:::tldr` (Release version, highlight summary, upgrade command)
  2. Major New Features (`:::cards`)
  3. Breaking Changes & Migration Steps (`:::callout-warning` and `:::steps`)
  4. Bug Fixes & Performance Improvements (`:::stats`)
  5. Contributors & Third-Party Notices
  6. Next Steps & Roadmap Preview

---

## 11. Research Summary / Literature Review
- **Tone**: Scholarly, rigorous, synthesized.
- **Recommended Theme**: `paper`.
- **Key Components**: `:::tldr`, `:::cards`, blockquotes, citations.
- **Section Order**:
  1. `:::tldr` (Core thesis, methodology, primary takeaways)
  2. Research Context & Questions
  3. Methodologies & Data Sources
  4. Findings & Thematic Synthesis (`:::cards`)
  5. Limitations & Threats to Validity
  6. Industry / Codebase Implications
  7. Next Steps & Future Research Directions

---

## 12. Engineering Onboarding Guide
- **Tone**: Empathetic, structured, empowering.
- **Recommended Theme**: `aurora` or `paper`.
- **Key Components**: `:::tldr`, `:::steps`, `:::tabs`, `:::filetree`, `:::faq`.
- **Section Order**:
  1. `:::tldr` (First-week checklist, dev setup duration, key mentors)
  2. Local Environment Setup (`:::tabs` for macOS/Linux/Windows)
  3. Repository Architecture (`:::filetree`)
  4. First PR Walkthrough (`:::steps`)
  5. Engineering Standards & Conventions
  6. Frequently Asked Questions (`:::faq`)
  7. Next Steps & 30-Day Milestone Goals

---

## 13. API Reference & Developer Guide
- **Tone**: Technical, concise, syntax-accurate.
- **Recommended Theme**: `aurora`.
- **Key Components**: `:::tldr`, `:::tabs`, code blocks with titles, responsive tables.
- **Section Order**:
  1. `:::tldr` (Base URL, auth method, rate limits, status check)
  2. Authentication & Headers (`:::kv`)
  3. Endpoints Matrix (Responsive table with methods and status codes)
  4. Request & Response Payloads (Code blocks with JSON title)
  5. SDK Client Usage (`:::tabs` for multiple languages)
  6. Error Codes & Handling (`:::callout-danger`)
  7. Next Steps & Interactive Sandbox Link
