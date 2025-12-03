# API Proyecto Inglés - FastAPI

API REST para gestión académica de cursos de inglés.

## 🚀 Despliegue en Azure App Service

### Archivos necesarios (✅ Ya incluidos):
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `startup.txt` - Comando de inicio para Azure
- ✅ `src/config.py` - Configuración con variables de entorno
- ✅ `.gitignore` - Archivos a ignorar en git
- ✅ `.env.example` - Ejemplo de variables de entorno

### Pasos para desplegar:

#### 1. Crear App Service en Azure
```bash
az webapp up --runtime PYTHON:3.12 --sku B1 --name tu-nombre-app
```

#### 2. Configurar Variables de Entorno en Azure
En Azure Portal → Tu App Service → Configuration → Application settings:

| Name | Value |
|------|-------|
| `DATABASE_URL` | `mysql+pymysql://admin_ingles:Gui11ermo1@mysqlingles.mysql.database.azure.com/proyectoIngles` |
| `SECRET_KEY` | `tu_clave_secreta_super_segura_cambiala_en_produccion` |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` |
| `PYTHON_VERSION` | `3.12` |

#### 3. Configurar Startup Command
En Azure Portal → Tu App Service → Configuration → General settings:
```
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app --bind 0.0.0.0:8000
```

#### 4. Desplegar desde GitHub
- Ve a Deployment Center en Azure Portal
- Conecta tu repositorio de GitHub
- Azure automáticamente construirá y desplegará la aplicación

### 📝 Endpoints principales:
- `POST /token` - Autenticación (retorna JWT)
- `GET /docs` - Documentación Swagger UI
- `GET /estudiantes/` - Listar estudiantes
- `GET /profesores/` - Listar profesores
- `GET /grupos/` - Listar grupos
- `POST /inscripciones/` - Inscribir estudiante a grupo

### 🔒 Autenticación:
1. Obtén token en `/token` con usuario y contraseña
2. Usa el token en el header: `Authorization: Bearer {token}`
3. Usuarios de prueba: `1000`, `1001`, `1002` (contraseña: `123456`)

### 💾 Base de Datos:
- Azure MySQL Flexible Server
- Host: `mysqlingles.mysql.database.azure.com`
- Base de datos: `proyectoIngles`
- Conexión SSL requerida

### 🛠️ Desarrollo Local:
```bash
# Activar entorno virtual
.\env\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python -m uvicorn src.main:app --reload
```

La API estará disponible en: http://127.0.0.1:8000

### 📦 Tecnologías:
- FastAPI 0.116.1
- SQLModel 0.0.27
- PyMySQL 1.1.1
- Python-Jose (JWT)
- Uvicorn/Gunicorn
