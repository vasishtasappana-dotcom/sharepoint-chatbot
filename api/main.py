from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Chat API (Demo)")

class Query(BaseModel):
    message: str

# simple demo "corpus"
DOCS = [
    {"title":"MOC overview","text":"Management of Change covers approvals, risks, testing."},
    {"title":"Fit-to-standard scripts","text":"Standard test scripts for S/4 HANA modules."},
    {"title":"CPI iFlow guide","text":"Explains palette steps, error handling."}
]

@app.post("/chat")
def chat(q: Query):
    # naive retrieval: pick docs containing at least one query word
    tokens = set(w.lower() for w in q.message.split())
    hits = [d for d in DOCS if any(w in d["text"].lower() for w in tokens)]
    if not hits:
        hits = DOCS[:1]
    answer = "This is a demo answer synthesized from the sample docs."
    return {"answer": answer, "sources": [{"title": d["title"]} for d in hits]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
