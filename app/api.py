from fastapi import APIRouter,Depends,HTTPException
from app.security import auth
from app.domain import GoalRequest,Plan,ConnectorCall
from app.registry import all_capabilities
from app.service import AgentPlatform
from app.runtime import Runtime
from app.connectors import call
router=APIRouter(prefix="/v1",dependencies=[Depends(auth)])
@router.get("/capabilities")
async def capabilities():return {"capabilities":all_capabilities()}
@router.post("/goals")
async def goals(r:GoalRequest):return await AgentPlatform().goal(r)
@router.post("/plans/execute")
async def execute(p:Plan):
 try:return {"outputs":await Runtime().execute(p)}
 except ValueError as e:raise HTTPException(400,str(e))
@router.post("/connectors/call")
async def connector(c:ConnectorCall):return await call(c.connector,c.operation,c.arguments,c.dry_run)
