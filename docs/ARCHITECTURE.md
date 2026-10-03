# Architecture
```text
Enterprise Goal -> Planner -> Typed DAG -> Runtime
                                  |
          +-----------------------+----------------------+
          |           |           |                     |
        Sales       Support    Commerce              Marketing
          +-----------+-----------+---------------------+
                                  |
                           Skills Registry
                                  |
                       MCP / Connector Gateway
                                  |
                     Policy / Approval / Audit
                                  |
                     Memory / Evaluation / Replan
```
Production evolution uses durable SQL state, transactional outbox, Kafka/Pulsar, leased workers, idempotency, reconciliation, OIDC/workload identity, policy-as-code, OpenTelemetry and Kubernetes.
