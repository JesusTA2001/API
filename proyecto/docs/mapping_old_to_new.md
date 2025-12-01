Mapping: esquema antiguo (`ingles`) -> nuevo (`proyectoIngles`)

Resumen general
- Propósito: documentar cómo mapear las tablas/columnas del esquema antiguo que usa el código actual hacia las nuevas tablas/columnas del esquema `proyectoIngles`.
- Enfoque: por cada tabla antigua, listar columnas y la(s) tabla(s) destino en la nueva base, notas de transformación y acciones de código necesarias (modelos, DAOs, endpoints).

1) Tabla `alumnos` (antigua)
- Campos relevantes (ejemplo): id, nControl, apellidoPaterno, apellidoMaterno, nombre, email, genero, password, CURP, telefono, Direccion, Modalidad, Nivel
- Nuevo destino:
  - `DatosPersonales` -> campos personales: `apellidoPaterno`, `apellidoMaterno`, `nombre`, `email`, `genero`, `CURP`, `telefono`, `direccion` (mapear `Direccion` -> `direccion`).
  - `Estudiante` -> campos académicos/propios del estudiante: `nControl` -> `matricula` (o `nControl` si se mantiene), `id_DatosPersonales` -> FK a `DatosPersonales.id_dp`, `id_nivel` -> FK a `Nivel.id_nivel`, `id_modalidad` -> FK a `Modalidad.id_modalidad`, `id_usuario` -> FK a `Usuarios.id_usuario` (si corresponda)
- Acciones de código:
  - Crear/ajustar modelos: `DatosPersonales`, `Estudiante` (SQLModel) y esquemas Pydantic para creación/lectura.
  - Adapatar `UsuariosDAO.crearAlumno` para insertar en `DatosPersonales` y `Estudiante` en dos pasos (o usar vistas/procedures).
  - Revisar endpoints que devuelven `alumnos` para usar nuevo `vAlumnos`/view o construir response combinando `DatosPersonales` + `Estudiante`.

2) Tabla `profesores` (antigua)
- Campos: id_Profesor, apellidoPaterno, apellidoMaterno, nombre, email, genero, password, CURP, telefono, direccion, nivelEstudio
- Nuevo destino:
  - `DatosPersonales` -> datos personales (igual que alumnos).
  - `Profesor` -> `id_empleado` o `id_profesor` con FK a `DatosPersonales.id_dp` y campos propios (nivelEstudio).
  - `Empleado` puede ser usado como tabla genérica para roles de personal; `Profesor` extiende o referencia `Empleado`.
- Acciones:
  - Implementar `Profesor` + `Empleado` + `DatosPersonales` modelos.
  - Cambiar `crearProfesor` para crear `DatosPersonales` + `Empleado`/`Profesor` y posiblemente `Usuarios`.

3) Tabla `administrador` (antigua)
- Similar a profesores: mapear a `DatosPersonales` + `Empleado` (rol Administrativo) y a `Usuarios` para credenciales si aplica.

4) Tabla `Grupo` (antigua)
- Campos: id_Grupo (antes INT), Grupo (nombre), id_Horario, id_Profesor, id_Alumno, id_Nivel, id_Modalidad, Periodo
- Nuevo destino:
  - `Grupo` (nuevo): `id_Grupo` VARCHAR(50) PK (ahora string), `nombre_grupo` (o `nombre`), `id_periodo` FK a `Periodo.id_periodo`, `id_nivel` FK a `Nivel.id_nivel`, `id_modalidad` FK a `Modalidad.id_modalidad`, `id_profesor` FK a `Profesor.id_profesor`, `capacidad`, `seccion`, etc.
- Acciones:
  - Actualizar modelo `Grupo` (SQLModel) para usar `id_Grupo: Optional[str]` y renombrar campos según el nuevo esquema.
  - Actualizar DAO y endpoints: métodos de búsqueda/creación/actualización deben manejar `id_Grupo` string, y validar `Periodo`, `Nivel`, `Modalidad`, `Profesor`.
  - Migración de datos: convertir int->string para PKs (posible renombrado o gen nuevo id).

5) Tabla `Horario` (antigua)
- Campos: id_Horario, anio, id_Grupo, id_profesor, id_nivel, diaSemana
- Nuevo destino:
  - `CatalogoHorarios` -> `id_catalogo` PK (string), `diaSemana`, `horaInicio`, `horaFin`.
  - `Grupo` puede referenciar a `CatalogoHorarios` o existir una relación `Grupo` <-> `CatalogoHorarios` (dependiendo del diseño final).
