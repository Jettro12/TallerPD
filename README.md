# 🎲 Sumador Aleatorio - Full Stack Application

Aplicación web full-stack que genera sumas aleatorias y las almacena en una base de datos PostgreSQL.

## 🚀 Características

- **Frontend**: Interfaz web interactiva con botón para generar sumas aleatorias
- **Backend**: API REST con FastAPI
- **Base de datos**: PostgreSQL para almacenar historial de sumas
- **Docker**: Configuración completa con Docker Compose

## 📋 Requisitos

- Python 3.12
- Docker y Docker Compose
- PostgreSQL (si ejecutas localmente sin Docker)

## 🏗️ Estructura del Proyecto

```
Backend_HelloWorld/
├── src/
│   ├── __init__.py
│   ├── main.py              # API FastAPI
│   └── static/
│       └── index.html       # Frontend
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── Dockerfile
├── docker-compose.yml       # Orquestación de contenedores
├── requirements.txt
└── README.md
```

## 🔌 Endpoints de la API

- **GET /** → Sirve el frontend
- **POST /api/sumar** → Genera suma aleatoria y la guarda en BD
- **GET /api/historial?limit=10** → Obtiene historial de sumas
- **GET /api/health** → Estado de la aplicación

## 🐳 Opción 1: Ejecución con Docker Compose (Recomendado)

Esta es la forma más sencilla de ejecutar el proyecto completo:

```powershell
# Construir y levantar los contenedores
docker-compose up --build

# O en modo detached (segundo plano)
docker-compose up -d --build
```

La aplicación estará disponible en: **http://localhost**

Para detener los contenedores:
```powershell
docker-compose down

# Para eliminar también los volúmenes (datos de BD)
docker-compose down -v
```

## 💻 Opción 2: Ejecución Local (Desarrollo)

### 1. Configurar PostgreSQL local

Instala PostgreSQL y crea la base de datos:

```sql
CREATE DATABASE sumador_db;
```

### 2. Crear y activar entorno virtual

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Si hay error de ejecución de políticas:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Configurar variable de entorno (opcional)

Si tu PostgreSQL tiene credenciales diferentes, configura la URL:

```powershell
$env:DATABASE_URL = "postgresql://usuario:password@localhost:5432/sumador_db"
```

### 5. Ejecutar la aplicación

```powershell
python -m uvicorn src.main:app --host 0.0.0.0 --port 80 --reload
```

La aplicación estará disponible en: **http://localhost**

### 6. Ejecutar tests

```powershell
pytest tests/
```

## 📊 Base de Datos

### Esquema de la tabla `sumas`

```sql
CREATE TABLE sumas (
    id SERIAL PRIMARY KEY,
    numero1 INTEGER NOT NULL,
    numero2 INTEGER NOT NULL,
    resultado INTEGER NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Consultas útiles

```sql
-- Ver todas las sumas
SELECT * FROM sumas ORDER BY fecha DESC;

-- Contar total de sumas
SELECT COUNT(*) FROM sumas;

-- Ver estadísticas
SELECT 
    COUNT(*) as total_sumas,
    AVG(resultado) as promedio_resultado,
    MAX(resultado) as resultado_maximo,
    MIN(resultado) as resultado_minimo
FROM sumas;
```

## 🐋 Docker Commands Quick Reference

```powershell
# Ver contenedores en ejecución
docker-compose ps

# Ver logs
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Detener sin eliminar contenedores
docker-compose stop

# Eliminar todo (contenedores y volúmenes)
docker-compose down -v

# Reconstruir solo el backend
docker-compose up -d --build backend
```

## 🧪 Testing

```powershell
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=src tests/

# Modo verbose
pytest -v
```

## 🌐 Uso de la Aplicación

1. Abre tu navegador en **http://localhost**
2. Haz clic en el botón "✨ Generar Suma Aleatoria"
3. La aplicación generará dos números aleatorios entre 1 y 100
4. Verás la operación y el resultado
5. El historial muestra las últimas 10 sumas realizadas
6. El historial se actualiza automáticamente cada 30 segundos

## 🔧 Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión a PostgreSQL | `postgresql://postgres:postgres@localhost:5432/sumador_db` |

## 📝 Notas Importantes

- El backend corre en el puerto 80
- PostgreSQL usa el puerto 5432
- Los datos se persisten en un volumen Docker
- La aplicación crea automáticamente la tabla `sumas` al iniciar
- CORS está configurado para permitir todas las origins (ajustar en producción)

## 🚀 Deploy en Producción

Para producción, considera:

1. Cambiar credenciales de PostgreSQL
2. Configurar CORS específicamente para tu dominio
3. Usar variables de entorno para secretos
4. Implementar HTTPS
5. Configurar límites de rate limiting
6. Agregar logs más robustos
7. Implementar monitoreo y alertas

## 📦 Publicar en Docker Hub

```powershell
# Login
docker login

# Tag la imagen
docker tag backend_helloworld:latest TU_USUARIO/sumador-aleatorio:latest

# Push
docker push TU_USUARIO/sumador-aleatorio:latest
```

## 🤝 Contribuciones

Este proyecto es parte de un curso académico de Programación Distribuida en la UCE.

## 📄 Licencia

Proyecto académico - UCE 2025-2026
