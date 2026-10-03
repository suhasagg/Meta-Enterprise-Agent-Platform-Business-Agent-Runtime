from app.planner import Planner
from app.runtime import Runtime
class AgentPlatform:
 async def goal(self,req):
  p=Planner().plan(req.goal,req.context);out=await Runtime().execute(p,req.principal_id,req.tenant_id)
  status="WAITING_APPROVAL" if any(isinstance(v,dict) and v.get("status")=="WAITING_APPROVAL" for v in out.values()) else "COMPLETED"
  return {"status":status,"goal":req.goal,"plan":p.model_dump(),"outputs":out}
