from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from src.dao.database import Conexion
from src.models.UsuariosModel import (
    Usuarios, DatosPersonales, Estudiante, Empleado, Profesor, Administrador,
    RolEnum, EstadoEnum
)

class UsuariosDAO:
    def __init__(self):
        self.conexion = Conexion()

    # ==========================================================================
    #  1. GESTIÓN DE ESTUDIANTES (CRUD)
    # ==========================================================================

    # CREAR ESTUDIANTE
    def crear_estudiante(self, datos_dict: dict):
        session = self.conexion.getSession()
        try:
            # 1. Datos Personales
            nuevo_dp = DatosPersonales(
                apellidoPaterno=datos_dict['apellidoPaterno'],
                apellidoMaterno=datos_dict['apellidoMaterno'],
                nombre=datos_dict['nombre'],
                email=datos_dict['email'],
                genero=datos_dict.get('genero'),
                CURP=datos_dict.get('CURP'),
                telefono=datos_dict.get('telefono'),
                direccion=datos_dict.get('direccion')
            )
            session.add(nuevo_dp)
            session.flush() 

            # 2. Estudiante
            nuevo_estudiante = Estudiante(
                nControl=datos_dict['nControl'],
                id_dp=nuevo_dp.id_dp,
                estado=EstadoEnum.activo,
                ubicacion=datos_dict.get('ubicacion', 'S/N')
            )
            session.add(nuevo_estudiante)
            
            # 3. Usuario Login
            nuevo_usuario = Usuarios(
                usuario=datos_dict['usuario'],
                contraseña=datos_dict['password'],
                rol=RolEnum.ESTUDIANTE,
                id_relacion=datos_dict['nControl']
            )
            session.add(nuevo_usuario)

            session.commit()
            session.refresh(nuevo_estudiante)
            return {"estatus": True, "mensaje": "Estudiante registrado correctamente"}
        except SQLAlchemyError as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    # LEER ESTUDIANTE (JOIN Estudiante + DatosPersonales)
    def obtener_estudiante(self, nControl: int):
        session = self.conexion.getSession()
        try:
            statement = select(Estudiante, DatosPersonales).where(
                Estudiante.id_dp == DatosPersonales.id_dp
            ).where(Estudiante.nControl == nControl)
            
            resultado = session.exec(statement).first()
            
            if resultado:
                estudiante, datos = resultado
                # Retornamos un diccionario combinado
                respuesta = estudiante.model_dump()
                respuesta.update(datos.model_dump())
                return {"estatus": True, "data": respuesta}
            else:
                return {"estatus": False, "mensaje": "Estudiante no encontrado"}
        finally:
            session.close()

    # MODIFICAR ESTUDIANTE
    def modificar_estudiante(self, nControl: int, nuevos_datos: dict):
        session = self.conexion.getSession()
        try:
            estudiante = session.get(Estudiante, nControl)
            if not estudiante:
                return {"estatus": False, "mensaje": "Estudiante no encontrado"}
            
            # Actualizar Datos Personales
            dp = session.get(DatosPersonales, estudiante.id_dp)
            if dp:
                for key, value in nuevos_datos.items():
                    if hasattr(dp, key) and value is not None:
                        setattr(dp, key, value)
            
            # Actualizar Datos Propios del Estudiante (ej. ubicacion)
            if 'ubicacion' in nuevos_datos:
                estudiante.ubicacion = nuevos_datos['ubicacion']

            session.add(dp)
            session.add(estudiante)
            session.commit()
            return {"estatus": True, "mensaje": "Estudiante modificado correctamente"}
        except SQLAlchemyError as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    # ELIMINAR ESTUDIANTE (SOFT DELETE - Cambiar a Inactivo)
    def eliminar_estudiante(self, nControl: int):
        session = self.conexion.getSession()
        try:
            estudiante = session.get(Estudiante, nControl)
            if estudiante:
                estudiante.estado = EstadoEnum.inactivo
                session.add(estudiante)
                session.commit()
                return {"estatus": True, "mensaje": "Estudiante dado de baja (inactivo)"}
            return {"estatus": False, "mensaje": "Estudiante no encontrado"}
        except SQLAlchemyError as e:
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    # ==========================================================================
    #  2. GESTIÓN DE PROFESORES (CRUD)
    # ==========================================================================

    # CREAR PROFESOR
    def crear_profesor(self, datos_dict: dict):
        session = self.conexion.getSession()
        try:
            # 1. Datos Personales
            nuevo_dp = DatosPersonales(
                apellidoPaterno=datos_dict['apellidoPaterno'],
                apellidoMaterno=datos_dict['apellidoMaterno'],
                nombre=datos_dict['nombre'],
                email=datos_dict['email'],
                genero=datos_dict.get('genero'),
                CURP=datos_dict.get('CURP'),
                telefono=datos_dict.get('telefono'),
                direccion=datos_dict.get('direccion')
            )
            session.add(nuevo_dp)
            session.flush()

            # 2. Empleado Base
            nuevo_empleado = Empleado(id_dp=nuevo_dp.id_dp, estado=EstadoEnum.activo, RFC=datos_dict.get('RFC'))
            session.add(nuevo_empleado)
            session.flush()

            # 3. Profesor
            nuevo_profesor = Profesor(
                id_empleado=nuevo_empleado.id_empleado,
                ubicacion=datos_dict.get('ubicacion'),
                nivelEstudio=datos_dict.get('nivelEstudio'),
                estado=EstadoEnum.activo
            )
            session.add(nuevo_profesor)
            session.flush()

            # 4. Usuario
            nuevo_usuario = Usuarios(
                usuario=datos_dict['usuario'],
                contraseña=datos_dict['password'],
                rol=RolEnum.PROFESOR,
                id_relacion=nuevo_profesor.id_Profesor
            )
            session.add(nuevo_usuario)

            session.commit()
            return {"estatus": True, "mensaje": "Profesor registrado correctamente"}
        except SQLAlchemyError as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    # LEER PROFESOR (JOIN Profesor -> Empleado -> DatosPersonales)
    def obtener_profesor(self, id_Profesor: int):
        session = self.conexion.getSession()
        try:
            statement = select(Profesor, Empleado, DatosPersonales)\
                .join(Empleado, Profesor.id_empleado == Empleado.id_empleado)\
                .join(DatosPersonales, Empleado.id_dp == DatosPersonales.id_dp)\
                .where(Profesor.id_Profesor == id_Profesor)
            
            resultado = session.exec(statement).first()
            
            if resultado:
                prof, emp, dp = resultado
                data = {**prof.model_dump(), **emp.model_dump(), **dp.model_dump()}
                return {"estatus": True, "data": data}
            else:
                return {"estatus": False, "mensaje": "Profesor no encontrado"}
        finally:
            session.close()

    # MODIFICAR PROFESOR
    def modificar_profesor(self, id_Profesor: int, nuevos_datos: dict):
        session = self.conexion.getSession()
        try:
            profesor = session.get(Profesor, id_Profesor)
            if not profesor:
                return {"estatus": False, "mensaje": "Profesor no encontrado"}
            
            empleado = session.get(Empleado, profesor.id_empleado)
            dp = session.get(DatosPersonales, empleado.id_dp)

            # Actualizar Datos Personales
            for key, value in nuevos_datos.items():
                if hasattr(dp, key) and value is not None:
                    setattr(dp, key, value)
            
            # Actualizar Datos Profesor
            if 'nivelEstudio' in nuevos_datos:
                profesor.nivelEstudio = nuevos_datos['nivelEstudio']
            if 'ubicacion' in nuevos_datos:
                profesor.ubicacion = nuevos_datos['ubicacion']
            if 'RFC' in nuevos_datos:
                empleado.RFC = nuevos_datos['RFC']

            session.add(dp)
            session.add(empleado)
            session.add(profesor)
            session.commit()
            return {"estatus": True, "mensaje": "Profesor modificado correctamente"}
        except SQLAlchemyError as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    # ELIMINAR PROFESOR (Soft Delete)
    def eliminar_profesor(self, id_Profesor: int):
        session = self.conexion.getSession()
        try:
            profesor = session.get(Profesor, id_Profesor)
            if profesor:
                # Damos de baja al profesor y al empleado
                profesor.estado = EstadoEnum.inactivo
                empleado = session.get(Empleado, profesor.id_empleado)
                if empleado:
                    empleado.estado = EstadoEnum.inactivo
                    session.add(empleado)
                
                session.add(profesor)
                session.commit()
                return {"estatus": True, "mensaje": "Profesor dado de baja"}
            return {"estatus": False, "mensaje": "Profesor no encontrado"}
        finally:
            session.close()
