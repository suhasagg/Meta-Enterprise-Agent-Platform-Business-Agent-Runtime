def authorize(step,principal,tenant):
 if not tenant:return {"decision":"DENY","reason":"missing tenant"}
 if step.risk=="HIGH":return {"decision":"REQUIRE_APPROVAL","reason":"consequential external action"}
 return {"decision":"ALLOW","reason":"capability allowed by reference policy"}
