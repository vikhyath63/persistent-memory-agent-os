import sqlite3,re
from pathlib import Path
def connect(db:Path):
    con=sqlite3.connect(db); con.row_factory=sqlite3.Row
    con.execute("CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY, session_id TEXT NOT NULL, content TEXT NOT NULL, tags TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
    con.commit(); return con
def tokens(s): return {w.lower() for w in re.findall(r"\w+",s) if len(w)>2}
def remember(db:Path,session_id:str,content:str,tags:list[str]):
    with connect(db) as con:
        cur=con.execute("INSERT INTO memories(session_id,content,tags) VALUES(?,?,?)",(session_id,content,",".join(tags)))
        return cur.lastrowid
def recall(db:Path,query:str,limit:int=5,session_id:str|None=None):
    q=tokens(query)
    with connect(db) as con:
        rows=con.execute("SELECT * FROM memories WHERE session_id=? ORDER BY id DESC",(session_id,)).fetchall() if session_id else con.execute("SELECT * FROM memories ORDER BY id DESC").fetchall()
    ranked=[]
    for row in rows:
        score=len(q & tokens(row["content"]))/max(1,len(q))
        if score: ranked.append({**dict(row),"score":round(score,3)})
    return sorted(ranked,key=lambda x:(x["score"],x["id"]),reverse=True)[:limit]