- Acciones:
  - Crear modelo `CatalogoHorarios` y adaptar `crearHorario` para insertar allí o enlazarlo.
  - Validar integridad con `Grupo` y `Profesor`.

6) Tabla `Niveles` (antigua)
- Campos: id_Nivel(int), Nivel(str)
- Nuevo destino:
  - `Nivel` (nuevo): `id_nivel` VARCHAR(50) PK, `nombre`, `descripcion`, `horas`, `precio`.
- Acciones:
  - Cambiar tipo en modelos a `str` (clave textual) y actualizar DAOs y endpoints.

7) Tabla `Modalidad` (antigua)
- Campos: id_Modalidad, Modalidad
- Nuevo destino: `Modalidad` (mismo concepto) pero revisar tipos y constraints.
- Acciones: ajustar modelos/DAOs si cambian los nombres de columnas.

8) Autenticación / `Usuarios`
- En el nuevo esquema hay una tabla `Usuarios` central que referencia a `DatosPersonales`, `Empleado` o `Estudiante` y contiene `email`, `password`, `rol`, `estatus`.
- Acciones:
  - Cambiar `autenticarDAO` y `UsuariosDAO.autenticar` para consultar la tabla `Usuarios` (si implementada) en vez de consultar `alumnos`/`profesores`/`administrador` por separado.
  - Si `Usuarios` no está poblada, adaptar la creación de usuarios al crear estudiantes/empleados para insertar también en `Usuarios`.

Cambios por archivo (propuesta inmediata)
- `src/models/UsuariosModel.py`:
  - Definir nuevos modelos: `DatosPersonales`, `Empleado`, `Profesor`, `Estudiante`, `Usuarios`, `Nivel` (id string), `CatalogoHorarios`, `Grupo` (id string), `Periodo`.
  - Mantener wrappers de vista (`vAlumnos`, `vGrupos`, `vHorarios`) pero actualizarlos para los nuevos campos y tipos.
  - Evitar duplicados: usar un único tipo con `table=True` para cada tabla y esquemas de entrada (`Crear`/`Actualizar`) como Pydantic `BaseModel` o SQLModel sin `table=True`.

- `src/dao/UsuariosDAO.py` y otros DAOs:
  - Reemplazar operaciones directas sobre tablas antiguas por operaciones que creen/lean las nuevas tablas en el orden correcto (p.ej. crear DatosPersonales antes de Estudiante).
  - Añadir validaciones FK (ya añadidas parcialmente) y mapear tipos (int->str donde aplique).

- `src/main.py`:
  - Ajustar firmas de endpoints (tipos de path/query) que usan `id_Grupo` como `int` a `str` si corresponde.
  - Actualizar `response_model` y ejemplos de payload a los nuevos esquemas.

Plan de trabajo recomendado (por prioridad)
1. Modelado: Crear los nuevos modelos SQLModel/Pydantic en `src/models/` (sin eliminar aún los antiguos) y añadir tests unitarios pequeños para instanciarlos.
2. DAO: Implementar versiones de DAO que usen los nuevos modelos, con validaciones y transacciones para operaciones multi-tabla (crear estudiante -> datos personales + estudiante + usuario).
3. Endpoints: Cambiar endpoints para utilizar nuevos esquemas y DAOs.
4. Migración de datos: elaborar scripts para migrar datos desde `ingles` hacia `proyectoIngles` (preservar relaciones). Hacer en staging primero.

Notas y riesgos
- Cambios en PK (int -> varchar) requieren decisiones de migración: mantener antiguo id como campo secundario o generar nuevos IDs.
- Migración de credenciales: si `Usuarios` centraliza auth, habrá que copiar email/password y asignar `id_usuario` a las entidades correspondientes.
- Validar triggers/procedures del nuevo esquema; pueden necesitar adaptación.

Siguiente paso propuesto
- ¿Quieres que genere los modelos nuevos en `src/models/` y los DAOs adaptados automáticamente ahora? Puedo:
  - Opción 1: generar nuevos modelos + DAOs en archivos separados (`models_new.py`, `dao_new.py`) y dejar los originales intactos (seguro, incremental).
  - Opción 2: refactor directo sobre los archivos existentes (riesgo mayor, pero limpia el repo).

Indica preferencia (1 ó 2).