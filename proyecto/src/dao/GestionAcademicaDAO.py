from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlmodel import select
from src.dao.database import Conexion
from src.models.UsuariosModel import (
    Grupo, EstudianteGrupo, Calificaciones, Asistencia, 
    EstudianteCalificaciones, EstadoGrupoEnum, DatosPersonales, Estudiante,
    Nivel, Periodo
)

class GestionAcademicaDAO:
    def __init__(self):
        self.conexion = Conexion()

    # -------------------------
    # 1. GESTIÓN DE GRUPOS (Ya existente)
    # -------------------------
    def crear_grupo(self, data: dict):
        session = self.conexion.getSession()
        try:
            nuevo_grupo = Grupo(
                grupo=data['grupo'],
                id_Periodo=data['id_Periodo'],
                id_Profesor=data['id_Profesor'],
                id_Nivel=data['id_Nivel'],
                ubicacion=data.get('ubicacion'),
                id_cHorario=data['id_cHorario']
            )
            session.add(nuevo_grupo)
            session.commit()
            return {"estatus": True, "mensaje": "Grupo creado exitosamente"}
        except Exception as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    def obtener_grupos_detalle(self):
        session = self.conexion.getSession()
        try:
            statement = select(Grupo) # Aquí puedes mejorar con JOINS como vimos antes
            resultados = session.exec(statement).all()
            return {"estatus": True, "data": resultados}
        finally:
            session.close()

    def modificar_grupo(self, id_grupo: int, datos: dict):
        session = self.conexion.getSession()
        try:
            grupo = session.get(Grupo, id_grupo)
            if not grupo:
                return {"estatus": False, "mensaje": "Grupo no encontrado"}
            
            # Actualizar solo los campos proporcionados
            if 'grupo' in datos: grupo.grupo = datos['grupo']
            if 'id_Periodo' in datos: grupo.id_Periodo = datos['id_Periodo']
            if 'id_Profesor' in datos: grupo.id_Profesor = datos['id_Profesor']
            if 'id_Nivel' in datos: grupo.id_Nivel = datos['id_Nivel']
            if 'ubicacion' in datos: grupo.ubicacion = datos['ubicacion']
            if 'id_cHorario' in datos: grupo.id_cHorario = datos['id_cHorario']
            
            session.add(grupo)
            session.commit()
            return {"estatus": True, "mensaje": "Grupo actualizado correctamente"}
        except Exception as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    def eliminar_grupo(self, id_grupo: int):
        session = self.conexion.getSession()
        try:
            grupo = session.get(Grupo, id_grupo)
            if not grupo:
                return {"estatus": False, "mensaje": "Grupo no encontrado"}
            
            session.delete(grupo)
            session.commit()
            return {"estatus": True, "mensaje": "Grupo eliminado correctamente"}
        except IntegrityError:
            session.rollback()
            return {"estatus": False, "mensaje": "No se puede eliminar: El grupo tiene estudiantes inscritos o registros asociados"}
        except Exception as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    # -------------------------
    # 2. INSCRIPCIÓN (Estudiante -> Grupo) - NUEVO
    # -------------------------
    def inscribir_estudiante(self, nControl: int, id_Grupo: int):
        session = self.conexion.getSession()
        try:
            # Verificar si ya existe
            inscripcion = EstudianteGrupo(
                nControl=nControl,
                id_Grupo=id_Grupo,
                estado=EstadoGrupoEnum.actual
            )
            session.add(inscripcion)
            session.commit()
            return {"estatus": True, "mensaje": "Estudiante inscrito correctamente"}
        except IntegrityError:
            session.rollback()
            return {"estatus": False, "mensaje": "El estudiante ya está inscrito en este grupo o datos inválidos."}
        except Exception as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    def obtener_estudiantes_por_grupo(self, id_Grupo: int):
        """ Obtiene la lista de alumnos inscritos en un grupo """
        session = self.conexion.getSession()
        try:
            # Join: EstudianteGrupo -> Estudiante -> DatosPersonales
            statement = select(Estudiante.nControl, DatosPersonales.nombre, DatosPersonales.apellidoPaterno)\
                .select_from(EstudianteGrupo)\
                .join(Estudiante, Estudiante.nControl == EstudianteGrupo.nControl)\
                .join(DatosPersonales, Estudiante.id_dp == DatosPersonales.id_dp)\
                .where(EstudianteGrupo.id_Grupo == id_Grupo)\
                .where(EstudianteGrupo.estado == EstadoGrupoEnum.actual)
            
            resultados = session.exec(statement).all()
            lista = [{"nControl": row[0], "nombre": f"{row[1]} {row[2]}"} for row in resultados]
            return {"estatus": True, "data": lista}
        except Exception as e:
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    # -------------------------
    # 3. CALIFICACIONES - NUEVO
    # -------------------------
    def asignar_calificacion(self, data: dict):
        """
        Recibe: {nControl, id_Grupo, id_Periodo, id_nivel, parcial1, parcial2, parcial3, final}
        """
        session = self.conexion.getSession()
        try:
            # Crear registro en tabla Calificaciones
            nueva_calif = Calificaciones(
                nControl=data['nControl'],
                id_Grupo=data['id_Grupo'],
                id_Periodo=data['id_Periodo'],
                id_nivel=data['id_nivel'],
                parcial1=data.get('parcial1', 0),
                parcial2=data.get('parcial2', 0),
                parcial3=data.get('parcial3', 0),
                final=data.get('final', 0)
            )
            session.add(nueva_calif)
            session.flush() # Para obtener el id generado

            # Vincular en la tabla intermedia EstudianteCalificaciones (según tu script)
            vinculo = EstudianteCalificaciones(
                nControl=data['nControl'],
                id_Calificaciones=nueva_calif.id_Calificaciones
            )
            session.add(vinculo)
            session.commit()
            return {"estatus": True, "mensaje": "Calificación registrada"}
        except Exception as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    def obtener_calificaciones_estudiante(self, nControl: int):
        session = self.conexion.getSession()
        try:
            # Join EstudianteCalificaciones -> Calificaciones -> Nivel/Periodo/Grupo
            statement = select(Calificaciones, Nivel.nivel, Periodo.descripcion, Grupo.grupo)\
                .join(EstudianteCalificaciones, EstudianteCalificaciones.id_Calificaciones == Calificaciones.id_Calificaciones)\
                .join(Nivel, Calificaciones.id_nivel == Nivel.id_Nivel)\
                .join(Periodo, Calificaciones.id_Periodo == Periodo.id_Periodo)\
                .join(Grupo, Calificaciones.id_Grupo == Grupo.id_Grupo)\
                .where(Calificaciones.nControl == nControl)
            
            resultados = session.exec(statement).all()
            lista = []
            for row in resultados:
                calif, niv, per, gru = row
                datos = calif.model_dump()
                datos['nombre_nivel'] = niv
                datos['nombre_periodo'] = per
                datos['nombre_grupo'] = gru
                lista.append(datos)
            return {"estatus": True, "data": lista}
        except Exception as e:
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    def modificar_calificacion(self, data: dict):
        # Requiere id_Calificaciones en el dict
        session = self.conexion.getSession()
        try:
            id_c = data.get('id_Calificaciones')
            calif = session.get(Calificaciones, id_c)
            if not calif:
                return {"estatus": False, "mensaje": "Registro de calificación no encontrado"}
            
            if 'parcial1' in data: calif.parcial1 = data['parcial1']
            if 'parcial2' in data: calif.parcial2 = data['parcial2']
            if 'parcial3' in data: calif.parcial3 = data['parcial3']
            if 'final' in data: calif.final = data['final']
            
            session.add(calif)
            session.commit()
            return {"estatus": True, "mensaje": "Calificaciones actualizadas"}
        except Exception as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()
    # -------------------------
    # 4. ASISTENCIA - NUEVO
    # -------------------------
    def registrar_asistencia(self, nControl: int, id_Grupo: int, fecha: str):
        session = self.conexion.getSession()
        try:
            # Convertir fecha de DD/MM/YYYY o DD-MM-YYYY a YYYY-MM-DD si es necesario
            from datetime import datetime
            if '/' in fecha:
                fecha_obj = datetime.strptime(fecha, '%d/%m/%Y')
                fecha = fecha_obj.strftime('%Y-%m-%d')
            elif '-' in fecha and fecha.split('-')[0].isdigit() and len(fecha.split('-')[0]) <= 2:
                fecha_obj = datetime.strptime(fecha, '%d-%m-%Y')
                fecha = fecha_obj.strftime('%Y-%m-%d')
            
            nueva_asistencia = Asistencia(
                nControl=nControl,
                id_Grupo=id_Grupo,
                fecha=fecha # Formato YYYY-MM-DD
            )
            session.add(nueva_asistencia)
            session.commit()
            return {"estatus": True, "mensaje": "Asistencia registrada"}
        except ValueError as ve:
            session.rollback()
            return {"estatus": False, "mensaje": f"Formato de fecha inválido. Use DD/MM/YYYY o YYYY-MM-DD: {str(ve)}"}
        except Exception as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()