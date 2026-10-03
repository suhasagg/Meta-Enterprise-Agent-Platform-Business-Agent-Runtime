# Meta Enterprise Agent Platform / Business Agent Runtime
## Production-Oriented Multi-Agent Business Operations Platform

Meta publicly announced **Meta Enterprise Platform** on September 28, 2026, saying its initial enterprise stack includes Muse, Meta Business Agent, Muse API and Muse Code. Meta also publicly describes **Meta Business Agent Platform** as infrastructure for businesses to build, customize and deploy agents at scale, connect to hundreds of systems such as Shopify and Zendesk, and apply enterprise controls, guardrails and measurement.

# Architecture

```text
Enterprise Goal
      |
Goal Understanding
      |
AI / Deterministic Planner
      |
Typed Workflow DAG
      |
Durable Agent Runtime
      |
+---------+---------+----------+-----------+
| Sales   | Support | Commerce | Marketing |
+---------+---------+----------+-----------+
      |
Skills / Capability Registry
      |
MCP / Connector Gateway ---- A2A Delegation
      |
+---------+---------+---------+-----------+
| Shopify | Zendesk | CRM     | Calendar  |
| Meta    | Other governed enterprise systems       |
+---------+---------+---------+-----------+
      |
Policy + RBAC/ABAC
      |
Human Approval
      |
Action Execution
      |
Durable State + Event Stream
      |
Memory + Evaluation
      |
Replan / Continue / Complete
```

# What is implemented

- typed goal and plan contracts;
- deterministic planner that runs without an LLM key;
- DAG validation;
- Sales, Support, Commerce and Marketing agents;
- capability registry;
- local Shopify/Zendesk/CRM/Calendar/Meta-style connector mocks;
- MCP and A2A protocol boundaries;
- risk policy and approval boundary;
- canonical action hashing;
- layered memory;
- evaluator;
- PostgreSQL models for runs, steps, approvals, idempotency, memory and audit;
- FastAPI;
- Docker Compose;
- tests and examples.

# Repository

```text
app/
  agents.py
  api.py
  compiler.py
  config.py
  connectors.py
  db.py
  domain.py
  evaluation.py
  main.py
  memory.py
  models.py
  planner.py
  policy.py
  protocols.py
  registry.py
  runtime.py
  security.py
  service.py
docs/
examples/
tests/
```

# Quick start

```bash
unzip meta-enterprise-agent-platform.zip
cd meta-enterprise-agent-platform
cp .env.example .env
docker compose build
docker compose up -d
docker compose ps
curl http://localhost:8000/health
```

Capabilities:

```bash
curl http://localhost:8000/v1/capabilities -H 'x-api-key: change-me'
```

Marketing goal:

```bash
curl -X POST http://localhost:8000/v1/goals  -H 'x-api-key: change-me'  -H 'Content-Type: application/json'  --data-binary @examples/marketing_goal.json
```

Commerce goal:

```bash
curl -X POST http://localhost:8000/v1/goals  -H 'x-api-key: change-me'  -H 'Content-Type: application/json'  --data-binary @examples/commerce_goal.json
```

Custom plan:

```bash
curl -X POST http://localhost:8000/v1/plans/execute  -H 'x-api-key: change-me'  -H 'Content-Type: application/json'  --data-binary @examples/custom_plan.json
```

# Host development

```bash
docker compose up -d postgres redis
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Change `.env` database and Redis hostnames from container names to `localhost`, then:

```bash
uvicorn app.main:app --reload
pytest -q
ruff check .
```

OpenAPI:

```text
http://localhost:8000/docs
```

# Database

```bash
docker compose exec postgres psql -U postgres -d agents
```

Useful tables:

```sql
SELECT * FROM runs;
SELECT * FROM steps;
SELECT * FROM approvals;
SELECT * FROM idempotency;
SELECT * FROM memory;
SELECT * FROM audit;
```

# Production target

```text
API / Goal Service
       |
Planner Service ---- Model Gateway
       |
DAG Compiler ---- Capability Registry ---- Policy PDP
       |
Distributed SQL
       |
Transactional Outbox
       |
Kafka / Pulsar
       |
+-----------+-----------+-----------+------------+
| Sales     | Support   | Commerce  | Marketing  |
| Workers   | Workers   | Workers   | Workers    |
+-----------+-----------+-----------+------------+
       |
MCP Gateway / Connector Plane ---- A2A Gateway
       |
Enterprise Systems
       |
Artifacts / Memory / Audit / OTel
       |
