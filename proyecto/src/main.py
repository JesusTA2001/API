from fastapi import FastAPI,Request,HTTPException,status
import uvicorn

from dao.database import Conexion
from dao.UsuariosDAO import UsuariosDAO
from models.UsuariosModel import UsuarioAutenticar,UsuarioSalida, HorarioCrear
from fastapi import Depends
from models.EventosModel import vAlumnos, AlumnoSalida, vProfesores, ProfesorSalida, vGrupos, GrupoSalida, GruposSalida, vHorarios, HorarioSalida, HorariosSalida
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from models.UsuariosModel import vUsuarios, alumnos, profesores, administrador, AlumnoCrear, ProfesorCrear, AdministradorCrear, nivelesCrear, modalidadCrear, GrupoCrear, carreraCrear, HorarioCrear
from models.UsuariosModel import AlumnoSalida
from dao.autenticarDAO import AutenticacionDAO

# JESUS TORRES ALVAREZ
# MAESTRIA EN SISTEMAS COMPUTACIONALES
# ARQUITECTURA ORIENTADA A SERVICIOS
# MAESTRO:Roberto Suarez SINZUN

app=FastAPI()
security=HTTPBasic()

@app.on_event("startup")
def startup():
    conexion=Conexion()
    session=conexion.getSession()
    app.session=session
    print("Conectado con la BD")
def obtener_usuario_actual(
    credentials: HTTPBasicCredentials = Depends(security), 
    request: Request = None
):
    dao = AutenticacionDAO(request.app.session)
    return dao.autenticar(credentials.username, credentials.password)

@app.get("/")
async def inicio():
    return "Bienvenido a la API REST del Proyecto"
#Validación de usuario
def validarUsuario(request: Request, credenciales: HTTPBasicCredentials = Depends(security)):
    uDAO = UsuariosDAO(request.app.session)
    usuario = uDAO.autenticar(credenciales.username, credenciales.password)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    return usuario

