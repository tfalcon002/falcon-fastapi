from fastapi import FastAPI

app = FastAPI(title="Falcon API")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Falcon API", "connected": True}