Evaluator + Replanner + Human Approval
```

## 1. Product applications

Customer support, product recommendation, lead qualification, appointment booking, sales assistance, marketing intelligence, business briefings, market research, product insights, calendar operations, competitive intelligence and cross-system business workflows.

## 2. Supervisor and specialist agents

The supervisor owns the goal and delegates domain work to Sales, Support, Commerce and Marketing agents. Specialist agents expose typed capabilities rather than unconstrained prompts.

## 3. Multi-layer memory

Working memory holds current execution context; session memory holds interaction continuity; episodic memory stores prior outcomes; semantic memory retrieves enterprise knowledge; entity memory stores structured business objects; procedural memory stores governed workflow preferences.

## 4. Durable long-running tasks

Accepted work must survive process restarts. Persist run, plan version, step states, external IDs, checkpoints and approvals. Dispatch through an outbox/event bus rather than relying on in-memory coroutines.

## 5. MCP connectors

Use MCP for governed agent-to-tool access. A gateway should enforce identity, tool allowlists, JSON schemas, policy, rate limits, audit, secrets, timeouts and observability.

## 6. A2A delegation

Use A2A for autonomous agent delegation. Track agent identity, capabilities, task lifecycle, deadlines, cancellation, artifact exchange, trust and callbacks.

## 7. Enterprise identity

Production identity includes human principal, tenant, workload, agent and connector identities. Tenant must come from trusted authentication claims.

## 8. RBAC and ABAC

RBAC grants coarse roles; ABAC evaluates tenant, resource, capability, data classification, environment and risk. Planning never grants authorization.

## 9. Approval workflows

High-impact writes pause before execution. Approval binds to a canonical hash of exact action parameters; changing the action invalidates approval.

## 10. Transactional state

Keep database transactions short and deterministic. Persist state transitions atomically with outbox events, then perform network calls outside the transaction.

## 11. Event streaming

Kafka/Pulsar carries dispatch, callbacks, audit export and evaluation events. Consumers are idempotent and partition keys preserve ordering where needed.

## 12. Multi-tenancy

Scope SQL, cache, queue, memory, artifacts, credentials, logs and metrics. Prevent cross-tenant IDs from becoming authorization inputs.

## 13. Observability

Trace goal -> planner -> specialist -> connector -> approval -> evaluator. Measure queue lag, step latency, failures, retries, approvals, model cost and business outcomes.

## 14. Idempotency

Use tenant + workflow + step + action-version scoped keys. Same key with different request hash is a conflict.

## 15. Ambiguous outcomes

If a provider may have executed before timeout, transition to UNKNOWN and reconcile against provider state rather than blindly retrying.

## 16. Worker leases and fencing

Workers claim tasks with lease expiry and monotonic fencing token. Late stale workers cannot commit results.

## 17. Checkpointing

Checkpoint completed steps, artifacts, external task IDs, memory references and pending approvals. Do not treat chat history as workflow truth.

## 18. Replanning

Failures, new evidence, policy denial or user changes can create a new plan version. Reuse valid completed artifacts; never replan around policy.

## 19. Agent evaluation

Measure goal completion, correct tool selection, permission compliance, artifact quality, recovery, human intervention, latency and cost.

## 20. Policy enforcement

Policy decisions are deterministic ALLOW/DENY/REQUIRE_APPROVAL/REQUIRE_SANDBOX outcomes. An LLM is not a policy decision point.

## 21. Prompt injection

Retrieved messages, tickets, web pages and connector outputs are untrusted data. They cannot modify system policy or authorize tools.

## 22. Connector security

Use allowlisted operations, least-privilege credentials, SSRF defenses, schema validation, output size limits, DLP and egress restrictions.

## 23. Model gateway

Centralize provider routing, model allowlists, cost, rate limits, privacy policy, prompt/version registry, fallback and telemetry.

## 24. Artifacts

Large generated reports/content belong in object storage with immutable IDs, hashes, classification, lineage and authorization.

## 25. Knowledge retrieval

Hybrid retrieval must apply authorization filters before content reaches a model. Vector stores are semantic retrieval, not authoritative business state.

## 26. Knowledge graph

Graph relationships such as Customer->Order, Lead->Account, Campaign->Audience and Ticket->Product can improve lineage and impact analysis.

## 27. Cost governance

Track tokens, model calls, connector calls, storage and worker compute per tenant/workflow. Enforce workflow and tenant budgets.

## 28. Backpressure

Bound active workflows, model concurrency, connector calls, agent fan-out and artifact bytes. Queue accepted work and shed low-priority new work under overload.

## 29. Cancellation

Propagate cancellation to queued/running tasks where supported. Already committed external side effects require compensation or reconciliation.

## 30. Saga compensation

Business workflows may need domain-specific compensating actions. Compensation is not database rollback.

## 31. Multi-region

Use tenant home region, data residency and tool locality. A step must have one authoritative execution owner.

## 32. Disaster recovery

Define RPO/RTO, back up SQL and artifact metadata, fence the old region after failover, reconcile external writes and resume only safe work.

## 33. CI/CD

Run lint, unit/property/contract tests, integration, SAST, dependency/SBOM/image scans, staging workflows, load/chaos/security tests and progressive deployment.

## 34. Kubernetes

Separate API/planner/scheduler/runtime/evaluator/reconciliation deployments; use workload identity, NetworkPolicy, HPA on queue lag, PDB and topology spread.

## 35. SLOs

Define goal acceptance, scheduler availability, queue start latency, connector success and durable-state-loss objectives. Long business workflows need separate completion SLOs.

## 36. Commerce agent

Catalog search and recommendations should be grounded in authoritative catalog/inventory/pricing tools. Never invent availability or price.

## 37. Sales agent

Lead qualification should combine explicit rules and evidence. Calendar booking is a consequential write and can require approval/idempotency.

## 38. Support agent

Read ticket/customer context, retrieve policy, draft a response, and hand off based on configured confidence/risk thresholds.

## 39. Marketing agent

Use analytics and governed campaign tools. Separate draft creation from campaign launch; launch is a high-impact mutation.

## 40. Human handoff

Support explicit human takeover. Persist handoff reason, context and ownership so the agent does not continue conflicting actions.

## 41. Measurement

Separate platform metrics from business metrics such as qualified leads, resolution rate, conversion, booking completion and human acceptance.

## 42. Privacy

Minimize customer data sent to models; use opaque IDs/aggregates when possible, encryption, retention, deletion and data-residency controls.

## 43. Threat model

Cover cross-tenant access, prompt/tool injection, data exfiltration, credential theft, replay, forged callbacks, approval substitution, SSRF, excessive agency and memory poisoning.

## 44. Local versus production

The repository is runnable with deterministic planning, mock connectors and API-key auth. Production requires enterprise identity, durable worker wiring and provider-specific connector implementations.


# Full production state machines

Run:

```text
CREATED -> PLANNING -> VALIDATING -> READY -> RUNNING
                                      |        |
                                      |        +-> WAITING_APPROVAL
                                      |        +-> WAITING_EXTERNAL
                                      |        +-> REPLANNING
                                      |        +-> FAILED
                                      |        +-> CANCELLED
                                      v
                                  COMPLETED
```

Step:

```text
PENDING -> READY -> RUNNING -> SUCCEEDED
                      |          |
                      |          +-> downstream ready
                      +-> FAILED
                      +-> UNKNOWN -> RECONCILING
                      +-> WAITING_APPROVAL
```

# Exactly-once reality

Global exactly-once execution cannot generally be promised across independent SaaS providers. Use:

```text
at-least-once delivery
+ scoped idempotency
+ provider request IDs
+ fencing
+ reconciliation
+ immutable audit
```

# Transactional outbox

```sql
BEGIN;
UPDATE steps SET status='READY' WHERE id=:id;
INSERT INTO outbox_events(event_type,payload) VALUES ('STEP_READY',:payload);
COMMIT;
```

The publisher retries independently. Consumers are idempotent.

# Memory architecture

```text
Working     current reasoning/execution context
Session     conversation continuity
Episodic    previous workflow outcomes
Semantic    retrieved enterprise knowledge
Entity      structured customer/business objects
Procedural  approved workflow preferences/patterns
```

Memory is context, not authorization.

# Agent evaluation

```text
Goal Completion
      +
Tool Correctness
      +
Grounding
      +
Policy Compliance
      +