# crear alumno 
@app.post("/alumnos", response_model=AlumnoSalida, tags=["Alumnos"], summary="Crear un nuevo alumno")
def crear_alumno(alumno: AlumnoCrear, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Control de acceso por rol
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear alumnos")

    dao = UsuariosDAO(request.app.session)
    nuevo = dao.crearAlumno(alumno)
    return nuevo
# Obtener alumno por ID
@app.get("/alumnos/{id}", response_model=AlumnoSalida, tags=["Alumnos"], summary="Obtener un alumno por ID")
def obtener_alumno(id: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Ejemplo: cualquier rol puede consultar, excepto que quieras restringir
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para ver alumnos")

    dao = UsuariosDAO(request.app.session)
    alumno = dao.obtenerAlumno(id)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno

# Modificar alumno
@app.put("/alumnos/{id}", response_model=AlumnoSalida, tags=["Alumnos"], summary="Modificar un alumno existente")
def modificar_alumno(id: int, alumno: AlumnoCrear, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Ejemplo: solo administrativos y docentes pueden modificar
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar alumnos")

    dao = UsuariosDAO(request.app.session)
    actualizado = dao.modificarAlumno(id, alumno)
    return actualizado
# Eliminar alumno

@app.delete("/alumnos/{id}", tags=["Alumnos"], summary="Eliminar un alumno existente")
def eliminar_alumno(id: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Ejemplo: solo administrativos pueden eliminar
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar alumnos")

    dao = UsuariosDAO(request.app.session)
    exito = dao.eliminarAlumno(id)
    if not exito:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return {"mensaje": "Alumno eliminado correctamente"}
#crear profesor

@app.post("/profesores", tags=["Profesores"], summary="Crear un nuevo profesor")
async def crear_profesor(profesor: ProfesorCrear, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden crear profesores
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear profesores")

    dao = UsuariosDAO(request.app.session)
    nuevo = dao.crearProfesor(profesor)          
    return nuevo
# Obtener profesor por ID

@app.get("/profesores/{id_Profesor}", tags=["Profesores"], summary="Obtener un profesor por ID")
def obtener_profesor(id_Profesor: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para consultar profesores")

    dao = UsuariosDAO(request.app.session)
    profesor = dao.obtenerProfesor(id_Profesor)
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor

# Modificar profesor

@app.put("/profesores/{id_Profesor}", tags=["Profesores"], summary="Modificar un profesor existente")
def modificar_profesor(id_Profesor: int, profesor: ProfesorCrear, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden modificar profesores
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar profesores")

    dao = UsuariosDAO(request.app.session)
    actualizado = dao.modificarProfesor(id_Profesor, profesor)
    return actualizado

# Eliminar profesor

@app.delete("/profesores/{id_Profesor}", tags=["Profesores"], summary="Eliminar un profesor existente")
def eliminar_profesor(id_Profesor: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden eliminar profesores
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar profesores")

    dao = UsuariosDAO(request.app.session)
    exito = dao.eliminarProfesor(id_Profesor)
    if not exito:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return {"mensaje": "Profesor eliminado correctamente"}

#crear administrador

@app.post("/administrador", tags=["Administrador"], summary="Crear un nuevo administrador")
async def crear_administrador(administrador: AdministradorCrear, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administradores pueden crear a otros administradores
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear administradores")

    dao = UsuariosDAO(request.app.session)
    nuevo = dao.crearAdministrador(administrador)       
    return nuevo
# Obtener administrador por ID

@app.get("/administrador/{id_Administrador}", tags=["Administrador"], summary="Obtener un administrador por ID")
def obtener_administrador(id_Administrador: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administradores pueden consultar administradores
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para consultar administradores")

    dao = UsuariosDAO(request.app.session)
    administrador = dao.obtenerAdministrador(id_Administrador)
    if not administrador:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    return administrador
# Modificar Administrador

@app.put("/administrador/{id_Administrador}", tags=["Administrador"], summary="Modificar un administrador existente")
def modificar_administrador(id_Administrador: int, administrador: AdministradorCrear, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administradores pueden modificar administradores
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar administradores")

    dao = UsuariosDAO(request.app.session)
    actualizado = dao.modificarAdministrador(id_Administrador, administrador)
    return actualizado
# Eliminar Administrador

@app.delete("/administrador/{id_Administrador}", tags=["Administrador"], summary="Eliminar un administrador existente")
def eliminar_administrador(id_Administrador: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar administradores")

    dao = UsuariosDAO(request.app.session)
    exito = dao.eliminarAdministrador(id_Administrador)
    if not exito:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    return {"mensaje": "Administrador eliminado correctamente"}
#crear nivel
# @app.post("/niveles",tags=["Niveles"],summary="Crear un nuevo nivel")
# async def crear_nivel(nivel: nivelesCrear,request: Request):
#     dao = UsuariosDAO(request.app.session)
#     nuevo = dao.crearNivel(nivel)    
#     return nuevo
@app.post("/niveles", tags=["Niveles"], summary="Crear un nuevo nivel")
async def crear_nivel(nivel: nivelesCrear, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden crear niveles
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear niveles")

    dao = UsuariosDAO(request.app.session)
    nuevo = dao.crearNivel(nivel)    
    return nuevo
#Obtener nivel por ID
# @app.get("/niveles/{id_Nivel}", tags=["Niveles"], summary="Obtener un nivel por ID")
# def obtener_nivel(id_Nivel: int,request: Request):
#     dao = UsuariosDAO(request.app.session)
#     nivel = dao.obtenerNivel(id_Nivel)
#     if not nivel:
#         raise HTTPException(status_code=404, detail="Nivel no encontrado")
#     return nivel
@app.get("/niveles/{id_Nivel}", tags=["Niveles"], summary="Obtener un nivel por ID")
def obtener_nivel(id_Nivel: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para consultar niveles")

    dao = UsuariosDAO(request.app.session)
    nivel = dao.obtenerNivel(id_Nivel)
    if not nivel:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return nivel
# Modificar nivel
# @app.put("/niveles/{id_Nivel}", tags=["Niveles"], summary="Modificar un nivel existente")
# def modificar_nivel(id_Nivel: int, nivel: nivelesCrear,request: Request):
#     dao = UsuariosDAO(request.app.session)
#     actualizado = dao.modificarNivel(id_Nivel, nivel)
#     return actualizado
@app.put("/niveles/{id_Nivel}", tags=["Niveles"], summary="Modificar un nivel existente")
def modificar_nivel(id_Nivel: int, nivel: nivelesCrear, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden modificar niveles
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar niveles")

    dao = UsuariosDAO(request.app.session)
    actualizado = dao.modificarNivel(id_Nivel, nivel)
    return actualizado
# Eliminar nivel
# @app.delete("/niveles/{id_Nivel}", tags=["Niveles"], summary="Eliminar un nivel existente")
# def eliminar_nivel(id_Nivel: int,request: Request):
#     dao = UsuariosDAO(request.app.session)
#     exito = dao.eliminarNivel(id_Nivel)
#     if not exito:
#         raise HTTPException(status_code=404, detail="Nivel no encontrado")
#     return {"mensaje": "Nivel eliminado correctamente"}
@app.delete("/niveles/{id_Nivel}", tags=["Niveles"], summary="Eliminar un nivel existente")
def eliminar_nivel(id_Nivel: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden eliminar niveles
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar niveles")

    dao = UsuariosDAO(request.app.session)
    exito = dao.eliminarNivel(id_Nivel)
    if not exito:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return {"mensaje": "Nivel eliminado correctamente"}
#crear modalidad
# @app.post("/modalidades",tags=["Modalidades"],summary="Crear una nueva modalidad")
# async def crear_modalidad(modalidad: modalidadCrear,request: Request):  
#     dao = UsuariosDAO(request.app.session)
#     nuevo = dao.crearModalidad(modalidad)        
#     return nuevo
@app.post("/modalidades", tags=["Modalidades"], summary="Crear una nueva modalidad")
async def crear_modalidad(modalidad: modalidadCrear, request: Request, usuario=Depends(obtener_usuario_actual)):  
    # Solo Administrativos pueden crear modalidades
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear modalidades")

    dao = UsuariosDAO(request.app.session)
    nuevo = dao.crearModalidad(modalidad)        
    return nuevo
#Obtener modalidad por ID
# @app.get("/modalidades/{id_Modalidad}", tags=["Modalidades"], summary="Obtener una modalidad por ID")
# def obtener_modalidad(id_Modalidad: int,request: Request):
#     dao = UsuariosDAO(request.app.session)
#     modalidad = dao.obtenerModalidad(id_Modalidad)
#     if not modalidad:
#         raise HTTPException(status_code=404, detail="Modalidad no encontrada")
#     return modalidad
# Obtener modalidad por ID
@app.get("/modalidades/{id_Modalidad}", tags=["Modalidades"], summary="Obtener una modalidad por ID")
def obtener_modalidad(id_Modalidad: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para consultar modalidades")

    dao = UsuariosDAO(request.app.session)
    modalidad = dao.obtenerModalidad(id_Modalidad)
    if not modalidad:
        raise HTTPException(status_code=404, detail="Modalidad no encontrada")
    return modalidad
# Modificar modalidad
# @app.put("/modalidades/{id_Modalidad}", tags=["Modalidades"], summary="Modificar una modalidad existente")
# def modificar_modalidad(id_Modalidad: int, modalidad: modalidadCrear,request: Request):
#     dao = UsuariosDAO(request.app.session)
#     actualizado = dao.modificarModalidad(id_Modalidad, modalidad)
#     return actualizado
@app.put("/modalidades/{id_Modalidad}", tags=["Modalidades"], summary="Modificar una modalidad existente")
def modificar_modalidad(id_Modalidad: int, modalidad: modalidadCrear, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden modificar modalidades
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar modalidades")

    dao = UsuariosDAO(request.app.session)
    actualizado = dao.modificarModalidad(id_Modalidad, modalidad)
    return actualizado
# Eliminar modalidad
# @app.delete("/modalidades/{id_Modalidad}", tags=["Modalidades"], summary="Eliminar una modalidad existente")
# def eliminar_modalidad(id_Modalidad: int,request: Request):
#     dao = UsuariosDAO(request.app.session)
#     exito = dao.eliminarModalidad(id_Modalidad)
#     if not exito:
#         raise HTTPException(status_code=404, detail="Modalidad no encontrada")
#     return {"mensaje": "Modalidad eliminada correctamente"}
@app.delete("/modalidades/{id_Modalidad}", tags=["Modalidades"], summary="Eliminar una modalidad existente")
def eliminar_modalidad(id_Modalidad: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden eliminar modalidades
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar modalidades")

    dao = UsuariosDAO(request.app.session)
    exito = dao.eliminarModalidad(id_Modalidad)
    if not exito:
        raise HTTPException(status_code=404, detail="Modalidad no encontrada")
    return {"mensaje": "Modalidad eliminada correctamente"}
# Crear carrera
@app.post("/carreras", tags=["Carreras"], summary="Crear una nueva carrera")
async def crear_carrera(carrera: carreraCrear, request: Request, usuario=Depends(obtener_usuario_actual)):   
    # Solo Administrativos pueden crear carreras
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear carreras")

    dao = UsuariosDAO(request.app.session)
    nuevo = dao.crearCarrera(carrera)         
    return nuevo


# Obtener carrera por ID
@app.get("/carreras/{id_Carrera}", tags=["Carreras"], summary="Obtener una carrera por ID")
def obtener_carrera(id_Carrera: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para consultar carreras")

    dao = UsuariosDAO(request.app.session)
    carrera = dao.obtenerCarrera(id_Carrera)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera


# Modificar carrera
@app.put("/carreras/{id_Carrera}", tags=["Carreras"], summary="Modificar una carrera existente")
def modificar_carrera(id_Carrera: int, carrera: carreraCrear, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden modificar carreras
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar carreras")

    dao = UsuariosDAO(request.app.session)
    actualizado = dao.modificarCarrera(id_Carrera, carrera)
    return actualizado


# Eliminar carrera
@app.delete("/carreras/{id_Carrera}", tags=["Carreras"], summary="Eliminar una carrera existente")
def eliminar_carrera(id_Carrera: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden eliminar carreras
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar carreras")

    dao = UsuariosDAO(request.app.session)
    exito = dao.eliminarCarrera(id_Carrera)
    if not exito:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return {"mensaje": "Carrera eliminada correctamente"}

# Crear grupo
@app.post("/grupos", tags=["Grupos"], summary="Crear un nuevo grupo")
async def crear_grupo(grupo: GrupoCrear, request: Request, usuario=Depends(obtener_usuario_actual)):  
    # Solo Administrativos pueden crear grupos
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear grupos")

    dao = UsuariosDAO(request.app.session)
    try:
        nuevo = dao.crearGrupo(grupo)         
        return nuevo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Obtener grupo por ID
@app.get("/grupos/{id_Grupo}", tags=["Grupos"], summary="Obtener un grupo por ID")
def obtener_grupo(id_Grupo: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para consultar grupos")

    dao = UsuariosDAO(request.app.session)
    grupo = dao.obtenerGrupo(id_Grupo)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo


# Modificar grupo
@app.put("/grupos/{id_Grupo}", tags=["Grupos"], summary="Modificar un grupo existente")
def modificar_grupo(id_Grupo: int, grupo: GrupoCrear, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden modificar grupos
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar grupos")

    dao = UsuariosDAO(request.app.session)
    actualizado = dao.modificarGrupo(id_Grupo, grupo)
    return actualizado


# Eliminar grupo
@app.delete("/grupos/{id_Grupo}", tags=["Grupos"], summary="Eliminar un grupo existente")
def eliminar_grupo(id_Grupo: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden eliminar grupos
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar grupos")

    dao = UsuariosDAO(request.app.session)
    exito = dao.eliminarGrupo(id_Grupo)
    if not exito:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return {"mensaje": "Grupo eliminado correctamente"}

#CRUD para Horarios
# Crear horario
@app.post("/horarios", tags=["Horarios"], summary="Crear un nuevo horario")
async def crear_horario(horario: HorarioCrear, request: Request, usuario=Depends(obtener_usuario_actual)):  
    # Solo Administrativos pueden crear horarios
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear horarios")

    dao = UsuariosDAO(request.app.session)
    nuevo = dao.crearHorario(horario)         
    return nuevo


# Obtener horario por ID
@app.get("/horarios/{id_Horario}", tags=["Horarios"], summary="Obtener un horario por ID")
def obtener_horario(id_Horario: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para consultar horarios")

    dao = UsuariosDAO(request.app.session)
    horario = dao.obtenerHorario(id_Horario)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario


# Modificar horario
@app.put("/horarios/{id_Horario}", tags=["Horarios"], summary="Modificar un horario existente")
def modificar_horario(id_Horario: int, horario: HorarioCrear, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden modificar horarios
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar horarios")

    dao = UsuariosDAO(request.app.session)
    actualizado = dao.modificarHorario(id_Horario, horario)
    return actualizado


# Eliminar horario
@app.delete("/horarios/{id_Horario}", tags=["Horarios"], summary="Eliminar un horario existente")
def eliminar_horario(id_Horario: int, request: Request, usuario=Depends(obtener_usuario_actual)):
    # Solo Administrativos pueden eliminar horarios
    if usuario["rol"] not in ["Administrativo"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar horarios")

    dao = UsuariosDAO(request.app.session)
    exito = dao.eliminarHorario(id_Horario)
    if not exito:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return {"mensaje": "Horario eliminado correctamente"}


#autenticación de usuarios
# @app.post("/usuarios/autenticar",tags=["Usuarios"],summary="Autenticar Usuarios",response_model=UsuarioSalida)
# async def autenticar(usuarioA:UsuarioAutenticar,request:Request)->UsuarioSalida:
#     uDAO=UsuariosDAO(request.app.session)
#     return uDAO.autenticar(usuarioA.email,usuarioA.password)

if __name__ == '__main__':
    uvicorn.run("main:app",reload=True,port=8000,host="127.0.0.1")