import networkx as nx
def compile_plan(plan):
 keys={x.key for x in plan.steps}
 if len(keys)!=len(plan.steps):raise ValueError("duplicate step key")
 g=nx.DiGraph()
 for s in plan.steps:
  g.add_node(s.key)
  for d in s.depends_on:
   if d not in keys:raise ValueError(f"missing dependency: {d}")
   g.add_edge(d,s.key)
 if not nx.is_directed_acyclic_graph(g):raise ValueError("plan contains a cycle")
 return g
