from pydantic import BaseModel,Field
from typing import Any,Literal
class GoalRequest(BaseModel):
 tenant_id:str="acme";principal_id:str="owner@example";goal:str;context:dict[str,Any]=Field(default_factory=dict)
class StepSpec(BaseModel):
 key:str;agent:Literal["sales","support","commerce","marketing","supervisor"]
 capability:str;kind:Literal["skill","mcp","a2a","approval","evaluate"]="skill"
 depends_on:list[str]=Field(default_factory=list);input:dict[str,Any]=Field(default_factory=dict)
 risk:Literal["READ","WRITE","HIGH"]="READ"
class Plan(BaseModel):
 objective:str;steps:list[StepSpec]
class ConnectorCall(BaseModel):
 connector:str;operation:str;arguments:dict[str,Any]=Field(default_factory=dict);dry_run:bool=True
