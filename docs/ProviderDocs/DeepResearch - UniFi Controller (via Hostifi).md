# DeepResearch - UniFi Controller (via Hostifi)

**Platform URL:** https://m04032.hostifi.com:8443  
**Verified Docs & Resources:**  

- https://github.com/Art-of-WiFi/UniFi-Cloud-API-client  
- https://github.com/Art-of-WiFi/UniFi-API-client  
- https://developer.ui.com/unifi-api/  
- https://developer.ui.com/site-manager-api/gettingstarted/  
- https://support.hostifi.com/en/articles/3779128-unifi-alerts-with-slack-integration  
- https://support.hostifi.com/en/articles/3773633-rewriting-unifi-email-alerts-with-mailparser-and-postmark  
- https://support.hostifi.com/en/articles/4859912-unifi-which-ports-you-should-allow-outbound-to-a-cloud-controller  
- https://support.hostifi.com/en/articles/3773235-how-to-integrate-unifi-email-alerts-with-mailparser  
- https://unificontrol.readthedocs.io/en/latest/API.html
- https://unificontrol.readthedocs.io/en/latest/introduction.html
- https://unificontrol.readthedocs.io/en/latest/

---

## 🧠 Research Task:

Conduct a full technical analysis of the **UniFi Controller API** as deployed via **Hostifi**, with focus on:

- Multi-site MSP use
- API-based automation
- Monitoring and alert customization
- Integration potential with ticketing, reporting, and documentation platforms

Pay special attention to the Art-of-WiFi SDKs, and Hostifi-specific use cases for email alert rewrites, Slack integrations, and secure remote controller access.

---

## 📌 Research Instructions:

### 1. **API Authentication & Session Management**

- Document the authentication method for UniFi APIs (typically cookie/session based).
- Explore how session tokens are acquired, refreshed, and securely stored.
- Assess the feasibility of persistent service account use in MSP automation.

### 2. **Endpoint Analysis**

Using the Art-of-WiFi API clients and UniFi official documentation, extract and categorize the following:

- Client tracking: `/api/s/<site>/stat/sta`
- Device health and status: `/api/s/<site>/stat/device`, `/stat/health`
- Configuration: `/api/s/<site>/rest/wlanconf`, `/rest/networkconf`, `/rest/firewallrule`
- Commands: `/cmd/devmgr`, `/cmd/stamgr`
- Examples to document:
  - Reboot an access point remotely
  - Rename or modify an SSID
  - Block a rogue MAC address
  - Retrieve client bandwidth usage

### 3. **Multi-Site & MSP Operations**

- Investigate how UniFi handles multi-site architecture in API requests (`/s/<site>/`).
- Explore methods to discover site IDs and how switching is managed.
- Confirm if MSP-style delegated access or site RBAC is available via API.

### 4. **Monitoring & Alerts**

- Explore how API polling can be used to monitor:
  - Offline devices
  - High client load
  - Firmware out-of-date
- Review Hostifi’s guides on:
  - Slack alerting setup
  - Custom email parsing with Mailparser/Postmark
- Identify if any webhook support or alert endpoint exists.

### 5. **Integration Targets**

- Determine feasibility of integrating UniFi API data with:
  - **ConnectWise Manage** (e.g., auto-ticket for disconnected AP)
  - **IT Glue** (documenting devices per site)
  - **Grafana/Influx/Prometheus** (device health stats)
  - Email parsing tools for alert triage

### 6. **Security, Limits & Ports**

- Document which ports must be open to allow access to Hostifi cloud controllers.
- Review any known API rate limits or access throttling.
- Identify any gaps or gotchas (e.g., no native historical logging via API).

---

## 🧾 Output Format:

<output_format>
# UniFi Controller API Research Summary

## Executive Summary

- Overview of UniFi API capabilities in Hostifi-hosted MSP scenarios

## Endpoint Breakdown

| Endpoint       | Verbs    | Use Case                      |
| -------------- | -------- | ----------------------------- |
| /stat/sta      | GET      | Get connected clients         |
| /stat/device   | GET      | Check device uptime, firmware |
| /cmd/devmgr    | POST     | Reboot or upgrade APs         |
| /rest/wlanconf | GET/POST | Modify SSID settings          |

## Auth & Session Management

- Session cookie-based auth

- Persistent login best practices

- Timeout considerations

## Multi-Site MSP Support

- Site switching via `/s/<site>/`

- Site ID discovery method

- Role-based user access

## Monitoring & Alerts

- Offline device detection

- Slack & Mailparser integration

- Bandwidth usage polling

## Integrations

- CW Manage (tickets from alerts)

- IT Glue asset injection

- Grafana/Influx metrics dashboards

## Security & Constraints

- Required outbound ports for Hostifi

- Rate limiting behavior

- No native webhook support

## Resources

- Art-of-WiFi GitHub SDKs

- Hostifi alerting & email parsing guides

- Ubiquiti developer documentation

## ✅ Deliverables:

- Endpoint coverage for MSP workflows
- Automation strategies for SSIDs, AP mgmt, and alerting
- Integration options and alert forwarding best practices
- Multi-site management techniques for client isolation
  
  </output_format>

---
