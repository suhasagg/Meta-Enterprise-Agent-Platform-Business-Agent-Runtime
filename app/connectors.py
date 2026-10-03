from app.config import settings
async def call(connector,operation,args,dry_run=True):
 if dry_run or settings.connector_mode=="mock":
  samples={
   "shopify":{"catalog.search":{"products":[{"sku":"SKU-1","name":"Example Product","price":99}]}},
   "zendesk":{"ticket.read":{"ticket":{"id":"T-1","status":"open","summary":"Example support issue"}}},
   "crm":{"lead.read":{"lead":{"id":"L-1","score":72,"stage":"new"}}},
   "calendar":{"availability":{"slots":["2026-10-05T10:00:00","2026-10-05T15:00:00"]}}},
   "meta":{"marketing.insights":{"summary":{"conversations":1200,"qualified_leads":180}}}
  }
  return {"status":"DRY_RUN" if dry_run else "MOCK","connector":connector,"operation":operation,
          "data":samples.get(connector,{}).get(operation,{"ok":True,"arguments":args})}
 raise RuntimeError("live connector adapters require organization credentials and provider-specific implementation")