# ==========================================================================
    #  3. GESTIÓN DE ADMINISTRADORES (CRUD)
    # ==========================================================================

    # CREAR ADMINISTRADOR
    def crear_administrador(self, datos_dict: dict):
        session = self.conexion.getSession()
        try:
            # 1. Datos Personales
            nuevo_dp = DatosPersonales(
                apellidoPaterno=datos_dict['apellidoPaterno'],
                apellidoMaterno=datos_dict['apellidoMaterno'],
                nombre=datos_dict['nombre'],
                email=datos_dict['email'],
                genero=datos_dict.get('genero'),
                CURP=datos_dict.get('CURP'),
                telefono=datos_dict.get('telefono'),
                direccion=datos_dict.get('direccion')
            )
            session.add(nuevo_dp)
            session.flush()

            # 2. Empleado Base
            nuevo_empleado = Empleado(
                id_dp=nuevo_dp.id_dp, 
                estado=EstadoEnum.activo,
                RFC=datos_dict.get('RFC')
            )
            session.add(nuevo_empleado)
            session.flush()

            # 3. Administrador
            nuevo_admin = Administrador(
                id_empleado=nuevo_empleado.id_empleado,
                estado=EstadoEnum.activo
            )
            session.add(nuevo_admin)
            session.flush()

            # 4. Usuario
            nuevo_usuario = Usuarios(
                usuario=datos_dict['usuario'],
                contraseña=datos_dict['password'],
                rol=RolEnum.ADMINISTRADOR,
                id_relacion=nuevo_admin.id_Administrador
            )
            session.add(nuevo_usuario)

            session.commit()
            return {"estatus": True, "mensaje": "Administrador registrado correctamente"}
        except SQLAlchemyError as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    # LEER ADMINISTRADOR
    def obtener_administrador(self, id_admin: int):
        session = self.conexion.getSession()
        try:
            statement = select(Administrador, Empleado, DatosPersonales)\
                .join(Empleado, Administrador.id_empleado == Empleado.id_empleado)\
                .join(DatosPersonales, Empleado.id_dp == DatosPersonales.id_dp)\
                .where(Administrador.id_Administrador == id_admin)
            
            resultado = session.exec(statement).first()
            
            if resultado:
                admin, emp, dp = resultado
                # Unimos los diccionarios ignorando duplicados
                data = {**admin.model_dump(), **emp.model_dump(), **dp.model_dump()}
                return {"estatus": True, "data": data}
            else:
                return {"estatus": False, "mensaje": "Administrador no encontrado"}
        finally:
            session.close()

    # MODIFICAR ADMINISTRADOR
    def modificar_administrador(self, id_admin: int, nuevos_datos: dict):
        session = self.conexion.getSession()
        try:
            admin = session.get(Administrador, id_admin)
            if not admin:
                return {"estatus": False, "mensaje": "Administrador no encontrado"}
            
            empleado = session.get(Empleado, admin.id_empleado)
            dp = session.get(DatosPersonales, empleado.id_dp)

            # Actualizar Datos Personales
            for key, value in nuevos_datos.items():
                if hasattr(dp, key) and value is not None:
                    setattr(dp, key, value)
            
            # Actualizar RFC si viene
            if 'RFC' in nuevos_datos:
                empleado.RFC = nuevos_datos['RFC']

            session.add(dp)
            session.add(empleado)
            session.add(admin)
            session.commit()
            return {"estatus": True, "mensaje": "Administrador modificado correctamente"}
        except SQLAlchemyError as e:
            session.rollback()
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()

    # ELIMINAR ADMINISTRADOR (Soft Delete)
    def eliminar_administrador(self, id_admin: int):
        session = self.conexion.getSession()
        try:
            admin = session.get(Administrador, id_admin)
            if admin:
                admin.estado = EstadoEnum.inactivo
                empleado = session.get(Empleado, admin.id_empleado)
                if empleado:
                    empleado.estado = EstadoEnum.inactivo
                    session.add(empleado)
                
                session.add(admin)
                session.commit()
                return {"estatus": True, "mensaje": "Administrador dado de baja"}
            return {"estatus": False, "mensaje": "Administrador no encontrado"}
        finally:
            session.close()

    # ==========================================================================
    #  4. AUTENTICACIÓN
    # ==========================================================================
    def autenticar_usuario(self, usuario: str, password: str):
        session = self.conexion.getSession()
        try:
            statement = select(Usuarios).where(Usuarios.usuario == usuario).where(Usuarios.contraseña == password)
            resultado = session.exec(statement).first()
            if resultado:
                return {"estatus": True, "usuario": resultado, "mensaje": "Autenticación exitosa"}
            else:
                return {"estatus": False, "mensaje": "Credenciales incorrectas"}
        except Exception as e:
            return {"estatus": False, "mensaje": str(e)}
        finally:
            session.close()