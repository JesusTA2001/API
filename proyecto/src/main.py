from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt  # Requiere: pip install python-jose[cryptography]
from pydantic import BaseModel

# Importamos los Modelos y DAOs
from src.models.UsuariosModel import (
    Salida, UsuarioSalida, UsuarioAutenticar, RolEnum
)
from src.dao.UsuariosDAO import UsuariosDAO
from src.dao.CatalogosDAO import CatalogosDAO
from src.dao.GestionAcademicaDAO import GestionAcademicaDAO

# ==========================================
# CONFIGURACIÓN DE SEGURIDAD
# ==========================================
SECRET_KEY = "tu_clave_secreta_super_segura_cambiala_en_produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Esquema de seguridad OAuth2 (El frontend enviará usuario/pass a "/token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="API Proyecto Inglés", version="2.0.0")

# Configuración CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",  # React/Angular/Vue standard ports
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancias de los DAOs
dao_usuarios = UsuariosDAO()
dao_catalogos = CatalogosDAO()
dao_academica = GestionAcademicaDAO()

# ==========================================
# MODELOS PYDANTIC PARA REQUEST BODY
# ==========================================

class EstudianteCrear(BaseModel):
    nControl: int
    apellidoPaterno: str
    apellidoMaterno: str
    nombre: str
    email: str
    genero: Optional[str] = None
    CURP: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ubicacion: Optional[str] = "S/N"
    usuario: str
    password: str

class EstudianteActualizar(BaseModel):
    apellidoPaterno: Optional[str] = None
    apellidoMaterno: Optional[str] = None
    nombre: Optional[str] = None
    email: Optional[str] = None
    genero: Optional[str] = None
    CURP: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ubicacion: Optional[str] = None

class ProfesorCrear(BaseModel):
    apellidoPaterno: str
    apellidoMaterno: str
    nombre: str
    email: str
    genero: Optional[str] = None
    CURP: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ubicacion: Optional[str] = None
    nivelEstudio: Optional[str] = None
    RFC: Optional[str] = None
    usuario: str
    password: str

class ProfesorActualizar(BaseModel):
    apellidoPaterno: Optional[str] = None
    apellidoMaterno: Optional[str] = None
    nombre: Optional[str] = None
    email: Optional[str] = None
    genero: Optional[str] = None
    CURP: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ubicacion: Optional[str] = None
    nivelEstudio: Optional[str] = None
    RFC: Optional[str] = None

class AdministradorCrear(BaseModel):
    apellidoPaterno: str
    apellidoMaterno: str
    nombre: str
    email: str
    genero: Optional[str] = None
    CURP: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    RFC: Optional[str] = None
    usuario: str
    password: str

class AdministradorActualizar(BaseModel):
    apellidoPaterno: Optional[str] = None
    apellidoMaterno: Optional[str] = None
    nombre: Optional[str] = None
    email: Optional[str] = None
    genero: Optional[str] = None
    CURP: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    RFC: Optional[str] = None

# Modelos para Gestión Académica
class GrupoCrear(BaseModel):
    grupo: str
    id_Periodo: int
    id_Profesor: int
    id_Nivel: int
    ubicacion: Optional[str] = None
    id_cHorario: int

class GrupoActualizar(BaseModel):
    grupo: Optional[str] = None
    id_Periodo: Optional[int] = None
    id_Profesor: Optional[int] = None
    id_Nivel: Optional[int] = None
    ubicacion: Optional[str] = None
    id_cHorario: Optional[int] = None

class InscribirEstudiante(BaseModel):
    nControl: int
    id_Grupo: int

class CalificacionCrear(BaseModel):
    nControl: int
    id_Grupo: int
    id_Periodo: int
    id_nivel: int
    parcial1: Optional[float] = 0
    parcial2: Optional[float] = 0
    parcial3: Optional[float] = 0
    final: Optional[float] = 0

class CalificacionActualizar(BaseModel):
    id_Calificaciones: int
    parcial1: Optional[float] = None
    parcial2: Optional[float] = None
    parcial3: Optional[float] = None
    final: Optional[float] = None

class AsistenciaRegistrar(BaseModel):
    nControl: int
    id_Grupo: int
    fecha: str  # Formato: YYYY-MM-DD

