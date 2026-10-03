from app.memory import LayeredMemory
def test_layers():
 m=LayeredMemory();m.put("working","x",1);assert m.get("working","x")==1 and len(m.layers())==6
