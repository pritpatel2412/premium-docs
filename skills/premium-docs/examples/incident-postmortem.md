---
title: "Post-Mortem: Incident INC-8492 Authentication Gateway Degradation"
subtitle: Comprehensive timeline, root-cause analysis, and corrective action ledger for October 12, 2026
author: Site Reliability Engineering Team
date: October 13, 2026
status: final
tags: [Post-Mortem, SRE, Incident-Response, Root-Cause, Reliability]
theme: slate
toc: true
---

:::tldr Incident Summary
On October 12, 2026, between 14:02 and 14:15 UTC, the primary authentication gateway experienced a **13-minute performance degradation**, resulting in elevated HTTP 504 Gateway Timeouts affecting 1.8% of inbound customer authentication requests. **Zero credential or customer data was compromised.**
:::

## 1. Incident Impact & Recovery Metrics

:::stats
13m 14s | Total Incident Duration | Under 15m SLA
1.8% | Affected Inbound Requests | Peak during outage
4m 02s | Time to Acknowledge (MTTA) | SRE on-call paged
0 | Data Loss / Compromise | Zero security impact
:::

## 2. High-Resolution Incident Timeline

:::timeline
14:02 UTC | Automated Alarm Fired | Datadog synthetic canary triggered alert `P99 Auth Gateway Latency > 2,000ms`.
14:04 UTC | PagerDuty Incident Escalated | Primary and secondary on-call reliability engineers paged and joined incident bridge.
14:06 UTC | Incident Declared | Incident Commander declared SEV-2 operational impact; status page updated.
14:09 UTC | Root Cause Identified | Engineer identified pool exhaustion on primary Redis session cache following a sudden network blip.
14:12 UTC | Hotfix Applied | Increased connection pool ceiling from 500 to 2,500 connections and restarted connection poolers.
14:15 UTC | Traffic Normalized | Latency returned to baseline 18ms; all pending authentication requests cleared.
14:30 UTC | Incident Terminated | System confirmed stable under standard production load; post-incident review initiated.
:::

## 3. Root Cause Analysis (5 Whys)

:::danger Immediate Failure Trigger
A transient 800ms network packet drop between AZ-East-1a and AZ-East-1b caused client requests to stall waiting for TCP ACKs.
:::

1. **Why did the gateway return HTTP 504 errors?**
   Because incoming worker threads hung waiting for an available connection from the local Redis session connection pool.
2. **Why was the connection pool exhausted?**
   Because the pool ceiling was hardcoded to 500 connections, while concurrent inbound traffic during peak hour exceeded 1,800 concurrent requests.
3. **Why didn't connections time out quickly?**
   Because the socket read timeout was configured to 30 seconds rather than our standard 1.5 seconds.
4. **Why was the timeout configured to 30 seconds?**
   A legacy configuration parameter from an old database driver migration was copied over without updating the timeout specification.
5. **Why was this discrepancy not detected earlier?**
   The staging load testing suite did not simulate cross-availability-zone packet delay under sustained peak concurrency.

## 4. What Went Well vs. What Went Wrong

:::compare
### Pro: What Went Well
- Automated canary alerts fired within 90 seconds of the initial latency spike.
- Incident commander established the war room and status page communications in under 4 minutes.
- Rollback and pool expansion procedures completed cleanly without data corruption.
---
### Con: What Went Wrong
- Hardcoded connection pool ceiling was inadequate for peak enterprise traffic.
- Socket timeout was excessively permissive (30s), tying up worker threads during network delays.
- Staging load tests did not include chaos-injected packet loss profiles.
:::

## 5. Corrective Actions & Preventative Measures

The following remediation work is tracked in Jira under EPIC-SRE-412:

- [x] Expand default session connection pool ceiling from 500 to 2,500 connections.
- [x] Reduce Redis socket read timeout from 30,000ms to 1,500ms.
- [ ] Implement adaptive circuit breaker pattern around authentication cache lookups.
- [ ] Add automated chaos-testing tests simulating cross-AZ packet loss in staging CI.
- [ ] Audit all internal microservices for legacy connection timeout defaults.

## 6. Next Steps

1. Review post-mortem findings in the weekly Engineering Operations Review on Thursday.
2. Complete Jira tickets EPIC-SRE-412 by end of sprint (October 24, 2026).
3. Schedule synthetic chaos test run across staging clusters.