Recovery
      +
Human Acceptance
      +
Latency / Cost
```

# 

> I separate probabilistic planning from deterministic execution. The planner emits a typed DAG over a governed capability registry. The compiler validates structure, while RBAC/ABAC and policy determine executable authority. Durable SQL plus an outbox and event bus provide recoverable orchestration. Specialist agents perform sales, support, commerce and marketing work through MCP/connector gateways; A2A handles delegation to autonomous agents. Consequential mutations are bound to human approval using canonical action hashes. External writes use idempotency and reconciliation because global exactly-once semantics do not exist across independent SaaS systems. Layered memory provides governed context, while evaluation, audit and observability make outcomes measurable and reconstructable.

# Production readiness checklist

```text
[ ] OIDC/workload identity
[ ] tenant derived from trusted claims
[ ] RBAC/ABAC
[ ] policy-as-code
[ ] durable scheduler/workers
[ ] transactional outbox
[ ] Kafka/Pulsar
[ ] idempotency table wired into execution
[ ] leases/fencing
[ ] UNKNOWN/reconciliation
[ ] cancellation/compensation
[ ] production MCP gateway
[ ] production A2A gateway
[ ] provider-specific connectors
[ ] secret manager/KMS
[ ] DLP/egress controls
[ ] OpenTelemetry
[ ] object storage
[ ] model gateway
[ ] Alembic migrations
[ ] Kubernetes
[ ] load/chaos/security tests
[ ] DR tests
```

# Important implementation boundary

This code is a substantive, runnable **production-oriented reference implementation**, not a claim that a generic ZIP can be dropped into any enterprise unchanged. Real production deployment depends on the organization's identity provider, Meta/WhatsApp/Instagram entitlements, Shopify/Zendesk/CRM contracts, schemas, secrets, data-residency rules, compliance requirements, SLOs and infrastructure.

# Final engineering principle

```text
Model       -> reason and propose
Planner     -> produce typed work
Compiler    -> validate dependencies
Policy      -> authorize
Runtime     -> own execution truth
Agents      -> perform domain work
MCP         -> governed tools
A2A         -> autonomous delegation
Approval    -> control consequential writes
Memory      -> provide governed context
Evaluator   -> verify outcomes
Audit       -> reconstruct everything
```

**The model reasons. The platform executes. Policy controls authority. Data systems remain authoritative. Humans retain control over consequential actions.**


# Extended Principal / Staff Engineering Guide

## 1. Product context and scope

This repository models an enterprise business-agent runtime: a governed platform that can interpret a business goal, construct a typed plan, delegate work to domain agents, invoke enterprise systems, pause for approvals, preserve state, evaluate results, and continue or re-plan.

It is deliberately broader than a customer-service chatbot. The same runtime can support customer conversations, commerce, sales, marketing, support, analytics, research, scheduling, internal operations, and long-running cross-system workflows.

The implementation is an independent reference architecture. It is not Meta proprietary source code.

## 2. End-to-end request lifecycle

```text
Business/User/Event
        |
        v
Authentication + Tenant Resolution
        |
        v
Goal Contract
        |
        v
Context + Governed Memory Retrieval
        |
        v
Planner
        |
        v
Typed Workflow DAG
        |
        v
Compiler / Static Validation
        |
        +----> Capability Registry
        +----> Policy / RBAC / ABAC
        |
        v
Durable Scheduler
        |
        v
Specialist Agent
        |
   +----+-----+
   |          |
  MCP        A2A
   |          |
Tool/System  Agent
   |          |
   +----+-----+
        |
        v
Artifact / Result
        |
        v
Evaluator
        |
 +------+------+------+
 |             |      |
PASS          RETRY  REPLAN
 |                    |
 v                    +----> new plan version
Approval if needed
 |
 v
External Action
 |
 v
Audit + Memory + Measurement
```

## 3. Why a typed plan is essential

The planner must not emit only natural-language intentions. A production runtime needs typed steps:

```json
{
  "key": "campaign_draft",
  "agent": "marketing",
  "capability": "marketing.campaign.draft",
  "kind": "skill",
  "depends_on": ["insights"],
  "risk": "WRITE",
  "input": {}
}
```

Typed plans enable validation, authorization, deterministic scheduling, testing, replay, cost accounting and audit.

## 4. Compiler responsibilities

A production compiler should validate:

```text
unique step keys
dependency existence
DAG acyclicity
capability existence
input schema
output compatibility
risk classification
policy constraints
region constraints
budget feasibility
deadline feasibility
protocol compatibility
```

The included compiler implements dependency and cycle correctness and provides the extension point for the remaining checks.

## 5. Workflow plan versioning

Never silently mutate an executing plan.

```text
Run
 |
 +-- Plan v1
 |     +-- research SUCCEEDED
 |     +-- campaign FAILED
 |
 +-- Plan v2
       +-- reuse research artifact
       +-- replacement campaign step
       +-- new validation step
```

Persist exact versions of plans, skills, prompts, models, policies and connectors used by every attempt.

## 6. Specialist-agent contract

A specialist agent should receive:

```text
goal fragment
typed input
dependency artifacts
permissions
deadline
budget
memory references
trace context
```

and return:

```text
status
typed output
evidence
artifacts
external IDs
cost
warnings
```

Specialist agents do not grant themselves new permissions.

## 7. Sales Agent

Typical capabilities:

```text
lead.read
lead.qualify
account.summarize
calendar.availability
appointment.propose
appointment.book
followup.draft
```

Read operations are lower risk. Booking, sending or changing CRM state are mutations requiring idempotency and potentially approval.

## 8. Support Agent

Typical flow:

```text
Customer message
      |
Ticket lookup
      |
Customer/order context
      |
Knowledge retrieval
      |
Policy retrieval
      |
Resolution reasoning
      |
Draft response
      |
Confidence/risk gate
   /             \
auto respond    human handoff
```

Never let retrieved ticket text or a customer message redefine system instructions.

## 9. Commerce Agent

Ground recommendations in authoritative catalog, inventory and pricing systems:

```text
intent
 |
catalog search
 |
eligibility/inventory
 |
ranking
 |
recommendation
 |
optional cart/action
```

An LLM should not invent current inventory, price or delivery promises.

## 10. Marketing Agent

```text
Business objective
      |
Analytics / insights
      |
Audience hypothesis
      |
Campaign draft
      |
Brand/policy validation
      |
Human approval
      |
Launch
      |
