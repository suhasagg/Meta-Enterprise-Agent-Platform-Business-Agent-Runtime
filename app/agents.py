from app.connectors import call
class SalesAgent:
 async def run(self,cap,payload):
  if cap=="crm.lead.read":return await call("crm","lead.read",payload)
  if cap=="crm.lead.qualify":return {"status":"DRAFT","qualification":{"score":80,"next_action":"human-reviewed follow-up"}}
  return {"status":"OK"}
class SupportAgent:
 async def run(self,cap,payload):
  if cap=="support.ticket.read":return await call("zendesk","ticket.read",payload)
  return {"status":"DRAFT","reply":"Thanks for contacting us. A support specialist can review this proposed response."}
class CommerceAgent:
 async def run(self,cap,payload):
  if cap=="catalog.search":return await call("shopify","catalog.search",payload)
  return {"status":"OK","recommendations":[{"sku":"SKU-1","reason":"matches supplied constraints"}]}
class MarketingAgent:
 async def run(self,cap,payload):
  if cap=="marketing.insights":return await call("meta","marketing.insights",payload)
  if cap=="marketing.campaign.draft":return {"status":"DRAFT","campaign":{"objective":"growth","creative":"draft","audience":"draft"}}
  return {"status":"OK"}
AGENTS={"sales":SalesAgent(),"support":SupportAgent(),"commerce":CommerceAgent(),"marketing":MarketingAgent()}
