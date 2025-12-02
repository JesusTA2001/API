from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from enum import Enum as PyEnum

# ==============================
# Enums (Para coincidir con el script de BD)
# ==============================
class RolEnum(str, PyEnum):
    ADMINISTRADOR = "ADMINISTRADOR"
    ESTUDIANTE = "ESTUDIANTE"
    PROFESOR = "PROFESOR"
    COORDINADOR = "COORDINADOR"
    DIRECTIVO = "DIRECTIVO"

class EstadoEnum(str, PyEnum):
    activo = "activo"
    inactivo = "inactivo"

class EstadoGrupoEnum(str, PyEnum):
    concluido = "concluido"
    actual = "actual"


# 1. TABLA BASE: DatosPersonales

class DatosPersonales(SQLModel, table=True):
    __tablename__ = "DatosPersonales"
    
    id_dp: Optional[int] = Field(default=None, primary_key=True)
    apellidoPaterno: Optional[str] = Field(max_length=50)
    apellidoMaterno: Optional[str] = Field(max_length=50)
    nombre: Optional[str] = Field(max_length=50)
    email: Optional[str] = Field(max_length=100)
    genero: Optional[str] = Field(max_length=30)
    CURP: Optional[str] = Field(max_length=40)
    telefono: Optional[str] = Field(max_length=50)
    direccion: Optional[str] = Field(max_length=255)

# ==============================
# 2. ESTRUCTURA DE EMPLEADOS
# ==============================
class Empleado(SQLModel, table=True):
    __tablename__ = "Empleado"

    id_empleado: Optional[int] = Field(default=None, primary_key=True)
    id_dp: int = Field(foreign_key="DatosPersonales.id_dp")
    estado: Optional[EstadoEnum] = None
    RFC: Optional[str] = Field(max_length=20)

class Administrador(SQLModel, table=True):
    __tablename__ = "Administrador"

    id_Administrador: Optional[int] = Field(default=None, primary_key=True)
    id_empleado: int = Field(foreign_key="Empleado.id_empleado")
    estado: Optional[EstadoEnum] = None

class Coordinador(SQLModel, table=True):
    __tablename__ = "Coordinador"
    
    id_Coordinador: Optional[int] = Field(default=None, primary_key=True)
    id_empleado: int = Field(foreign_key="Empleado.id_empleado")
    estado: Optional[EstadoEnum] = None

class Directivo(SQLModel, table=True):
    __tablename__ = "Directivo"

    id_Directivo: Optional[int] = Field(default=None, primary_key=True)
    id_empleado: int = Field(foreign_key="Empleado.id_empleado")
    estado: Optional[EstadoEnum] = None

class Profesor(SQLModel, table=True):
    __tablename__ = "Profesor"

    id_Profesor: Optional[int] = Field(default=None, primary_key=True)
    id_empleado: int = Field(foreign_key="Empleado.id_empleado")
    ubicacion: Optional[str] = Field(max_length=50)
    estado: Optional[EstadoEnum] = None
    nivelEstudio: Optional[str] = Field(max_length=50)


# 3. ESTUDIANTE

class Estudiante(SQLModel, table=True):
    __tablename__ = "Estudiante"

    nControl: int = Field(primary_key=True) # Nota: No es auto-increment, es manual (número de control)
    id_dp: int = Field(foreign_key="DatosPersonales.id_dp")
    estado: Optional[EstadoEnum] = None
    ubicacion: Optional[str] = Field(max_length=50)

# 4. LOGIN Y ACCESO

class Usuarios(SQLModel, table=True):
    __tablename__ = "Usuarios"

    id_usuario: Optional[int] = Field(default=None, primary_key=True)
    usuario: str = Field(max_length=50, unique=True)
    contraseña: str = Field(max_length=255)
    rol: RolEnum
    id_relacion: int  # Guardará nControl, id_Profesor, id_Administrador, etc.

class UsuarioAutenticar(SQLModel):
    usuario: str
    password: str

# 5. CATALOGOS Y GRUPOS (Esenciales para que funcione el resto)

