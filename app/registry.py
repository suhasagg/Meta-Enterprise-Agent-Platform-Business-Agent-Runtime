CAPABILITIES={
"crm.lead.read":{"agent":"sales","risk":"READ"},"crm.lead.qualify":{"agent":"sales","risk":"WRITE"},
"support.ticket.read":{"agent":"support","risk":"READ"},"support.ticket.draft":{"agent":"support","risk":"WRITE"},
"catalog.search":{"agent":"commerce","risk":"READ"},"commerce.recommend":{"agent":"commerce","risk":"READ"},
"calendar.availability":{"agent":"sales","risk":"READ"},"calendar.book":{"agent":"sales","risk":"HIGH"},
"marketing.insights":{"agent":"marketing","risk":"READ"},"marketing.campaign.draft":{"agent":"marketing","risk":"WRITE"},
"marketing.campaign.launch":{"agent":"marketing","risk":"HIGH"},"external.delegate":{"agent":"supervisor","risk":"WRITE"}}
def all_capabilities():return [{"name":k,**v} for k,v in CAPABILITIES.items()]
