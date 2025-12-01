from sqlmodel import SQLModel, Field
from typing import Optional, List
from pydantic import BaseModel
# ==============================
# Vista: Alumnos con grupo

class vAlumnos(BaseModel):
    idAlumno: int
    nControl: int
    apellidoPaterno: str
    apellidoMaterno: str
    nombreAlumno: str
    correo: str
    genero: str
    CURP: str
    Telefono: str
    Direccion: str
    modalidad_text: str
    nivel_text: str
    id_Grupo: Optional[int] = None
    nombreGrupo: Optional[str] = None
    periodoGrupo: Optional[str] = None

# Vista: Profesores 
class vProfesores(BaseModel):
    id_Profesor: int
    apellidoPaterno: str
    apellidoMaterno: str
    nombreProfesor: str
    email: str
    genero: str
    CURP: str
    telefono: str
    direccion: str
    nivelEstudio: str
    numGrupos: int


# Vista: Grupos 
class vGrupos(BaseModel):
    id_Grupo: int
    nombreGrupo: Optional[str] = None  # corresponde al campo 'Grupo'
    id_Horario: Optional[int] = None
    id_Profesor: Optional[int] = None
    id_Alumno: Optional[int] = None
    id_Nivel: Optional[int] = None
    id_Modalidad: Optional[int] = None
    Periodo: Optional[str] = None


# Vista: Horarios con grupo y profesor
class vHorarios(BaseModel):
    id_Horario: int
    anio: Optional[str] = None
    diaSemana: Optional[str] = None
    id_Grupo: Optional[int] = None
    id_profesor: Optional[int] = None
    id_nivel: Optional[int] = None

# Vista: Carrera
class vCarrera(BaseModel):
    id_Carrera: int
    nombreCarrera: str


class Salida(BaseModel):
    estatus: bool
    mensaje: str
# -----------------------
# Wrappers de salida API
class CarreraSalida(Salida):
    carrera: Optional[vCarrera] = None

class CarrerasSalida(Salida):
    carreras: Optional[List[vCarrera]] = None
# Wrapper común de salida

# Wrappers de salida API
class GrupoSalida(Salida):
    grupo: Optional[vGrupos] = None

class GruposSalida(Salida):
    grupos: Optional[List[vGrupos]] = None

class HorarioSalida(Salida):
    horario: Optional[vHorarios] = None

class HorariosSalida(Salida):
    horarios: Optional[List[vHorarios]] = None

    # Wrappers de salida API
class AlumnoSalida(Salida):
    alumno: Optional[vAlumnos] = None

class AlumnosSalida(Salida):
    alumnos: Optional[List[vAlumnos]] = None


class ProfesorSalida(Salida):
    profesor: Optional[vProfesores] = None

class ProfesoresSalida(Salida):
    profesores: Optional[List[vProfesores]] = None

class GrupoSalida(Salida):
    grupo: Optional[vGrupos] = None

class GruposSalida(Salida):
    grupos: Optional[List[vGrupos]] = None


class HorarioSalida(Salida):
    horario: Optional[vHorarios] = None

class HorariosSalida(Salida):
    horarios: Optional[List[vHorarios]] = None
