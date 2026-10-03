from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
 database_url:str="postgresql+asyncpg://postgres:postgres@localhost:5432/agents"
 redis_url:str="redis://localhost:6379/0";api_key:str="change-me";environment:str="local"
 max_parallel_steps:int=8;mcp_gateway_url:str="http://localhost:8100";a2a_gateway_url:str="http://localhost:8200"
 connector_mode:str="mock"
 model_config=SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()