Measurement
      |
Optimization
```

Draft creation and campaign launch are separate security boundaries.

## 11. Supervisor Agent

The supervisor owns coordination, not every domain decision. Responsibilities:

```text
goal decomposition
capability selection
dependency management
progress interpretation
re-planning
human clarification
final synthesis
```

## 12. Capability Registry

Recommended capability metadata:

```text
capability ID
version
owner
agent
description
input schema
output schema
risk
required permissions
protocol
region
cost class
latency class
health
deprecation status
```

This registry bounds planner freedom.

## 13. Skills versus tools versus agents

```text
Skill
  reusable business capability/instruction package

MCP Tool
  governed operation/resource exposed to an agent

A2A Agent
  autonomous delegated worker with its own task lifecycle

Workflow Step
  one durable unit in the current execution plan
```

These abstractions should not be conflated.

## 14. MCP gateway architecture

```text
Agent
 |
MCP Client
 |
Enterprise MCP Gateway
 |
+ Authentication
+ Tenant binding
+ Authorization
+ Tool allowlist
+ Schema validation
+ DLP
+ Rate limiting
+ Approval check
+ Audit
+ Idempotency
+ Telemetry
 |
MCP Servers / Enterprise APIs
```

## 15. MCP execution envelope

A production gateway can internally normalize:

```json
{
  "tenant_id": "...",
  "principal_id": "...",
  "workflow_id": "...",
  "step_id": "...",
  "tool": "...",
  "arguments": {},
  "idempotency_key": "...",
  "deadline": "...",
  "trace_context": {}
}
```

Identity fields must come from trusted runtime context, not blindly from model output.

## 16. MCP discovery

Tool discovery should be cached using:

```text
tenant + server ID + server version
```

Invalidate on server/version/policy change. Do not expose every discovered tool automatically to every agent.

## 17. A2A gateway architecture

```text
Supervisor
 |
A2A Gateway
 |
Identity / Trust / Delegation Policy
 |
Agent Registry
 |
Remote Specialist Agent
 |
Task + Artifact lifecycle
```

A2A is appropriate when the remote component is an autonomous agent rather than a simple function.

## 18. A2A task lifecycle

```text
SUBMITTED
   |
ACCEPTED
   |
WORKING
  /   \
INPUT  AUTH_REQUIRED
  \   /
COMPLETED
 /    \
FAILED CANCELLED
```

Provider-specific states should map into a normalized internal state machine.

## 19. Delegation scope

Delegation grants should constrain:

```text
caller
callee
tenant
capabilities
resource scope
expiry
maximum risk
maximum cost
```

Delegated authority must never exceed caller authority.

## 20. Connector plane

Provider adapters translate internal capability contracts into provider-specific APIs. Each adapter owns:

```text
authentication
request schema
response mapping
provider error mapping
timeouts
rate limits
idempotency behavior
pagination
version compatibility
reconciliation
```

Generic HTTP wrappers are useful infrastructure but not sufficient for robust production integrations.

## 21. Shopify-style commerce integration

Production flow:

```text
Commerce Agent
 |
catalog capability
 |
Connector Gateway
 |
Shopify adapter
 |
product/catalog API
```

Use authoritative inventory and pricing responses.

## 22. Zendesk-style support integration

```text
Support Agent
 |
ticket.read / ticket.update
 |
Connector Gateway
 |
Zendesk adapter
```

Separate read credentials from write credentials where possible.

## 23. CRM integration

Expose approved business operations rather than arbitrary database access:

```text
lead.read
lead.qualify
account.read
opportunity.update
```

## 24. Calendar integration

Booking requires:

```text
fresh availability
exact participant/time
timezone
idempotency
approval when configured
provider confirmation
```

A timeout after booking can produce an ambiguous outcome and must be reconciled.

## 25. Meta messaging/channel integration

Messaging actions should distinguish:

```text
draft
preview
send
broadcast
campaign launch
```

The higher-impact operations require stronger authorization and policy.

## 26. Durable run state

Recommended run lifecycle:

```text
CREATED
 |
PLANNING
 |
VALIDATING
 |
READY
 |
RUNNING
 +---- WAITING_INPUT
 +---- WAITING_APPROVAL
 +---- WAITING_EXTERNAL
 +---- REPLANNING
 +---- CANCEL_REQUESTED
 |
COMPLETED / FAILED / CANCELLED
```

## 27. Durable step state

```text
PENDING
 |
READY
 |
RUNNING
 +---- WAITING_APPROVAL
 +---- WAITING_EXTERNAL
 +---- UNKNOWN
 |
SUCCEEDED / FAILED / CANCELLED
```

`UNKNOWN` is crucial for external side effects.

## 28. Transactional outbox

Never commit SQL state and publish a queue event as unrelated operations.

```text
BEGIN
 update workflow state
 insert outbox event
COMMIT
```

A publisher asynchronously sends the outbox record to Kafka/Pulsar.

## 29. Event bus

Recommended event types:

```text
RUN_CREATED
PLAN_COMPILED
STEP_READY
STEP_STARTED
STEP_SUCCEEDED
STEP_FAILED
STEP_UNKNOWN
APPROVAL_REQUESTED
APPROVAL_DECIDED
ARTIFACT_CREATED
REPLAN_REQUESTED
RUN_COMPLETED
```

## 30. Event envelope

```json
{
  "event_id": "...",
  "event_type": "STEP_SUCCEEDED",
  "tenant_id": "...",
  "run_id": "...",
  "step_id": "...",
  "sequence": 42,
  "occurred_at": "...",
  "payload": {},
  "trace_id": "..."
}
```

## 31. Partitioning

For per-workflow ordering:

```text
partition key = run_id
```

For very large fan-out workflows:

```text
partition key = run_id:user/shard
```

with an aggregation barrier.

## 32. Worker lease

```text
worker A acquires lease token 15
 |
lease expires
 |
worker B acquires token 16
 |
worker A returns late
```

Token 15 must be rejected from committing after token 16 owns the step.

## 33. Fencing

Persist monotonically increasing fencing tokens. Every state-changing worker write checks its token.

## 34. Idempotency

Recommended key scope:

```text
tenant
+ workflow
+ step
+ action version
```

Persist request hash and result reference.

Same key + different request hash = conflict.

## 35. Exactly-once limitation

Across independent SaaS APIs, global exactly-once cannot normally be guaranteed.

Use:

```text
at-least-once delivery
+ idempotency
+ provider request IDs
+ reconciliation
+ immutable audit
```

## 36. UNKNOWN and reconciliation

Example:

```text
POST appointment
        |