# Modelos para Catálogos
class HorarioCrear(BaseModel):
    ubicacion: Optional[str] = None
    diaSemana: Optional[str] = None
    hora: Optional[str] = None

class HorarioActualizar(BaseModel):
    ubicacion: Optional[str] = None
    diaSemana: Optional[str] = None
    hora: Optional[str] = None

# ==========================================
# UTILIDADES DE SEGURIDAD (JWT)
# ==========================================

def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    """
    Valida el token y devuelve los datos del usuario (rol e id).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: str = payload.get("sub")
        rol: str = payload.get("rol")
        id_relacion: int = payload.get("id_relacion")
        
        if usuario is None:
            raise credentials_exception
        return {"usuario": usuario, "rol": rol, "id_relacion": id_relacion}
    except JWTError:
        raise credentials_exception

# ==========================================
# 1. AUTHENTICATION (LOGIN)
# ==========================================

@app.post("/token", tags=["Autenticación"])
async def login_para_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # form_data.username y form_data.password vienen del formulario estándar de OAuth2
    respuesta = dao_usuarios.autenticar_usuario(form_data.username, form_data.password)
    
    if not respuesta["estatus"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    usuario_db = respuesta["usuario"]
    
    # Creamos el token incluyendo el ROL y el ID específico (nControl, idProfesor, etc.)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crear_token_acceso(
        data={
            "sub": usuario_db.usuario, 
            "rol": usuario_db.rol,
            "id_relacion": usuario_db.id_relacion
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "rol": usuario_db.rol,
        "id_vinculado": usuario_db.id_relacion
    }

# ==========================================
# 2. GESTIÓN DE USUARIOS (ESTUDIANTES, PROFESORES, ADMIN)
# ==========================================

# --- ESTUDIANTES ---
@app.post("/estudiantes/", tags=["Estudiantes"])
def crear_estudiante(datos: EstudianteCrear, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] not in [RolEnum.ADMINISTRADOR, RolEnum.COORDINADOR]:
        raise HTTPException(status_code=403, detail="No tienes permisos")
    return dao_usuarios.crear_estudiante(datos.model_dump())

@app.get("/estudiantes/{nControl}", tags=["Estudiantes"])
def leer_estudiante(nControl: int, current_user: dict = Depends(obtener_usuario_actual)):
    return dao_usuarios.obtener_estudiante(nControl)

@app.put("/estudiantes/{nControl}", tags=["Estudiantes"])
def actualizar_estudiante(nControl: int, datos: EstudianteActualizar, current_user: dict = Depends(obtener_usuario_actual)):
    # Permisos: Admin, Coordinador, o el propio estudiante (opcional)
    if current_user['rol'] not in [RolEnum.ADMINISTRADOR, RolEnum.COORDINADOR]:
         if current_user['rol'] == RolEnum.ESTUDIANTE and current_user['id_relacion'] == nControl:
             pass # Es el mismo estudiante, permitido
         else:
            raise HTTPException(status_code=403, detail="No tienes permisos")
    return dao_usuarios.modificar_estudiante(nControl, datos.model_dump(exclude_unset=True))

@app.delete("/estudiantes/{nControl}", tags=["Estudiantes"])
def eliminar_estudiante(nControl: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=403, detail="Solo Administradores pueden eliminar")
    return dao_usuarios.eliminar_estudiante(nControl)

# --- PROFESORES ---
@app.post("/profesores/", tags=["Profesores"])
def crear_profesor(datos: ProfesorCrear, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=403, detail="No tienes permisos")
    return dao_usuarios.crear_profesor(datos.model_dump())

@app.get("/profesores/{id_profesor}", tags=["Profesores"])
def leer_profesor(id_profesor: int, current_user: dict = Depends(obtener_usuario_actual)):
    return dao_usuarios.obtener_profesor(id_profesor)

@app.put("/profesores/{id_profesor}", tags=["Profesores"])
def actualizar_profesor(id_profesor: int, datos: ProfesorActualizar, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=403, detail="No tienes permisos")
    return dao_usuarios.modificar_profesor(id_profesor, datos.model_dump(exclude_unset=True))

@app.delete("/profesores/{id_profesor}", tags=["Profesores"])
def eliminar_profesor(id_profesor: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=403, detail="Solo Administradores pueden eliminar")
    return dao_usuarios.eliminar_profesor(id_profesor)

# --- ADMINISTRADORES ---
@app.post("/administradores/", tags=["Administradores"])
def crear_administrador(datos: AdministradorCrear, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=403, detail="Solo un Admin puede crear otro Admin")
    return dao_usuarios.crear_administrador(datos.model_dump())

@app.get("/administradores/{id_admin}", tags=["Administradores"])
def leer_administrador(id_admin: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=403, detail="No autorizado")
    return dao_usuarios.obtener_administrador(id_admin)

@app.put("/administradores/{id_admin}", tags=["Administradores"])
def actualizar_administrador(id_admin: int, datos: AdministradorActualizar, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=403, detail="No autorizado")
    return dao_usuarios.modificar_administrador(id_admin, datos.model_dump(exclude_unset=True))

@app.delete("/administradores/{id_admin}", tags=["Administradores"])
def eliminar_administrador(id_admin: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=403, detail="No autorizado")
    return dao_usuarios.eliminar_administrador(id_admin)

# ==========================================
# 3. GESTIÓN ACADÉMICA (GRUPOS)
# ==========================================

@app.post("/grupos/", tags=["Grupos"])
def crear_grupo(datos: GrupoCrear, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] not in [RolEnum.ADMINISTRADOR, RolEnum.COORDINADOR]:
        raise HTTPException(status_code=403, detail="No autorizado")
    return dao_academica.crear_grupo(datos.model_dump())

@app.get("/grupos/", tags=["Grupos"])
def listar_grupos(current_user: dict = Depends(obtener_usuario_actual)):
    # Todos los usuarios autenticados pueden ver los grupos
    return dao_academica.obtener_grupos_detalle()

@app.put("/grupos/{id_grupo}", tags=["Grupos"])
def modificar_grupo(id_grupo: int, datos: GrupoActualizar, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] not in [RolEnum.ADMINISTRADOR, RolEnum.COORDINADOR]:
        raise HTTPException(status_code=403, detail="No autorizado")
    return dao_academica.modificar_grupo(id_grupo, datos.model_dump(exclude_unset=True))

@app.delete("/grupos/{id_grupo}", tags=["Grupos"])
def eliminar_grupo(id_grupo: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR:
        raise HTTPException(status_code=403, detail="No autorizado")
    return dao_academica.eliminar_grupo(id_grupo)

# ==========================================
# 4. CATÁLOGOS (NIVELES, PERIODOS, HORARIOS)
# ==========================================

@app.get("/niveles/", tags=["Catálogos"])
def obtener_niveles():
    return dao_catalogos.obtener_niveles()

@app.post("/niveles/", tags=["Catálogos"])
def crear_nivel(nombre: str, id_manual: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR: raise HTTPException(status_code=403)
    return dao_catalogos.crear_nivel(nombre, id_manual)

@app.put("/niveles/{id_nivel}", tags=["Catálogos"])
def actualizar_nivel(id_nivel: int, nombre: str, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR: raise HTTPException(status_code=403)
    return dao_catalogos.actualizar_nivel(id_nivel, nombre)

@app.delete("/niveles/{id_nivel}", tags=["Catálogos"])
def eliminar_nivel(id_nivel: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR: raise HTTPException(status_code=403)
    return dao_catalogos.eliminar_nivel(id_nivel)

@app.get("/periodos/", tags=["Catálogos"])
def obtener_periodos():
    return dao_catalogos.obtener_periodos()

@app.post("/periodos/", tags=["Catálogos"])
def crear_periodo(id_periodo: int, descripcion: str, anio: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR: raise HTTPException(status_code=403)
    return dao_catalogos.crear_periodo(id_periodo, descripcion, anio)

@app.put("/periodos/{id_periodo}", tags=["Catálogos"])
def actualizar_periodo(id_periodo: int, descripcion: str, anio: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR: raise HTTPException(status_code=403)
    return dao_catalogos.actualizar_periodo(id_periodo, descripcion, anio)

@app.delete("/periodos/{id_periodo}", tags=["Catálogos"])
def eliminar_periodo(id_periodo: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] != RolEnum.ADMINISTRADOR: raise HTTPException(status_code=403)
    return dao_catalogos.eliminar_periodo(id_periodo)

@app.get("/horarios/", tags=["Catálogos"])
def obtener_horarios():
    return dao_catalogos.obtener_horarios_activos()

@app.post("/horarios/", tags=["Catálogos"])
def crear_horario(datos: HorarioCrear, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] not in [RolEnum.ADMINISTRADOR, RolEnum.COORDINADOR]: raise HTTPException(status_code=403)
    return dao_catalogos.crear_horario(datos.model_dump())

@app.put("/horarios/{id_horario}", tags=["Catálogos"])
def actualizar_horario(id_horario: int, datos: HorarioActualizar, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] not in [RolEnum.ADMINISTRADOR, RolEnum.COORDINADOR]: raise HTTPException(status_code=403)
    return dao_catalogos.actualizar_horario(id_horario, datos.model_dump(exclude_unset=True))

@app.delete("/horarios/{id_horario}", tags=["Catálogos"])
def eliminar_horario(id_horario: int, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] not in [RolEnum.ADMINISTRADOR, RolEnum.COORDINADOR]: raise HTTPException(status_code=403)
    return dao_catalogos.eliminar_horario(id_horario)

# ==========================================
# 5. GESTIÓN ACADÉMICA (INSCRIPCIONES, CALIFICACIONES, ASISTENCIA)
# ==========================================

@app.post("/inscripciones/", tags=["Académico"])
def inscribir_alumno(datos: InscribirEstudiante, current_user: dict = Depends(obtener_usuario_actual)):
    # Solo Admin o Coordinador inscribe
    if current_user['rol'] not in [RolEnum.ADMINISTRADOR, RolEnum.COORDINADOR]:
        raise HTTPException(status_code=403, detail="No autorizado para inscribir")
    return dao_academica.inscribir_estudiante(datos.nControl, datos.id_Grupo)

@app.get("/inscripciones/grupo/{id_grupo}", tags=["Académico"])
def ver_alumnos_grupo(id_grupo: int, current_user: dict = Depends(obtener_usuario_actual)):
    return dao_academica.obtener_estudiantes_por_grupo(id_grupo)

@app.post("/calificaciones/", tags=["Académico"])
def registrar_calificacion(datos: CalificacionCrear, current_user: dict = Depends(obtener_usuario_actual)):
    # Profesores pueden calificar
    if current_user['rol'] not in [RolEnum.ADMINISTRADOR, RolEnum.PROFESOR]:
        raise HTTPException(status_code=403, detail="No autorizado")
    return dao_academica.asignar_calificacion(datos.model_dump())

@app.get("/calificaciones/{nControl}", tags=["Académico"])
def obtener_calificaciones(nControl: int, current_user: dict = Depends(obtener_usuario_actual)):
    # El estudiante puede ver sus calificaciones, o el profesor/admin
    if current_user['rol'] == RolEnum.ESTUDIANTE and current_user['id_relacion'] != nControl:
        raise HTTPException(status_code=403, detail="No autorizado para ver estas calificaciones")
    return dao_academica.obtener_calificaciones_estudiante(nControl)

@app.put("/calificaciones/", tags=["Académico"])
def actualizar_calificacion(datos: CalificacionActualizar, current_user: dict = Depends(obtener_usuario_actual)):
    # Solo Profesores o Admin pueden actualizar calificaciones
    if current_user['rol'] not in [RolEnum.ADMINISTRADOR, RolEnum.PROFESOR]:
        raise HTTPException(status_code=403, detail="No autorizado")
    return dao_academica.modificar_calificacion(datos.model_dump())

@app.post("/asistencias/", tags=["Académico"])
def tomar_asistencia(datos: AsistenciaRegistrar, current_user: dict = Depends(obtener_usuario_actual)):
    if current_user['rol'] not in [RolEnum.ADMINISTRADOR, RolEnum.PROFESOR]:
        raise HTTPException(status_code=403, detail="No autorizado")
    return dao_academica.registrar_asistencia(datos.nControl, datos.id_Grupo, datos.fecha)