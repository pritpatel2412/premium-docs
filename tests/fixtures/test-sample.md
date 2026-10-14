---
title: Engineering Design Document
subtitle: Distributed Cache Invalidation Service
author: Platform Engineering Team
date: October 2026
status: review
tags: [Infrastructure, Caching, Architecture]
theme: aurora
toc: true
---

:::tldr Key Summary
This document specifies the architecture for our global cache invalidation service, reducing cache staleness from 15 minutes to under 500 milliseconds across all 12 edge locations.
:::

## Overview & Background

Modern web applications require strong consistency for sensitive authorization state while benefiting from low-latency reads. Our current TTL-based cache model introduces unacceptable staleness windows.

:::note Architectural Decision
We selected an event-driven pub/sub architecture backed by persistent log streaming over direct point-to-point RPC invalidation.
:::

## Key Performance Targets

Here are the target performance metrics for the initial release:

:::stats
99.99% | Invalidation SLA | +0.4% vs Q2
< 250ms | Global Propagation | -14.5s vs TTL
120k | Invalidation Events/s | Sustained peak
0 | Data Loss Incidents | Zero tolerance
:::

## Architectural Components

The invalidation engine is organized into three decoupled subsystems:

:::cards
### Event Ingest Gateway
High-throughput REST and gRPC gateway validating write-through invalidation requests and signing them with cryptographic tokens.
---
### Distributed Log Stream
Partitioned append-only log cluster ensuring total ordering of invalidation events per tenant boundary.
---
### Edge Worker Daemon
Lightweight local agents colocated with caching layers, applying batch evictions and reporting heartbeat acknowledgments.
:::

## Deployment Workflow

Follow these steps to deploy a regional invalidation agent:

:::steps
### Configure IAM Permissions
Assign the edge daemon role with read access to the tenant invalidation topic.
### Deploy Daemon Container
Run the container using the standard systemd unit file or Kubernetes daemonset.
### Verify Health Check
Ensure the local probe reports healthy status on port 9090.
:::

## Implementation Profiles

:::tabs
@tab Edge Node (Go)
The Go-based daemon runs directly on cache nodes, consuming memory under 35MB per instance.

```go title="agent/daemon.go"
func (d *Daemon) ProcessInvalidations(ctx context.Context) error {
    for event := range d.events {
        d.cache.Invalidate(event.Key)
    }
    return nil
}
```

@tab Control Plane (Python)
The control plane coordinates cluster partition assignments and monitors heartbeat drift.

```python title="controller/main.py"
def reconcile_partitions(nodes: list[str]) -> dict[str, list[int]]:
    return {node: list(range(i, 64, len(nodes))) for i, node in enumerate(nodes)}
```
:::

## Comparison of Eviction Strategies

:::compare
### Pro: Active Pub/Sub Eviction
- Sub-second global propagation
- Zero cache stampede on update
- Minimal memory footprint
---
### Con: Passive TTL Expiration
- Unpredictable staleness windows
- Heavy database load during bulk refresh
- Difficult to invalidate related graph keys
:::

## System Directory Layout

:::filetree
invalidation-engine/
├── cmd/
│   ├── daemon/          # Edge invalidation worker
│   └── controller/      # Partition manager
├── pkg/
│   ├── cache/           # Eviction drivers
│   └── protocol/        # Protobuf definitions
└── config/              # Cluster deployment specs
:::

## System Configuration Parameters

:::kv
Default Buffer Size | 64 MB per worker
Max Batch Latency   | 50 ms
Replication Factor | 3 replicas across AZs
Protobuf Version   | v3.24.1
:::

## Frequently Asked Questions

:::faq
### What happens if an edge node loses network connectivity?
The edge node buffers locally and reconnects with exponential backoff. Upon reconnection, it queries the checkpoint offset to evict any keys missed during the partition.

### Can custom eviction keys use regex patterns?
Yes. Prefix matching and exact key hashes are supported with constant-time lookup.
:::

## Verification Checklist

- [x] Regional failover tested under synthetic partition
- [x] Benchmark validates 120,000 events/sec sustained throughput
- [ ] Multi-region active-active testing completed
