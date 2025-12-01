from sqlmodel import SQLModel,Field
from typing import Optional
from pydantic import BaseModel
class vUsuarios(SQLModel):
    idUsuario: int
    usuario: str
    email: str
    password: str
    tipo: str   # "Alumno", "Profesor" o "Administrador"
    estatus: bool = True 
# ==============================
# Tablas de Usuarios
# ==============================
class Alumno(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)  # auto-increment
    nControl: int
    apellidoPaterno: str
    apellidoMaterno: str
    nombre: str
    email: str
    genero: str
    password: str
    CURP: str
    telefono: str
    Direccion: str
    Modalidad: str
    Nivel: str

# --- Esquema de entrada (request) ---
class AlumnoCrear(Alumno):
    pass

# --- Esquema de salida (response) ---
class AlumnoSalida(Alumno):
    id: int

class alumnos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    nControl: int
    apellidoPaterno: str
    apellidoMaterno: str
    nombre: str
    email: str
    genero: str
    password: str
    CURP: str
    telefono: str
    Direccion: str
    Modalidad: str
    Nivel: str
# profesores
class Profesores(SQLModel):
    id_Profesor:int=Field(primary_key=True)
    apellidoPaterno:str
    apellidoMaterno:str
    nombre:str
    email:str
    genero:str
    password:str
    CURP:str
    telefono:str
    direccion:str
    nivelEstudio:str

class ProfesorCrear(Profesores):
    pass

class ProfesorSalida(Profesores):
    id_Profesor:int

class profesores(SQLModel,table=True):
    id_Profesor:int=Field(primary_key=True)
    apellidoPaterno:str
    apellidoMaterno:str
    nombre:str
    email:str
    genero:str
    password:str
    CURP:str
    telefono:str
    direccion:str
    nivelEstudio:str

#administrador
class Administrador(SQLModel):
    id_Administrador:int=Field(primary_key=True)
    apellidoPaterno:str
    apellidoMaterno:str
    nombre:str
    email:str
    genero:str
    password:str
    CURP:str
    telefono:str
    direccion:str
    
class AdministradorCrear(Administrador):
    pass

class AdministradorSalida(Administrador):
    id_Administrador:int

class administrador(SQLModel,table=True):
    id_Administrador:int=Field(primary_key=True)
    apellidoPaterno:str
    apellidoMaterno:str
    nombre:str
    email:str
    genero:str
    password:str
    CURP:str
    telefono:str
    direccion:str

#Niveles
class niveles(SQLModel):
    id_Nivel:int=Field(primary_key=True)
    Nivel:str
class nivelesCrear(niveles):
    pass

class nivelesSalida(niveles):
    id_Nivel:int

class Niveles(SQLModel,table=True):
    id_Nivel:int=Field(primary_key=True)
    Nivel:str

#Modalidad
class modalidad(SQLModel):
    id_Modalidad:int=Field(primary_key=True)
    Modalidad:str

class modalidadCrear(modalidad):
    pass

class modalidadSalida(modalidad):
    id_Modalidad:int

class Modalidad(SQLModel,table=True):
    id_Modalidad:int=Field(primary_key=True)
    Modalidad:str

#Carreras
class carrera(SQLModel):
    id_Carrera:int=Field(primary_key=True)
    Carrera:str

class carreraCrear(carrera):
    pass

class carreraSalida(carrera):
    id_Carrera:int

class Carrera(SQLModel,table=True):
    id_Carrera:int=Field(primary_key=True)
    Carrera:str

# Horario
class Horario(SQLModel, table=True):
    id_Horario: Optional[int] = Field(default=None, primary_key=True)
    anio: str
    id_Grupo: int
    id_profesor: int
    id_nivel: int
    diaSemana: str

class HorarioCrear(SQLModel):
    anio: str
    id_Grupo: int
    id_profesor: int
    id_nivel: int
    diaSemana: str

class HorarioSalida(Horario):
    pass

#Grupo
# class grupo(SQLModel):
#     id_Grupo:int=Field(primary_key=True)
#     Grupo:str
#     id_Horario: int = Field(foreign_key="Horario.id_Horario")
#     id_Profesor: int = Field(foreign_key="profesores.id_Profesor")
#     id_Alumno: int = Field(foreign_key="alumnos.id")
#     id_Nivel: int = Field(foreign_key="niveles.id_Nivel")
#     id_Modalidad: int = Field(foreign_key="modalidad.id_Modalidad")
#     Periodo: str

#Grupo
class Grupo(SQLModel, table=True):
    id_Grupo: Optional[int] = Field(default=None, primary_key=True)
    Grupo: str
    id_Horario: int #= Field(foreign_key="horario.id_Horario")
    id_Profesor: int #= Field(foreign_key="profesores.id_Profesor")
    id_Alumno: int #= Field(foreign_key="alumnos.id")
    id_Nivel: int #= Field(foreign_key="niveles.id_Nivel")
    id_Modalidad: int #= Field(foreign_key="modalidad.id_Modalidad")
    Periodo: str

class GrupoCrear(SQLModel):
    Grupo: str
    id_Horario: int
    id_Profesor: int
    id_Alumno: int
    id_Nivel: int
    id_Modalidad: int
    Periodo: str

class GrupoSalida(Grupo):
    pass

class UsuarioSalida(BaseModel):
    usuario: Optional[alumnos | profesores | administrador] = None

class UsuarioAutenticar(SQLModel):
    email:str
    password:str

class Salida(BaseModel):
    estatus: bool
    mensaje: str