network timeout
        |
Did provider create it?
        |
      UNKNOWN
        |
Reconciliation worker
        |
GET provider by request ID
    /              \
created           absent
  |                 |
SUCCEEDED        retry safely
```

Never blindly repeat a consequential write after an ambiguous timeout.

## 37. Retry policy

Retry transport/transient failures only when safe.

Use exponential backoff with jitter and respect `Retry-After`.

Set maximum attempts and a global retry budget.

## 38. Circuit breaker

```text
CLOSED -> OPEN -> HALF_OPEN -> CLOSED
```

A failing connector should not cause thousands of agents to amplify an outage.

## 39. Bulkheads

Separate worker pools for:

```text
interactive reads
writes
browser/computer use
content generation
long analytics
reconciliation
```

## 40. Backpressure

Bound:

```text
active workflows
steps/run
parallel agent calls
model calls
connector calls
artifact bytes
queue age
```

Under overload, preserve accepted durable work and shed lower-priority new work.

## 41. Fair scheduling

Use tenant-aware weighted fair scheduling so a large tenant cannot starve smaller tenants.

## 42. Cancellation

Cancellation is itself durable:

```text
RUNNING -> CANCEL_REQUESTED -> CANCELLED
```

Already committed external actions may need compensation rather than cancellation.

## 43. Saga compensation

Example:

```text
create campaign
reserve budget
schedule launch
```

If scheduling fails, compensation might release budget and archive the draft. Compensation is a business action, not database rollback.

## 44. Human approval architecture

Approval record should contain:

```text
workflow
step
action summary
canonical action hash
risk
requester
required role
expiry
decision
approver
evidence
```

## 45. Action hash

Approval must bind to exact action semantics. If audience, budget, recipient, content, destination or schedule changes, generate a new hash and invalidate the old approval.

## 46. Separation of duties

For sensitive operations, policy can prevent the requester from also being the sole approver.

## 47. Approval expiration

Stale approvals must not authorize changed or outdated actions.

## 48. Human clarification

If required business context cannot safely be inferred:

```text
workflow -> WAITING_INPUT
```

The human response becomes a durable event.

## 49. Conversation versus workflow

```text
Conversation = interaction surface
Workflow     = durable execution object
```

One conversation can create multiple workflows, and a workflow can outlive a chat session.

## 50. Multi-layer memory architecture

```text
Working
Session
Episodic
Semantic
Entity
Procedural
```

Each layer has different retention, authority and storage characteristics.

## 51. Working memory

Temporary execution context:

```text
current goal
plan
recent step outputs
temporary calculations
```

It can be reconstructed from durable state where possible.

## 52. Session memory

Conversation continuity within a bounded interaction/session.

## 53. Episodic memory

Previous workflow outcomes:

```text
campaign X required legal review
customer preferred handoff
workflow Y failed due to connector outage
```

Store evidence and timestamps.

## 54. Semantic memory

Knowledge retrieval from documents, policies and business content. Usually hybrid lexical/vector retrieval with authorization filtering.

## 55. Entity memory

Structured facts about business entities:

```text
account
lead
ticket
product
campaign
```

Authoritative systems remain the source of truth.

## 56. Procedural memory

Governed reusable preferences/patterns, for example:

```text
team requires brand review before campaign approval
```

It cannot override security policy.

## 57. Memory write gate

```text
candidate
 |
classification
 |
scope
 |
policy
 |
dedup/conflict
 |
persist
```

Do not persist every model observation automatically.

## 58. Memory conflict

Define explicit precedence:

```text
security/policy
> organization
> team/project
> user preference
> inferred preference
```

## 59. Memory deletion

Delete primary record, semantic index, caches and derived personalization as required by policy.

## 60. RAG architecture

```text
Query
 |
Identity / Authorization
 |
Hybrid Retrieval
 |
Metadata filters
 |
Reranker
 |
Source validation
 |
Model context
```

Authorization filtering happens before content reaches the model.

## 61. Knowledge graph

Useful relationships:

```text
Customer -> owns -> Order
Lead -> belongs_to -> Account
Ticket -> concerns -> Product
Campaign -> targets -> Audience
Campaign -> uses -> Creative
```

## 62. Artifact service

Large outputs belong outside workflow rows:

```text
artifact_id
tenant
workflow
type
version
hash
classification
storage URI
lineage
```

## 63. Artifact immutability

Editing creates a new version. Approval references an immutable artifact hash/version.

## 64. Enterprise identity model

Represent:

```text
human principal
tenant
service workload
agent identity
connector identity
delegated identity
```

## 65. OIDC

Production API should validate issuer, audience, signature, expiry and trusted tenant claims.

## 66. Workload identity

Internal services use workload identity/mTLS rather than shared long-lived API keys.

## 67. RBAC

Example roles:

```text
viewer
operator
campaign_manager
support_agent
approver
tenant_admin
```

## 68. ABAC

Attributes:

```text
tenant
resource owner
region
risk
data classification
environment
capability
channel
```

## 69. Policy decision point

Return structured outcomes:

```text
ALLOW
DENY
REQUIRE_APPROVAL
REQUIRE_SANDBOX
REQUIRE_REDACTION
```

## 70. Policy is not an LLM task

Models can summarize policy, but deterministic policy infrastructure grants authority.

## 71. Secret management

Use KMS/Vault/cloud secret manager. Secrets should never appear in prompts, memory, logs, traces or artifacts.

## 72. Short-lived credentials

Workers should receive scoped, short-lived credentials or credential references for the exact operation.

## 73. DLP

Before model/tool dispatch:

```text
classify
 |
redact/tokenize
 |
destination policy
 |
