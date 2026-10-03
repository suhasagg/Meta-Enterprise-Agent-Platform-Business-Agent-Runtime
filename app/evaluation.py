def evaluate(outputs):
 blocked=[k for k,v in outputs.items() if isinstance(v,dict) and v.get("status") in {"FAILED","BLOCKED"}]
 return {"decision":"PASS" if not blocked else "REPLAN","blocking_steps":blocked,"evidence_steps":list(outputs)}
