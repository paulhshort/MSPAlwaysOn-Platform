---
```markdown
# 🔍 DeepResearch Canvas: SentinelOne MDR

**Platform URL:** https://usea1-cw04mdr.sentinelone.net  
**API Docs & Developer References:**  
- https://usea1-cw04mdr.sentinelone.net/api-doc/  
- https://usea1-cw04mdr.sentinelone.net/docs/en/generating-api-tokens.html  

---

## 🧠 Research Task:
Conduct a deep technical investigation of the **SentinelOne MDR** platform, focusing on its **REST API**, MDR capabilities, incident remediation workflows, and integration potential for MSPs. Priority is given to endpoint management, threat detection retrieval, automation of common SOC tasks, and tenant/org-based access control.

---

## 📌 Research Instructions:

### 1. **API Documentation Mapping**
- Map the structure and scope of SentinelOne's API:
  - Base URL and versioning.
  - Endpoint groups (e.g., `threats`, `agents`, `activities`, `accounts`, `sites`, `webhooks`).
  - Authentication method (token generation, expiry, scopes).
- For each major endpoint:
  - Document available HTTP methods (GET, POST, PUT, DELETE).
  - Required parameters and data schemas.
  - Provide example JSON payloads for both requests and responses.
  - Note filtering capabilities (e.g., get all unresolved threats in last 24 hours).

### 2. **Authentication & Permissions**
- Explore API token generation process (per user, per org/site).
- Define token scopes and expiration details.
- Detail best practices for securing tokens in MSP automation workflows.
- Identify if the platform supports scoped tokens per client (tenant-level isolation).

### 3. **Threat Management & Remediation**
- Document how to:
  - Pull a list of active threats.
  - Get threat details, status, and classification.
  - Trigger remediation actions (e.g., resolve, rollback, disconnect from network).
- Include command examples for initiating automated response actions from scripts or dashboards.

### 4. **Endpoint & Agent Management**
- Explore how to list agents, check device health, assign policies.
- Identify options to uninstall, scan, isolate, or reboot endpoints via API.
- Document asset metadata accessible via API (OS, hostname, IP, agent version, etc.).

### 5. **Automation & Webhooks**
- Look into real-time webhook support:
  - List available events (e.g., threat detected, agent offline).
  - Explain how to configure and test webhook delivery.
- Explore polling alternatives if no webhooks are available.
- Identify available PowerShell, Python, or Postman scripts for common automation tasks.

### 6. **Multi-Tenant MSP Support**
- Identify features that support multi-site or multi-organization management:
  - Site-level scoping for agents, threats, and users.
  - Role-based access via API or console.
  - Aggregated vs scoped reporting options.
- Investigate if MSPs can provision new tenants (sites/accounts) via API.

### 7. **Integration Paths**
- Investigate integrations with:
  - ConnectWise Manage (for alert > ticket workflows).
  - IT Glue (threat object linking, device notes).
  - Grafana or SIEM platforms (event export or dashboarding).
- Find GitHub repos or scripts that showcase security response playbooks.

---

## 🧾 Output Format:
<output_format>

# SentinelOne MDR API Research Summary

## Executive Summary

- Overview of API capabilities, remediation workflows, and integration points

## API Endpoint Overview

| Endpoint Group | Methods           | Use Case Examples                        |
| -------------- | ----------------- | ---------------------------------------- |
| `/threats`     | GET, POST         | Query, resolve, rollback threats         |
| `/agents`      | GET, POST, DELETE | List agents, run scans, isolate machines |
| `/activities`  | GET               | Review platform events and logs          |
| `/webhooks`    | GET, POST         | Real-time event alerting                 |

## Auth & Security

- Token generation and usage

- Scope and expiration

- MSP token strategies

## Threat Response

- Pulling unresolved threats

- Automating remediation (rollback, resolve, disconnect)

## Agent & Endpoint Control

- Available agent commands

- Metadata & status fields

- Bulk actions and tagging

## Automation Tools

- Webhook setup

- Scripting modules (PowerShell, Python)

- Postman collections

## Multi-Tenant Features

- Managing multiple clients

- Site scoping

- Reporting by org

## Integrations

- Known CW Manage/SIEM/IT Glue integrations

- Open-source or community tools

## Known Limitations

- Rate limits

- Historical data retention

- Permissions issues across sites

## References & Resources

- API Docs

- Token Setup Guide

- Community Projects or Examples


## ✅ Deliverables:
- Complete technical breakdown of SentinelOne MDR API
- Emphasis on real-world MSP use cases (bulk remediation, alert triage automation, SOC alerting)
- Data payload examples and authentication guidance
</output_format>


