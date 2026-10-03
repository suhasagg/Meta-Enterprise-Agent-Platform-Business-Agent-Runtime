# Distributed Runtime

Production topology:

```text
API -> SQL + Outbox -> Kafka/Pulsar -> Scheduler/Workers -> MCP/A2A/Connectors
 |                                                        |
 +---------------- Audit/Artifacts/Evaluation <-----------+
```

Use leases and fencing for task ownership, idempotency for logical actions, UNKNOWN plus reconciliation for ambiguous writes, checkpoints for restart, cancellation and compensation for long-running workflows, and explicit plan versions for replanning.

Never keep a SQL transaction open across an external model/tool call.
