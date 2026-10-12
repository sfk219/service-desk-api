"""Ticket management REST API using FastAPI and SQLite."""
import sqlite3,os
from datetime import datetime,timezone
from pathlib import Path
from typing import Literal
from fastapi import FastAPI,HTTPException,Query,Response
from pydantic import BaseModel,Field
DB=os.getenv("TICKETS_DB","data/tickets.db")
app=FastAPI(title="Service Desk API",version="1.0")
def connect():
    Path(DB).parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
    c.execute("CREATE TABLE IF NOT EXISTS tickets(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,category TEXT NOT NULL,priority TEXT NOT NULL,status TEXT NOT NULL,created_at TEXT NOT NULL)")
    return c
class CreateTicket(BaseModel):
    title:str=Field(min_length=3,max_length=150)
    category:str=Field(min_length=2,max_length=60)
    priority:Literal["low","medium","high"]="medium"
class UpdateTicket(BaseModel):
    status:Literal["open","in_progress","resolved"]
@app.get("/health")
def health():return {"status":"ok"}
@app.post("/tickets",status_code=201)
def create(ticket:CreateTicket):
    with connect() as db:
        cur=db.execute("INSERT INTO tickets(title,category,priority,status,created_at) VALUES(?,?,?,?,?)",(ticket.title,ticket.category,ticket.priority,"open",datetime.now(timezone.utc).isoformat()))
        return dict(db.execute("SELECT * FROM tickets WHERE id=?",(cur.lastrowid,)).fetchone())
@app.get("/tickets")
def listing(status:str|None=None,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0)):
    with connect() as db:
        rows=db.execute("SELECT * FROM tickets WHERE (? IS NULL OR status=?) ORDER BY id LIMIT ? OFFSET ?",(status,status,limit,offset)).fetchall()
        return [dict(r) for r in rows]
@app.get("/tickets/{id}")
def get(id:int):
    with connect() as db:row=db.execute("SELECT * FROM tickets WHERE id=?",(id,)).fetchone()
    if row is None:raise HTTPException(404,"Ticket not found")
    return dict(row)
@app.patch("/tickets/{id}")
def update(id:int,body:UpdateTicket):
    with connect() as db:
        db.execute("UPDATE tickets SET status=? WHERE id=?",(body.status,id))
        row=db.execute("SELECT * FROM tickets WHERE id=?",(id,)).fetchone()
    if row is None:raise HTTPException(404,"Ticket not found")
    return dict(row)
@app.delete("/tickets/{id}",status_code=204)
def delete(id:int):
    with connect() as db:result=db.execute("DELETE FROM tickets WHERE id=?",(id,))
    if not result.rowcount:raise HTTPException(404,"Ticket not found")
    return Response(status_code=204)
