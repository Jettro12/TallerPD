"""
FastAPI backend que suma dos números aleatorios y almacena el resultado en PostgreSQL.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import random
import os
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import asyncpg

app = FastAPI(title="Sumador Aleatorio API")

# Configurar CORS para permitir peticiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/sumador_db"
)

# Pool de conexiones de base de datos
db_pool: Optional[asyncpg.Pool] = None


class SumaResultado(BaseModel):
    """Modelo para el resultado de una suma."""
    id: int
    numero1: int
    numero2: int
    resultado: int
    fecha: datetime


@app.on_event("startup")
async def startup():
    """Inicializar conexión a la base de datos y crear tabla si no existe."""
    global db_pool
    
    try:
        db_pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=1,
            max_size=10
        )
        
        # Crear tabla si no existe
        async with db_pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS sumas (
                    id SERIAL PRIMARY KEY,
                    numero1 INTEGER NOT NULL,
                    numero2 INTEGER NOT NULL,
                    resultado INTEGER NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        print("✓ Conexión a la base de datos establecida")
        
    except Exception as e:
        print(f"✗ Error al conectar con la base de datos: {e}")
        raise


@app.on_event("shutdown")
async def shutdown():
    """Cerrar conexión a la base de datos."""
    global db_pool
    if db_pool:
        await db_pool.close()
        print("✓ Conexión a la base de datos cerrada")


@app.get("/")
async def root():
    """
    Endpoint raíz que sirve el frontend.
    """
    return FileResponse("src/static/index.html")


@app.post("/api/sumar", response_model=SumaResultado)
async def generar_suma():
    """
    Genera dos números aleatorios, los suma y almacena el resultado en la base de datos.
    
    Returns:
        SumaResultado: Objeto con los números generados, el resultado y la fecha
    """
    if not db_pool:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    
    try:
        # Generar números aleatorios entre 1 y 100
        numero1 = random.randint(1, 100)
        numero2 = random.randint(1, 100)
        resultado = numero1 + numero2
        
        # Insertar en la base de datos
        async with db_pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO sumas (numero1, numero2, resultado)
                VALUES ($1, $2, $3)
                RETURNING id, numero1, numero2, resultado, fecha
            """, numero1, numero2, resultado)
        
        return SumaResultado(
            id=row['id'],
            numero1=row['numero1'],
            numero2=row['numero2'],
            resultado=row['resultado'],
            fecha=row['fecha']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la suma: {str(e)}")


@app.get("/api/historial", response_model=List[SumaResultado])
async def obtener_historial(limit: int = 10):
    """
    Obtiene el historial de las últimas sumas realizadas.
    
    Args:
        limit: Número máximo de resultados a retornar (default: 10)
    
    Returns:
        List[SumaResultado]: Lista de las últimas sumas realizadas
    """
    if not db_pool:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    
    try:
        async with db_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT id, numero1, numero2, resultado, fecha
                FROM sumas
                ORDER BY fecha DESC
                LIMIT $1
            """, limit)
        
        return [
            SumaResultado(
                id=row['id'],
                numero1=row['numero1'],
                numero2=row['numero2'],
                resultado=row['resultado'],
                fecha=row['fecha']
            )
            for row in rows
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener historial: {str(e)}")


@app.get("/api/health")
async def health_check():
    """
    Verifica el estado de la aplicación y la conexión a la base de datos.
    
    Returns:
        dict: Estado de la aplicación y la base de datos
    """
    db_status = "connected" if db_pool else "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status
    }


# Montar archivos estáticos (frontend)
if os.path.exists("src/static"):
    app.mount("/static", StaticFiles(directory="src/static"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
