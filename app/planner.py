from app.domain import Plan,StepSpec
class Planner:
 def plan(self,goal,ctx):
  g=goal.lower();s=[]
  if any(x in g for x in ["lead","sales","appointment"]):
   s += [StepSpec(key="lead",agent="sales",capability="crm.lead.read"),
         StepSpec(key="qualify",agent="sales",capability="crm.lead.qualify",depends_on=["lead"],risk="WRITE")]
  if any(x in g for x in ["support","ticket","customer issue"]):
   s += [StepSpec(key="ticket",agent="support",capability="support.ticket.read"),
         StepSpec(key="support_draft",agent="support",capability="support.ticket.draft",depends_on=["ticket"],risk="WRITE")]
  if any(x in g for x in ["product","shop","commerce","recommend"]):
   s += [StepSpec(key="catalog",agent="commerce",capability="catalog.search"),
         StepSpec(key="recommend",agent="commerce",capability="commerce.recommend",depends_on=["catalog"])]
  if any(x in g for x in ["marketing","campaign","growth"]):
   s += [StepSpec(key="insights",agent="marketing",capability="marketing.insights"),
         StepSpec(key="campaign_draft",agent="marketing",capability="marketing.campaign.draft",depends_on=["insights"],risk="WRITE"),
         StepSpec(key="approval",agent="supervisor",capability="marketing.campaign.launch",kind="approval",depends_on=["campaign_draft"],risk="HIGH"),
         StepSpec(key="launch",agent="marketing",capability="marketing.campaign.launch",kind="mcp",depends_on=["approval"],risk="HIGH")]
  if not s:s=[StepSpec(key="research",agent="supervisor",capability="external.delegate",kind="a2a",input={"goal":goal},risk="WRITE")]
  s.append(StepSpec(key="evaluate",agent="supervisor",capability="workflow.evaluate",kind="evaluate",depends_on=[s[-1].key]))
  return Plan(objective=goal,steps=s)
