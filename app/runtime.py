from app.compiler import compile_plan
from app.policy import authorize
from app.security import action_hash
from app.agents import AGENTS
from app.protocols import mcp_call,a2a_delegate
from app.evaluation import evaluate
class Runtime:
 async def execute(self,plan,principal="local",tenant="acme",approved=None):
  approved=set(approved or []);compile_plan(plan);pending={s.key:s for s in plan.steps};done={}
  while pending:
   ready=[s for s in pending.values() if all(d in done for d in s.depends_on)]
   if not ready:raise RuntimeError("dependency deadlock")
   for s in ready:
    pol=authorize(s,principal,tenant)
    if s.kind=="approval":
     h=action_hash({"capability":s.capability,"input":s.input,"dependencies":s.depends_on})
     done[s.key]={"status":"APPROVED" if s.key in approved else "WAITING_APPROVAL","action_hash":h}
    elif pol["decision"]=="REQUIRE_APPROVAL" and not any(done.get(d,{}).get("status")=="APPROVED" for d in s.depends_on):
     done[s.key]={"status":"BLOCKED","reason":"approval required"}
    elif s.kind=="mcp":done[s.key]=await mcp_call(s.capability,s.input)
    elif s.kind=="a2a":done[s.key]=await a2a_delegate(s.capability,s.input)
    elif s.kind=="evaluate":done[s.key]=evaluate(done)
    else:
     agent=AGENTS.get(s.agent);done[s.key]=await agent.run(s.capability,s.input|{"dependency_outputs":{d:done[d] for d in s.depends_on}})
    del pending[s.key]
  return done