class Nivel(SQLModel, table=True):
    __tablename__ = "Nivel"
    id_Nivel: int = Field(primary_key=True)
    nivel: str = Field(max_length=50)

class Periodo(SQLModel, table=True):
    __tablename__ = "Periodo"
    id_Periodo: int = Field(primary_key=True)
    descripcion: str = Field(max_length=50)
    año: int

class CatalogoHorarios(SQLModel, table=True):
    __tablename__ = "CatalogoHorarios"
    id_cHorario: Optional[int] = Field(default=None, primary_key=True)
    ubicacion: Optional[str] = Field(max_length=50)
    diaSemana: Optional[str] = Field(max_length=20)
    hora: Optional[str] = Field(max_length=20)
    estado: Optional[EstadoEnum] = None

class Grupo(SQLModel, table=True):
    __tablename__ = "Grupo"
    id_Grupo: Optional[int] = Field(default=None, primary_key=True)
    grupo: Optional[str] = Field(max_length=50)
    id_Periodo: Optional[int] = Field(foreign_key="Periodo.id_Periodo")
    id_Profesor: Optional[int] = Field(foreign_key="Profesor.id_Profesor")
    id_Nivel: Optional[int] = Field(foreign_key="Nivel.id_Nivel")
    ubicacion: Optional[str] = Field(max_length=50)
    id_cHorario: Optional[int] = Field(foreign_key="CatalogoHorarios.id_cHorario")

# ==============================
# 6. GESTIÓN ACADÉMICA: INSCRIPCIONES, CALIFICACIONES, ASISTENCIA
# ==============================

class EstudianteGrupo(SQLModel, table=True):
    """Tabla intermedia: relación Estudiante-Grupo (inscripciones)"""
    __tablename__ = "EstudianteGrupo"
    
    id_EstudianteGrupo: Optional[int] = Field(default=None, primary_key=True)
    nControl: int = Field(foreign_key="Estudiante.nControl")
    id_Grupo: int = Field(foreign_key="Grupo.id_Grupo")
    estado: EstadoGrupoEnum = Field(default=EstadoGrupoEnum.actual)

class Calificaciones(SQLModel, table=True):
    """Registro de calificaciones por estudiante, grupo y periodo"""
    __tablename__ = "Calificaciones"
    
    id_Calificaciones: Optional[int] = Field(default=None, primary_key=True)
    nControl: int = Field(foreign_key="Estudiante.nControl")
    id_Grupo: int = Field(foreign_key="Grupo.id_Grupo")
    id_Periodo: int = Field(foreign_key="Periodo.id_Periodo")
    id_nivel: int = Field(foreign_key="Nivel.id_Nivel")
    parcial1: Optional[float] = Field(default=0)
    parcial2: Optional[float] = Field(default=0)
    parcial3: Optional[float] = Field(default=0)
    final: Optional[float] = Field(default=0)

class EstudianteCalificaciones(SQLModel, table=True):
    """Tabla intermedia: vincula estudiantes con sus calificaciones"""
    __tablename__ = "EstudianteCalificaciones"
    
    id_EstudianteCalificaciones: Optional[int] = Field(default=None, primary_key=True)
    nControl: int = Field(foreign_key="Estudiante.nControl")
    id_Calificaciones: int = Field(foreign_key="Calificaciones.id_Calificaciones")

class Asistencia(SQLModel, table=True):
    """Registro de asistencias de estudiantes por grupo"""
    __tablename__ = "Asistencia"
    
    id_Asistencia: Optional[int] = Field(default=None, primary_key=True)
    nControl: int = Field(foreign_key="Estudiante.nControl")
    id_Grupo: int = Field(foreign_key="Grupo.id_Grupo")
    fecha: str = Field(max_length=10)  # Formato: YYYY-MM-DD

# ==============================
# MODELOS DE RESPUESTA GENERAL (Pydantic puro para respuestas de API)
# ==============================
class Salida(SQLModel):
    estatus: bool
    mensaje: str

class UsuarioSalida(SQLModel):
    """Modelo para respuesta de usuario autenticado"""
    id_usuario: int
    usuario: str
    rol: RolEnum
    id_relacion: int