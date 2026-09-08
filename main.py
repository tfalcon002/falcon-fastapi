from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import psycopg2

app = FastAPI(title="Falcon API")

class WebhookData(BaseModel):
    user_id: str
    message: str
    agent_response: str

@app.get("/")
def read_root():
    return {"estado": "ok", "servicio": "API Falcon", "conectado": True}

@app.post("/webhook/n8n")
def receive_n8n_data(data: WebhookData):
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise HTTPException(status_code=500, detail="DATABASE_URL no configurada")
    
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS interacciones_agente (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255),
                mensaje TEXT,
                respuesta TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute("""
            INSERT INTO interacciones_agente (user_id, mensaje, respuesta)
            VALUES (%s, %s, %s)
        """, (data.user_id, data.message, data.agent_response))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {"status": "success", "message": "Interacción registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))