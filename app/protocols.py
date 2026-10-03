import httpx
from app.config import settings
async def mcp_call(name,args):
 if settings.connector_mode=="mock":return {"status":"MOCK","protocol":"MCP","tool":name,"result":{"accepted":True}}
 async with httpx.AsyncClient(timeout=30) as c:
  r=await c.post(f"{settings.mcp_gateway_url}/tools/call",json={"name":name,"arguments":args});r.raise_for_status();return r.json()
async def a2a_delegate(capability,args):
 if settings.connector_mode=="mock":return {"status":"MOCK","protocol":"A2A","capability":capability,"artifact":{"summary":"delegated result"}}
 async with httpx.AsyncClient(timeout=30) as c:
  r=await c.post(f"{settings.a2a_gateway_url}/tasks",json={"capability":capability,"input":args});r.raise_for_status();return r.json()
