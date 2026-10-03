# Code Walkthrough

The runnable reference separates domain contracts, planning, compilation, specialist agents, connector/protocol boundaries, deterministic policy, execution, memory and evaluation.

- `domain.py`: typed GoalRequest, StepSpec, Plan and ConnectorCall.
- `planner.py`: deterministic no-key planner; replace with schema-constrained model adapter.
- `compiler.py`: graph validation and cycle detection.
- `registry.py`: bounded capabilities and risk.
- `agents.py`: Sales, Support, Commerce and Marketing specialists.
- `connectors.py`: executable local enterprise-system mocks.
- `protocols.py`: MCP and A2A boundaries.
- `policy.py`: deterministic authorization foundation.
- `security.py`: local auth and canonical action hash.
- `runtime.py`: dependency-aware orchestration and approval boundary.
- `memory.py`: six memory layers.
- `evaluation.py`: outcome evaluation.
- `models.py`: durable SQL entities.
- `service.py`: goal-to-execution coordinator.
- `api.py`: REST surface.
- `main.py`: application bootstrap.

Production should persist every state transition and dispatch through durable workers rather than relying on in-process execution.