dispatch
```

## 74. Prompt injection

Tool results, support tickets, webpages and documents are untrusted data.

Embedded instructions cannot grant permissions or alter system policy.

## 75. Indirect prompt injection

Treat retrieved content as data with explicit delimiters/structured parsing and tool authorization independent of model instructions.

## 76. Tool injection

Never dynamically trust a tool because its description claims it is safe. Registry admission is administrative/security-controlled.

## 77. SSRF

For URL-capable connectors:

```text
destination allowlist
DNS/IP validation
private-range blocking
redirect revalidation
metadata endpoint denial
```

## 78. Code execution

Generated code requires an isolated sandbox with resource limits, restricted network, ephemeral filesystem and no host secrets.

## 79. Computer/browser use

Use ephemeral sessions, domain allowlists, download scanning and human confirmation for consequential actions.

## 80. Multi-tenancy

Tenant isolation must cover:

```text
SQL
cache
queue
vector search
object storage
memory
secrets
logs
traces
connector credentials
```

## 81. Database tenant isolation

Use tenant-scoped queries and optionally database row-level security as defense in depth.

## 82. Cache isolation

Cache keys include tenant and authorization-sensitive dimensions.

## 83. Queue isolation

Every event carries trusted tenant identity; consumers validate it against durable workflow state.

## 84. Model gateway

```text
Agents
 |
Model Gateway
 |
+ routing
+ allowlist
+ privacy policy
+ token budget
+ rate limits
+ fallback
+ prompt registry
+ telemetry
 |
Approved Models
```

## 85. Model routing

Select based on:

```text
task
quality requirement
latency
cost
data classification
region
availability
```

## 86. Model fallback

Fallback only to models compatible with the same security/data constraints.

## 87. Structured model output

Planner/evaluator output must validate against JSON/Pydantic schemas before entering control flow.

## 88. Prompt registry

Version system prompts, planner prompts, evaluator prompts and tool descriptions. Attach versions to workflow traces.

## 89. Agent evaluation

Evaluate:

```text
goal completion
tool selection
grounding
policy compliance
handoff correctness
recovery
latency
cost
human acceptance
```

## 90. Evaluation hierarchy

```text
L0 schema validation
L1 deterministic business rules
L2 evidence/source consistency
L3 model-based quality judge
L4 human acceptance
L5 real business outcome
```

## 91. Offline evaluation

Maintain a versioned goal corpus with expected capabilities, forbidden operations, required approvals and outcome criteria.

## 92. Online evaluation

Measure real outcomes while separating agent quality from external factors.

## 93. Model confidence

A model saying it is confident does not prove an external action occurred. Provider state is authoritative.

## 94. Observability

Use:

```text
OpenTelemetry traces
structured logs
Prometheus-compatible metrics
workflow audit
business outcome events
```

## 95. Trace propagation

Propagate W3C trace context through HTTP, event bus, MCP and A2A calls.

## 96. Metrics

Platform:

```text
goal acceptance rate
queue lag
step latency
connector errors
retry rate
UNKNOWN count
approval wait
replan rate
model cost
```

Business:

```text
resolution rate
qualified leads
bookings
conversion
campaign outcome
human acceptance
```

## 97. Cardinality

Do not use workflow ID, customer ID or prompt text as metric labels. Put them in traces/logs with access controls.

## 98. Audit

Audit:

```text
who
tenant
what capability
resource
policy decision
approval
tool/agent
action hash
artifact IDs
timestamp
result
```

## 99. Audit immutability

Export compliance-relevant audit to append-only/WORM-compatible storage where required.

## 100. Privacy

Minimize customer data sent to models. Prefer opaque IDs, aggregates and scoped retrieved fields.

## 101. Data residency

Capability and model registries should record residency constraints; planner selection cannot override them.

## 102. Retention

Different retention classes for:

```text
workflow state
audit
memory
traces
artifacts
customer-derived data
```

## 103. Data deletion

Deletion workflows must traverse SQL, object storage, vector indexes, caches and memory.

## 104. Production service decomposition

```text
services/
  api
  goal
  planner
  compiler
  scheduler
  runtime-worker
  sales-worker
  support-worker
  commerce-worker
  marketing-worker
  approval
  reconciliation
  evaluator
  registry
  memory
  mcp-gateway
  a2a-gateway
  audit-exporter
```

## 105. Database tables

Recommended:

```text
runs
plan_versions
steps
step_attempts
approvals
idempotency_keys
outbox_events
workflow_events
skills
agents
mcp_servers
connectors
delegation_grants
artifacts
memory_records
audit_events
```

## 106. Database indexes

Examples:

```text
steps(status, not_before)
steps(run_id, step_key)
outbox_events(published_at, created_at)
approvals(status, created_at)
memory_records(tenant_id, scope, subject)
audit_events(run_id, created_at)
```

## 107. Transaction boundaries

Correct:

```text
BEGIN
claim/update state
insert audit/outbox
COMMIT

network call

BEGIN
record result
insert next outbox
COMMIT
```

Do not hold SQL transactions open during LLM/SaaS calls.

## 108. Alembic

The local reference uses `create_all()` for easy startup.

Production should use Alembic and expand/contract migrations.

## 109. Object storage

Store reports, generated assets and large evidence packages with opaque object keys and integrity hashes.

## 110. Redis

Good uses:

```text
short-lived cache
rate limits
ephemeral coordination
```

Do not make Redis the only durable workflow state.

## 111. Kafka/Pulsar

Use for asynchronous dispatch and events, not as the sole queryable workflow database.

## 112. Kubernetes

```text
Ingress/API
 |
Control Plane
 |
SQL / Redis / Kafka
 |
Worker Deployments
 |
MCP/A2A Gateways
 |
Artifact Store
```

Use HPA, PDB, topology spread, NetworkPolicy and workload identity.

## 113. Autoscaling

Scale workers using queue lag, oldest task age and resource utilization rather than CPU alone.

## 114. Multi-region

Route using tenant home region, data residency and connector locality. Avoid two regions executing the same step concurrently.

## 115. Disaster recovery

After failover:

```text
fence old workers
restore/confirm authoritative state
replay unpublished events
reconcile external actions
resume safe work
```

## 116. RPO and RTO

Define separately for workflow state, audit, memory and artifacts.

## 117. Capacity planning

Example:

```text
100,000 goals/day
x 8 steps/goal
= 800,000 step executions/day
```

Model separately:

```text
planner QPS
model QPS/tokens
connector QPS
queue throughput
SQL writes
artifact bandwidth
```

## 118. Cost accounting

Workflow cost:

```text
planner tokens
+ specialist model tokens
+ tool/API charges
+ worker compute
+ artifact storage
```

Persist estimated and actual cost.

## 119. Cost budgets

Support per-workflow, user, team and tenant budgets. Budget is a planner constraint and runtime enforcement boundary.

## 120. Infinite-loop prevention

Set:

```text
max replans
max steps
max model calls
max elapsed time
max cost
```

## 121. CI pipeline

```text
lint
unit tests
property tests
contract tests
integration tests
SAST
dependency scan
SBOM
container scan/sign
staging workflows
load smoke
```

## 122. Property tests

Important invariants:

```text
child never executes before dependencies
unapproved high-risk action never executes
same idempotency action cannot duplicate logical write
tenant A cannot access tenant B state
stale fencing token cannot commit
```

## 123. Contract tests

For each connector/MCP/A2A adapter test auth, request/response schema, timeout, errors, cancellation, idempotency and version compatibility.

## 124. Load testing

Test many small chats/goals, huge fan-out workflows, slow providers, approval backlogs and post-outage bursts.

## 125. Chaos testing

Inject:

```text
worker death
DB failover
event duplication
Redis loss
provider timeout
model outage
gateway restart
```

Verify correctness, not just availability.

## 126. Progressive delivery

```text
internal
 -> canary tenants
 -> percentage rollout
 -> broad release
