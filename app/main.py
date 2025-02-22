from fastapi import FastAPI
import logging
from prometheus_fastapi_instrumentator import Instrumentator

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Instrumentar Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def always_ok():
    logger.info("Service C respondió exitosamente (fallback)")
    return {"message": "Hola desde C, soy el backup de B"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "C"}
