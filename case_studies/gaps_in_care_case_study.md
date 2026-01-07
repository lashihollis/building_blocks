# Improving Gaps in Care Visibility to Support Preventive Care Outcomes

## Overview

Preventive care gaps (e.g., breast cancer screenings, A1c checks) are critical to patient health outcomes and directly tied to quality incentives and revenue in value-based care models. At the time of this work, multiple teams relied on fragmented and manual processes to identify and act on these gaps.

This case study outlines how a scalable, trusted data foundation was built to support reporting, care team workflows, and external vendor integrations — operating as a platform product rather than a one-off analytics project.

---

## Product Context

The organization lacked a single, reliable source of truth for gaps-in-care (GIC) data. Existing processes were slow, inconsistent, and required significant manual effort to prepare information for quality reporting and downstream systems. These inefficiencies led to delayed preventive care actions and missed financial opportunities.

Leadership elevated gaps in care to a company-wide priority, creating urgency to deliver a solution that balanced speed, accuracy, and long-term scalability.

---

## Users & Stakeholders

### Primary Users

* **Quality Team** – Responsible for performance reporting, leadership updates, and quality metric tracking.

### Secondary Users

* **Patient Care Teams** – Consumed gaps-in-care information through internal software interfaces to guide outreach and care delivery.
* **Software Engineers** – Integrated GIC data into user-facing tools and maintained downstream systems.

### Key Stakeholders

* Organizational leadership
* Analytics and data teams
* Clinical and operational partners

---

## Problem Statement

Prior to this initiative:

* Gaps-in-care data was inconsistent and slow to surface
* Manual workflows were required to make data usable
* Existing reporting assets were underutilized or poorly understood
* Teams lacked confidence in the accuracy of the data

As a result, care teams struggled to act efficiently, and the organization missed opportunities to improve patient outcomes and capture quality-driven revenue.

---

## Product Goals

* Enable care teams to identify and address preventive care needs more effectively
* Support leadership’s focus on improving quality performance and revenue outcomes
* Reduce manual effort and operational friction across reporting workflows
* Establish a trusted, reusable data foundation to support multiple downstream use cases

---

## Role & Ownership

I owned the design and delivery of the data foundation powering the gaps-in-care initiative.

Key responsibilities included:

* Designing and building the end-to-end data pipeline based on quality team requirements
* Modeling analytics-ready datasets to surface standardized gaps-in-care data
* Creating and maintaining data exports sent to third-party vendors used for gap calculations and accreditation reporting

While clinical intent and quality goals were defined by stakeholders, I translated those needs into scalable technical solutions that could reliably support reporting, product interfaces, and external dependencies.

---

## Product & Technical Decisions

### Standardizing Gap Logic

* Defined and refined compliance logic based on payer-provided data
* Partnered with quality analysts to align clinical intent with technical implementation
* Iterated on definitions as requirements evolved to maintain consistency across teams

### Scope Management

* Pushed back on requests that would duplicate data already available in other marts (e.g., member demographic information)
* Maintained clear ownership boundaries to reduce confusion and ensure long-term maintainability
* Framed decisions around reuse, clarity, and platform health rather than short-term convenience

---

## Constraints & Tradeoffs

This initiative faced several constraints:

* Dependency on the availability and stability of payer data
* A shift from ingesting full payer files to a minimum viable schema in BigQuery
* Significant time pressure due to leadership prioritization

To address these constraints:

* I optimized ingestion and transformation workflows around the most stable and actionable data
* Prioritized delivery of a trusted core dataset over completeness
* Deferred lower-impact manual processes to later phases without blocking adoption

---

## Phased Delivery Approach

### Phase 1 (MVP)

* Delivered accurate, accessible gaps-in-care data
* Enabled immediate use by quality teams and software engineers
* Powered care team interfaces and leadership reporting

### Phase 2 (Planned)

* Reintroduced select manual reporting adjustments (e.g., reporting month logic)
* Expanded functionality once trust and adoption were established

---

## Outcomes & Impact

### Adoption & Usage

* Used for monthly quality reporting delivered to leadership
* Consumed via daily and monthly exports to third-party vendors
* Combined with external vendor data to create holistic quality reports

### Operational Efficiency

* Manual data preparation was largely eliminated
* Remaining manual work was limited to spot validation
* Reporting cycles became faster, more repeatable, and more reliable

### Care Team Enablement

* Software engineers consistently surfaced gaps-in-care data in internal tools
* Care teams gained more reliable visibility into preventive care needs
* Enabled more proactive outreach and care coordination

### Stakeholder Feedback

* Positive feedback on speed of delivery despite evolving requirements
* Recognition of collaborative approach and willingness to support cross-team needs
* Confidence that reporting objectives were met as intended

---

## Reflection & Future Opportunities

### What I’d Improve

* Set expectations and clarify strategic importance earlier, especially as the work evolved from a side project into a major initiative
* Ask more upfront questions around urgency, scope, and downstream dependencies
* Invest earlier in documentation to support continuity during personnel changes and parallel implementations

### What I’d Explore Next

* Identify additional quality reporting pain points that could benefit from automation or standardization
* Partner earlier with stakeholders to scope and prioritize improvements based on care and reporting impact
* Extend existing data products to support new use cases without introducing unnecessary complexity

---

## Summary

This initiative transformed gaps-in-care data into a trusted, scalable platform that supported quality reporting, care team workflows, and external integrations. It demonstrates technical product ownership, cross-functional leadership, and outcome-driven decision-making — key competencies for a Technical Product Management role.