```

Monitor quality and policy outcomes as well as HTTP health.

## 127. Feature flags

Useful for planner model, new skill, connector, evaluator, memory strategy and protocol adapter.

## 128. Backward compatibility

An in-flight workflow may reference an older skill/model/schema version. Persist exact versions until it completes.

## 129. SLO examples

Illustrative engineering targets, not Meta claims:

```text
API availability       99.9%
accepted-state loss    0 after durable commit
scheduler start p95    < 10 s
read workflow p95      < 500 ms
```

Business workflow completion needs separate, longer SLOs.

## 130. Operational dashboard

Display:

```text
active runs
queue lag
oldest task
step throughput
failure/retry/UNKNOWN
approval backlog
connector health
model latency/cost
replan rate
```

## 131. Alerting

Alert on sustained queue age, failure spikes, reconciliation backlog, DB saturation, connector outage and invalid model output.

## 132. Incident: stuck workflow

1. inspect run/plan version;
2. locate oldest nonterminal step;
3. inspect lease and worker;
4. inspect external provider;
5. check approval/input;
6. reconcile UNKNOWN;
7. requeue only if safe;
8. preserve audit.

## 133. Incident: connector outage

1. open circuit;
2. stop retry amplification;
3. preserve queued work;
4. use only approved fallback;
5. communicate degraded state;
6. resume gradually;
7. reconcile ambiguous writes.

## 134. Incident: compromised connector

1. disable registry entry;
2. revoke/rotate credentials;
3. block egress;
4. inspect recent calls;
5. preserve audit;
6. assess data/action impact;
7. security-review before re-enable.

## 135. Incident: policy defect

1. disable affected capability;
2. stop new dispatch;
3. identify workflows/policy version;
4. inspect external effects;
5. patch and regression-test;
6. controlled resume.

## 136. Application: customer service

```text
Message
 -> identity/context
 -> ticket
 -> knowledge
 -> resolution
 -> draft
 -> policy
 -> respond/handoff
```

## 137. Application: product recommendation

```text
Customer intent
 -> catalog retrieval
 -> inventory/eligibility
 -> ranking
 -> explanation
 -> optional commerce action
```

## 138. Application: lead qualification

```text
Inbound lead
 -> CRM context
 -> qualification rules
 -> enrichment
 -> score/evidence
 -> next action
 -> sales handoff
```

## 139. Application: appointment booking

```text
Intent
 -> availability
 -> proposed slot
 -> confirmation
 -> booking write
 -> provider confirmation
```

## 140. Application: morning business briefing

```text
overnight conversations
 + sales/support signals
 + analytics
 -> prioritization
 -> concise briefing
 -> suggested actions
```

## 141. Application: market research

```text
business question
 -> research plan
 -> governed sources
 -> extraction
 -> evidence
 -> synthesis
 -> report
```

## 142. Application: product insights

Combine catalog, conversation and analytics signals while respecting source permissions and data classification.

## 143. Application: competitive intelligence

Use governed public/enterprise sources, source citations and explicit uncertainty. Do not allow web content to authorize tools.

## 144. Application: marketing operations

```text
goal
 -> insights
 -> campaign draft
 -> approval
 -> launch
 -> measurement
 -> recommendation
```

## 145. Application: internal operations

The same runtime can coordinate CRM, project-management, documents, calendar and analytics tools.

## 146. Application: long-running business project

A project owns persistent context, artifacts and milestones; workflows are individual execution phases within the project.

## 147. Agent-to-agent collaboration

Example:

```text
Supervisor
 |
+ Sales Agent
|   + CRM tool
|
+ Commerce Agent
|   + catalog tool
|
+ Marketing Agent
    + external analytics agent via A2A
```

## 148. Replanning

Evaluator can return:

```json
{
  "decision": "REPLAN",
  "findings": ["campaign lacks required evidence"],
  "preserve_steps": ["insights"]
}
```

The planner generates a new version; completed valid artifacts are reused.

## 149. Evaluator design

Evaluation input:

```text
goal
success criteria
plan
step outputs
artifacts
policy findings
evidence
```

Output:

```text
PASS
RETRY
REPLAN
HUMAN
```

## 150. Evidence grounding

Every important business conclusion should reference authoritative source/tool artifacts rather than model recollection.

## 151. Human handoff

Persist:

```text
reason
owner
priority
context/artifacts
what the agent already attempted
```

Once handed off, agent actions must obey ownership rules.

## 152. Business outcome feedback

Feedback can improve evaluation datasets, but a single user correction should not silently rewrite global behavior.

## 153. Safe learning loop

```text
feedback
 -> candidate improvement
 -> offline evaluation
 -> review
 -> versioned release
