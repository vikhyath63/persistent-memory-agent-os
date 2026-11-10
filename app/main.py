from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel,Field
from app.memory import remember,recall
app=FastAPI(title="Persistent Memory Agent OS",version="0.1.0")
DB=Path("memory.db")
class MemoryInput(BaseModel): session_id:str=Field(min_length=1); content:str=Field(min_length=1); tags:list[str]=[]
class RecallInput(BaseModel): query:str=Field(min_length=1); session_id:str|None=None; limit:int=Field(default=5,ge=1,le=50)
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/memories")
def create_memory(req:MemoryInput): return {"id":remember(DB,req.session_id,req.content,req.tags)}
@app.post("/recall")
def get_memories(req:RecallInput): return {"memories":recall(DB,req.query,req.limit,req.session_id)}
