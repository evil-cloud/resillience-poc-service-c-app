from fastapi import FastAPI
import logging
import json
from datetime import datetime, timezone
from prometheus_fastapi_instrumentator import Instrumentator

# Configurar logging con formato JSON estructurado

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("service-c")

def log_json(level, component, message, status_code=None):
    log_entry = {
        "level": level,
        "time": datetime.now(timezone.utc).isoformat(),
        "component": component,
        "message": message
    }
    if status_code is not None:
        log_entry["status_code"] = status_code
    print(json.dumps(log_entry))

app = FastAPI()

# Instrumentar Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def always_ok():
    log_json("info", "service-c", "Service C responded successfully (fallback).", 200)
    return {"message": "Hello from C, I'm the backup for B"}

@app.get("/health")
async def health_check():
    log_json("info", "service-c", "Health check endpoint called.", 200)
    return {"status": "ok", "service": "C"}