```

## 154. Local code walkthrough: `domain.py`

Defines the typed external contracts: goals, steps, plans and connector calls.

## 155. Local code walkthrough: `planner.py`

Provides a deterministic planner so the repository runs without an external model key. Production can implement the same planner interface using structured model output.

## 156. Local code walkthrough: `compiler.py`

Builds a directed graph, rejects duplicate/missing dependencies and cycles.

## 157. Local code walkthrough: `agents.py`

Contains executable Sales, Support, Commerce and Marketing specialist adapters.

## 158. Local code walkthrough: `registry.py`

Defines the bounded capability catalog and risk metadata.

## 159. Local code walkthrough: `connectors.py`

Provides runnable local provider-style mocks. Production replaces these with authenticated, contract-tested adapters.

## 160. Local code walkthrough: `protocols.py`

Implements the MCP/A2A integration boundary and a mock mode for local execution.

## 161. Local code walkthrough: `policy.py`

Implements a simple deterministic risk gate. Replace with enterprise PDP/OPA/Cedar-style infrastructure.

## 162. Local code walkthrough: `security.py`

Provides local API-key authentication and canonical SHA-256 action hashing.

## 163. Local code walkthrough: `runtime.py`

Validates the DAG, executes ready steps, passes dependency outputs, enforces approval requirements and routes skill/MCP/A2A/evaluator steps.

## 164. Local code walkthrough: `memory.py`

Implements the six memory namespaces as a runnable foundation. Production persists them with scope, provenance, authorization and retention.

## 165. Local code walkthrough: `evaluation.py`

Implements deterministic workflow result evaluation foundation.

## 166. Local code walkthrough: `models.py`

Defines durable SQL entities for runs, steps, approvals, idempotency, memory and audit. A production v2 should wire every runtime transition to these models.

## 167. Local code walkthrough: `service.py`

Coordinates goal -> planner -> runtime.

## 168. Local code walkthrough: `api.py`

Exposes capabilities, goals, direct plan execution and connector calls.

## 169. Local code walkthrough: `main.py`

Bootstraps FastAPI and initializes the local schema.

## 170. Important code boundary

The current repository is a runnable production-oriented reference, but its local runtime executes primarily in-process. The full distributed architecture described above requires wiring the models to scheduler/worker/outbox/event-bus services.

That distinction is intentional and documented rather than hidden.

## 171. Production upgrade sequence

Recommended order:

```text
1 enterprise OIDC
2 persisted run/step transitions
3 Alembic
4 transactional outbox
5 Kafka/Pulsar
6 scheduler + workers
7 idempotency
8 leases/fencing
9 UNKNOWN/reconciliation
10 approval resume API
11 production MCP gateway
12 provider connectors
13 A2A gateway
14 persistent governed memory
15 OTel
16 Kubernetes
17 load/chaos/security/DR validation
```

## 172. Full local run instructions

```bash
unzip meta-enterprise-agent-platform-comprehensive.zip
cd meta-enterprise-agent-platform

cp .env.example .env

docker compose build
docker compose up -d
docker compose ps

curl http://localhost:8000/health
```

Capabilities:

```bash
curl http://localhost:8000/v1/capabilities \
  -H 'x-api-key: change-me'
```

Marketing:

```bash
curl -X POST http://localhost:8000/v1/goals \
  -H 'x-api-key: change-me' \
  -H 'Content-Type: application/json' \
  --data-binary @examples/marketing_goal.json
```

Commerce:

```bash
curl -X POST http://localhost:8000/v1/goals \
  -H 'x-api-key: change-me' \
  -H 'Content-Type: application/json' \
  --data-binary @examples/commerce_goal.json
```

Custom DAG:

```bash
curl -X POST http://localhost:8000/v1/plans/execute \
  -H 'x-api-key: change-me' \
  -H 'Content-Type: application/json' \
  --data-binary @examples/custom_plan.json
```

Open:

```text
http://localhost:8000/docs
```

## 173. Host-development instructions

```bash
docker compose up -d postgres redis

python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
```

Change `.env` container hostnames `postgres` and `redis` to `localhost`, then:

```bash
uvicorn app.main:app --reload
```

## 174. Tests

```bash
pytest -q
ruff check .
```

The tests cover compiler correctness, planner approval behavior, memory layers and canonical action hashing.

## 175. Database inspection

```bash
docker compose exec postgres psql -U postgres -d agents
```

Then:

```sql
\dt
SELECT * FROM runs;
SELECT * FROM steps;
SELECT * FROM approvals;
SELECT * FROM idempotency;
SELECT * FROM memory;
SELECT * FROM audit;
```

## 176. Logs

```bash
docker compose logs -f api
docker compose logs -f postgres
docker compose logs -f redis
```

## 177. Stop

```bash
docker compose down
```

Delete local volumes:

```bash
docker compose down -v
```

## 178. Troubleshooting: database connection

Inside Docker, use hostname `postgres`.

When running FastAPI directly on the host, use `localhost`.

## 179. Troubleshooting: 401

Verify the `x-api-key` header matches `.env`.

## 180. Troubleshooting: plan compilation

Common causes:

```text
duplicate step key
unknown dependency
cycle
invalid Pydantic enum/value
```

## 181. Troubleshooting: MCP/A2A

The default `CONNECTOR_MODE=mock` keeps the project runnable without external gateways. To use real endpoints, implement provider/protocol contracts, configure authentication and add contract tests.

## 182. Troubleshooting: campaign waits for approval

This is expected. Campaign launch is intentionally modeled as a high-risk action. A production implementation should persist approval, expose decision APIs and resume the durable workflow.

## 183. Principal-level design summary

```text
I use an LLM only where probabilistic reasoning is useful. It emits a typed plan over a governed capability registry. A deterministic compiler validates that plan, and policy—not the model—decides authority. SQL is the source of truth for durable workflow state; an outbox and event bus connect it to leased/fenced workers. Specialist agents use MCP for tools and A2A for autonomous delegation. External writes are idempotent and can enter UNKNOWN for reconciliation because global exactly-once execution across SaaS systems is not realistic. Consequential actions bind human approval to a canonical action hash. Memory is layered and governed but never becomes authorization. Evaluation, audit and OpenTelemetry make the system measurable and reconstructable.
```

## 184. Whiteboard architecture

```text
Client / Messaging / Event
          |
      API Gateway
          |
   Goal / Identity
          |
      Planner
          |
     Typed DAG
          |
  Compiler + Policy
          |
   Durable Scheduler
          |
       Event Bus
          |
 +--------+--------+---------+----------+
 | Sales  |Support |Commerce |Marketing |
 +--------+--------+---------+----------+
          |
  Skills / MCP / A2A
          |
 Enterprise Systems
          |
 Artifacts + Memory
          |
       Evaluator
          |
 Approval / Replan
          |
     Audit + OTel
```

## 185. Final architecture principle

The anti-pattern is:

```text
user -> giant LLM -> unrestricted enterprise APIs
```

The production pattern is:

```text
goal
 -> bounded reasoning
 -> typed plan
 -> deterministic validation
 -> policy
 -> durable execution
 -> governed capabilities
 -> evidence
 -> evaluation
 -> human control at consequential boundaries
```

The model proposes. The compiler validates. Policy authorizes. The runtime owns truth. External systems remain authoritative. Humans retain control of consequential actions.
