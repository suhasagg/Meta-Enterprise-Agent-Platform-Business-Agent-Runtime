class LayeredMemory:
 def __init__(self):self.working={};self.session={};self.episodic={};self.semantic={};self.entity={};self.procedural={}
 def layers(self):return ["working","session","episodic","semantic","entity","procedural"]
 def put(self,layer,key,value):getattr(self,layer)[key]=value
 def get(self,layer,key,default=None):return getattr(self,layer).get(key,default)
