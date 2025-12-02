from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlmodel import select
from src.dao.database import Conexion
from src.models.UsuariosModel import (
    Nivel, Periodo, CatalogoHorarios, EstadoEnum
)

class CatalogosDAO:
    def __init__(self):
        self.conexion = Conexion()

    # ===========================
    # CRUD: NIVELES
    # ===========================
    def crear_nivel(self, nombre_nivel: str, id_manual: int):
        session = self.conexion.getSession()
        try:
            nuevo = Nivel(id_Nivel=id_manual, nivel=nombre_nivel)
            session.add(nuevo)
            session.commit()
            return {"estatus": True, "mensaje": "Nivel creado exitosamente"}
        except SQLAlchemyError as e:
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()
    def actualizar_nivel(self, id_nivel: int, nombre: str):
        session = self.conexion.getSession()
        try:
            nivel = session.get(Nivel, id_nivel)
            if nivel:
                nivel.nivel = nombre
                session.add(nivel)
                session.commit()
                return {"estatus": True, "mensaje": "Nivel actualizado"}
            return {"estatus": False, "mensaje": "Nivel no encontrado"}
        finally:
            session.close()

    def obtener_niveles(self):
        session = self.conexion.getSession()
        try:
            niveles = session.exec(select(Nivel)).all()
            return {"estatus": True, "data": niveles}
        finally:
            session.close()

    def eliminar_nivel(self, id_nivel: int):
        session = self.conexion.getSession()
        try:
            nivel = session.get(Nivel, id_nivel)
            if nivel:
                session.delete(nivel)
                session.commit()
                return {"estatus": True, "mensaje": "Nivel eliminado"}
            return {"estatus": False, "mensaje": "Nivel no encontrado"}
        except IntegrityError:
            return {"estatus": False, "mensaje": "No se puede eliminar: El nivel está en uso por grupos o alumnos."}
        finally:
            session.close()

    # ===========================
    # CRUD: PERIODOS
    # ===========================
    def crear_periodo(self, id_periodo: int, descripcion: str, anio: int):
        session = self.conexion.getSession()
        try:
            nuevo = Periodo(id_Periodo=id_periodo, descripcion=descripcion, año=anio)
            session.add(nuevo)
            session.commit()
            return {"estatus": True, "mensaje": "Periodo creado"}
        except SQLAlchemyError as e:
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()
    
    def obtener_periodos(self):
        session = self.conexion.getSession()
        try:
            lista = session.exec(select(Periodo)).all()
            return {"estatus": True, "data": lista}
        finally:
            session.close()
    def actualizar_periodo(self, id_periodo: int, descripcion: str, anio: int):
        session = self.conexion.getSession()
        try:
            periodo = session.get(Periodo, id_periodo)
            if periodo:
                periodo.descripcion = descripcion
                periodo.año = anio
                session.add(periodo)
                session.commit()
                return {"estatus": True, "mensaje": "Periodo actualizado"}
            return {"estatus": False, "mensaje": "Periodo no encontrado"}
        finally:
            session.close()
    def eliminar_periodo(self, id_periodo: int):
        session = self.conexion.getSession()
        try:
            periodo = session.get(Periodo, id_periodo)
            if periodo:
                session.delete(periodo)
                session.commit()
                return {"estatus": True, "mensaje": "Periodo eliminado"}
            return {"estatus": False, "mensaje": "Periodo no encontrado"}
        except IntegrityError:
            return {"estatus": False, "mensaje": "No se puede eliminar: El periodo está en uso por grupos."}
        finally:
            session.close()
    # ===========================
    # CRUD: HORARIOS (Soft Delete)
    # ===========================
    def crear_horario(self, data: dict):
        session = self.conexion.getSession()
        try:
            nuevo = CatalogoHorarios(
                ubicacion=data.get('ubicacion'),
                diaSemana=data.get('diaSemana'),
                hora=data.get('hora'),
                estado=EstadoEnum.activo
            )
            session.add(nuevo)
            session.commit()
            return {"estatus": True, "mensaje": "Horario agregado"}
        except Exception as e:
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()
    def actualizar_horario(self, id_horario: int, data: dict):
        session = self.conexion.getSession()
        try:
            horario = session.get(CatalogoHorarios, id_horario)
            if horario:
                if 'ubicacion' in data: horario.ubicacion = data['ubicacion']
                if 'diaSemana' in data: horario.diaSemana = data['diaSemana']
                if 'hora' in data: horario.hora = data['hora']
                session.add(horario)
                session.commit()
                return {"estatus": True, "mensaje": "Horario actualizado"}
            return {"estatus": False, "mensaje": "Horario no encontrado"}
        finally:
            session.close()
            
    def obtener_horarios_activos(self):
        session = self.conexion.getSession()
        try:
            statement = select(CatalogoHorarios).where(CatalogoHorarios.estado == EstadoEnum.activo)
            resultado = session.exec(statement).all()
            return {"estatus": True, "data": resultado}
        finally:
            session.close()

    def eliminar_horario(self, id_horario: int):
        """Cambia el estado a inactivo en lugar de borrar"""
        session = self.conexion.getSession()
        try:
            horario = session.get(CatalogoHorarios, id_horario)
            if horario:
                horario.estado = EstadoEnum.inactivo
                session.add(horario)
                session.commit()
                return {"estatus": True, "mensaje": "Horario desactivado"}
            return {"estatus": False, "mensaje": "Horario no encontrado"}
        finally:
            session.close()