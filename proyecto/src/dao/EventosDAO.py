import datetime
from sqlmodel import Session
from models.EventosModel import (
    vAlumnos, AlumnoSalida, AlumnosSalida,
    vProfesores, ProfesorSalida, ProfesoresSalida,
    vGrupos, GrupoSalida, GruposSalida,
    vHorarios, HorarioSalida, HorariosSalida,
    Salida,vCarrera,CarreraSalida,CarrerasSalida
)
class EventosDAO:
    def __init__(self, session: Session):
        self.session = session

    # -----------------------------
    # Alumnos
    # -----------------------------
    def consultarAlumnos(self) -> vAlumnos:
        return self.session.query(vAlumnos).all()

    def consultarAlumnoPorId(self, idAlumno: int) -> AlumnoSalida:
        alumno = self.session.get(vAlumnos, idAlumno)
        salida = AlumnoSalida(estatus=False, mensaje="", alumno=None)
        if alumno:
            salida.estatus = True
            salida.mensaje = f"Alumno encontrado con id: {idAlumno}"
            salida.alumno = alumno
        else:
            salida.mensaje = f"Alumno con id {idAlumno} no existe"
        return salida

    # -----------------------------
    # Profesores
    # -----------------------------
    def consultarProfesores(self) ->vProfesores:
        return self.session.query(vProfesores).all()

    def consultarProfesorPorId(self, idProfesor: int) -> ProfesorSalida:
        profesor = self.session.get(vProfesores, idProfesor)
        salida = ProfesorSalida(estatus=False, mensaje="", profesor=None)
        if profesor:
            salida.estatus = True
            salida.mensaje = f"Profesor encontrado con id: {idProfesor}"
            salida.profesor = profesor
        else:
            salida.mensaje = f"Profesor con id {idProfesor} no existe"
        return salida
    # -----------------------------
    #Carrera
    def consultarCarreras(self) ->vCarrera:
        return self.session.query(vCarrera).all()
    
    # Grupos
    
    def consultarGrupos(self) ->vGrupos:
        return self.session.query(vGrupos).all()

    def consultarGrupoPorId(self, idGrupo: int) -> GrupoSalida:
        grupo = self.session.get(vGrupos, idGrupo)
        salida = GrupoSalida(estatus=False, mensaje="", grupo=None)
        if grupo:
            salida.estatus = True
            salida.mensaje = f"Grupo encontrado con id: {idGrupo}"
            salida.grupo = grupo
        else:
            salida.mensaje = f"Grupo con id {idGrupo} no existe"
        return salida

    # -----------------------------
    # Horarios
    # -----------------------------
    def consultarHorarios(self) ->vHorarios:
        return self.session.query(vHorarios).all()

    def consultarHorarioPorId(self, idHorario: int) -> HorarioSalida:
        horario = self.session.get(vHorarios, idHorario)
        salida = HorarioSalida(estatus=False, mensaje="", horario=None)
        if horario:
            salida.estatus = True
            salida.mensaje = f"Horario encontrado con id: {idHorario}"
            salida.horario = horario
        else:
            salida.mensaje = f"Horario con id {idHorario} no existe"
        return salida