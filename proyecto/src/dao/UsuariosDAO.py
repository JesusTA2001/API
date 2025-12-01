from  models.UsuariosModel import vUsuarios, alumnos, profesores, administrador, Niveles, Modalidad, Carrera, Grupo, Horario, AlumnoCrear, ProfesorCrear, AdministradorCrear, nivelesCrear, modalidadCrear, GrupoCrear, carreraCrear, HorarioCrear
class UsuariosDAO:
    def __init__(self, session):
        self.session = session
# CRUD para alumnos
# Crear un nuevo alumno
    def crearAlumno(self, alumno_data: AlumnoCrear) -> alumnos:
        nuevo = alumnos(**alumno_data.dict())
        self.session.add(nuevo)
        self.session.commit()
        self.session.refresh(nuevo)
        return nuevo
    # Obtener un alumno por ID
    def obtenerAlumno(self, id: int) -> alumnos:
        return self.session.get(alumnos, id)

    # Obtener todos los alumnos
    def obtenerAlumnos(self) -> list[alumnos]:
        return self.session.query(alumnos).all()

    # Modificar un alumno existente
    def modificarAlumno(self, id: int, alumno_data: AlumnoCrear) -> alumnos:
        alumno_existente = self.session.get(alumnos, id)
        if not alumno_existente:
            raise Exception("Alumno no encontrado")
        
        # Solo actualiza los campos que no sean 'id'
        for key, value in alumno_data.dict().items():
            if key != "id":
                setattr(alumno_existente, key, value)
        
        self.session.commit()
        self.session.refresh(alumno_existente)
        return alumno_existente

    # Eliminar un alumno
    def eliminarAlumno(self, id: int) -> bool:
        alumno_existente = self.session.get(alumnos, id)
        if not alumno_existente:
            return False
        self.session.delete(alumno_existente)
        self.session.commit()
        return True

    #CRUD para profesores
    # Crear un nuevo profesor

    def crearProfesor(self, profesor_data: ProfesorCrear) -> profesores:
        nuevo = profesores(**profesor_data.dict())
        self.session.add(nuevo)
        self.session.commit()
        self.session.refresh(nuevo)
        return nuevo
    # Obtener profesor por ID
    def obtenerProfesor(self, id_Profesor: int) -> profesores | None:
        return self.session.get(profesores, id_Profesor)

    # Modificar profesor
    def modificarProfesor(self, id_Profesor: int, profesor_data: ProfesorCrear) -> profesores:
        profesor = self.session.get(profesores, id_Profesor)
        if not profesor:
            raise Exception("Profesor no encontrado")
        for key, value in profesor_data.dict().items():
            if key != "id_Profesor":
                setattr(profesor, key, value)
        self.session.commit()
        self.session.refresh(profesor)
        return profesor
        
    # Eliminar profesor
    def eliminarProfesor(self, id_Profesor: int) -> bool:
        profesor = self.session.get(profesores, id_Profesor)
        if not profesor:
            return False
        self.session.delete(profesor)
        self.session.commit()
        return True
        
    #CRUD para Administradores
    # Crear un nuevo Administrador
    def crearAdministrador(self, admin_data: AdministradorCrear) -> administrador:
        nuevo = administrador(**admin_data.dict())
        self.session.add(nuevo)
        self.session.commit()
        self.session.refresh(nuevo)
        return nuevo
    # Obtener administrador por ID
    def obtenerAdministrador(self, id_Administrador: int) -> administrador | None:
        return self.session.get(administrador, id_Administrador)
    # Modificar administrador
    def modificarAdministrador(self, id_Administrador: int, admin_data: AdministradorCrear) -> administrador:
        admin = self.session.get(administrador, id_Administrador)
        if not admin:
            raise Exception("Administrador no encontrado")
        for key, value in admin_data.dict().items():
            if key != "id_Administrador":
                setattr(admin, key, value)
        self.session.commit()
        self.session.refresh(admin)
        return admin

    # Eliminar administrador
    def eliminarAdministrador(self, id_Administrador: int) -> bool:
        admin = self.session.get(administrador, id_Administrador)
        if not admin:
            return False
        self.session.delete(admin)
        self.session.commit()
        return True

    #CRUD para Niveles
    # Crear un nuevo Nivel
    def crearNivel(self, nivel_data: nivelesCrear) -> Niveles:
        nuevo = Niveles(**nivel_data.dict())
        self.session.add(nuevo)
        self.session.commit()
        self.session.refresh(nuevo)
        return nuevo
    # Obtener nivel por ID
    def obtenerNivel(self, id_Nivel: int) -> Niveles | None:
        return self.session.get(Niveles, id_Nivel)
    # Modificar nivel
    def modificarNivel(self, id_Nivel: int, nivel_data: nivelesCrear) -> Niveles:
        nivel = self.session.get(Niveles, id_Nivel)
        if not nivel:
            raise Exception("Nivel no encontrado")
        for key, value in nivel_data.dict().items():
            if key != "id_Nivel":
                setattr(nivel, key, value)
        self.session.commit()
        self.session.refresh(nivel)
        return nivel
    # Eliminar nivel
    def eliminarNivel(self, id_Nivel: int) -> bool:
        nivel = self.session.get(Niveles, id_Nivel)
        if not nivel:
            return False
        self.session.delete(nivel)
        self.session.commit()
        return True
    #CRUD para Modalidad
    # Crear un nueva modalidad
    def crearModalidad(self, modalidad_data: modalidadCrear) -> Modalidad:
        nuevo = Modalidad(**modalidad_data.dict())
        self.session.add(nuevo)
        self.session.commit()
        self.session.refresh(nuevo)
        return nuevo
    #Obtener modalidad por ID
    def obtenerModalidad(self, id_Modalidad: int) -> Modalidad | None:
        return self.session.get(Modalidad, id_Modalidad)
    #Modificar modalidad
    def modificarModalidad(self, id_Modalidad: int, modalidad_data: modalidadCrear) -> Modalidad:
        modalidad = self.session.get(Modalidad, id_Modalidad)
        if not modalidad:
            raise Exception("Modalidad no encontrada")
        for key, value in modalidad_data.dict().items():
            if key != "id_Modalidad":
                setattr(modalidad, key, value)
        self.session.commit()
        self.session.refresh(modalidad)
        return modalidad
    #Eliminar modalidad
    def eliminarModalidad(self, id_Modalidad: int) -> bool:
        modalidad = self.session.get(Modalidad, id_Modalidad)
        if not modalidad:
            return False
        self.session.delete(modalidad)
        self.session.commit()
        return True
    #CRUD para Carrera
    # Crear un nueva Carrera
    def crearCarrera(self, carrera_data: carreraCrear) -> Carrera:
        nuevo = Carrera(**carrera_data.dict())
        self.session.add(nuevo)
        self.session.commit()
        self.session.refresh(nuevo)
        return nuevo
    #Obtener carrera por ID
    def obtenerCarrera(self, id_Carrera: int) -> Carrera | None:
        return self.session.get(Carrera, id_Carrera)
    #Modificar carrera
    def modificarCarrera(self, id_Carrera: int, carrera_data: carreraCrear) -> Carrera:
        carrera = self.session.get(Carrera, id_Carrera)
        if not carrera:
            raise Exception("Carrera no encontrada")
        for key, value in carrera_data.dict().items():
            if key != "id_Carrera":
                setattr(carrera, key, value)
        self.session.commit()
        self.session.refresh(carrera)
        return carrera
    #Eliminar carrera
    def eliminarCarrera(self, id_Carrera: int) -> bool:
        carrera = self.session.get(Carrera, id_Carrera)
        if not carrera:
            return False
        self.session.delete(carrera)
        self.session.commit()
        return True
    #CRUD para Grupo
    # Crear un nuevo Grupo
    def crearGrupo(self, grupo_data: GrupoCrear) -> Grupo:
        nuevo = Grupo(**grupo_data.dict())
        self.session.add(nuevo)
        self.session.commit()
        self.session.refresh(nuevo)
        return nuevo
    #Obtener grupo por ID
    def obtenerGrupo(self, id_Grupo: int) -> Grupo | None:
        return self.session.get(Grupo, id_Grupo)
    #Modificar grupo
    def modificarGrupo(self, id_Grupo: int, grupo_data: GrupoCrear) -> Grupo:
        grupo = self.session.get(Grupo, id_Grupo)
        if not grupo:
            raise Exception("Grupo no encontrado")
        for key, value in grupo_data.dict().items():
            if key != "id_Grupo":
                setattr(grupo, key, value)
        self.session.commit()
        self.session.refresh(grupo)
        return grupo
    #Eliminar grupo
    def eliminarGrupo(self, id_Grupo: int) -> bool:
        grupo = self.session.get(Grupo, id_Grupo)
        if not grupo:
            return False
        self.session.delete(grupo)
        self.session.commit()
        return True
    
    #CRUD para horario
    # Crear un nuevo horario
    def crearHorario(self, horario_data: HorarioCrear) -> Horario:
        # Validación opcional: asegurar que los IDs relacionados existen
        print(horario_data)
        #grupo=self.session.get(Grupo, horario_data.id_Grupo)
        #print(grupo)
        # if not self.session.get(Grupo, horario_data.id_Grupo):
        #     raise Exception("El grupo no existe")
        # if not self.session.get(profesores, horario_data.id_profesor):
        #     raise Exception("El profesor no existe")
        # if not self.session.get(Niveles, horario_data.id_nivel):
        #     raise Exception("El nivel no existe")
        nuevo = Horario(**horario_data.dict())
        self.session.add(nuevo)
        self.session.commit()
        self.session.refresh(nuevo)
        return nuevo
    #Obtener horario por ID
    def obtenerHorario(self, id_Horario: int) -> Horario | None:
        return self.session.get(Horario, id_Horario)
    #Modificar horario
    def modificarHorario(self, id_Horario: int, horario_data: HorarioCrear) -> Horario:
        horario = self.session.get(Horario, id_Horario)
        if not horario:
            raise Exception("Horario no encontrado")
        for key, value in horario_data.dict().items():
            if key != "id_Horario":
                setattr(horario, key, value)
        self.session.commit()
        self.session.refresh(horario)
        return horario
    #Eliminar horario
    def eliminarHorario(self, id_Horario: int) -> bool:
        horario = self.session.get(Horario, id_Horario)
        if not horario:
            return False
        self.session.delete(horario)
        self.session.commit()
        return True
    #Autenticacion de usuarios
    def autenticar(self, email: str, password: str) -> vUsuarios | None:
        # Buscar en alumnos
        user = self.session.query(alumnos).filter_by(correo=email, password=password).first()
        if user:
            return vUsuarios(
                idUsuario=user.id,
                usuario=user.nombre,
                email=user.correo,
                password=user.password,
                tipo="Alumno",
                estatus=True
            )

        # Buscar en profesores
        user = self.session.query(profesores).filter_by(correo=email, password=password).first()
        if user:
            return vUsuarios(
                idUsuario=user.id_Profesor,
                usuario=user.nombre,
                email=user.correo,
                password=user.password,
                tipo="Profesor",
                estatus=True
            )

        # Buscar en administrador
        user = self.session.query(administrador).filter_by(correo=email, password=password).first()
        if user:
            return vUsuarios(
                idUsuario=user.id_Administrador,
                usuario=user.nombre,
                email=user.correo,
                password=user.password,
                tipo="Administrador",
                estatus=True
            )

        # Si no existe en ninguna tabla
        return None

