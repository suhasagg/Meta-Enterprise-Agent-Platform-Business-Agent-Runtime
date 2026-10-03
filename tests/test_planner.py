from app.planner import Planner
def test_marketing_approval():
 p=Planner().plan("launch a marketing campaign",{})
 assert any(x.kind=="approval" for x in p.steps)
