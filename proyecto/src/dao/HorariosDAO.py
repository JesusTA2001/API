from sqlmodel import Session
from models.UsuariosModel import Horario

class HorarioDAO():
    def __init__(self, session: Session):
        self.session = session

    def listar_horarios(self):
        return self.session.query(Horario).all()

    def agregar_horario(self, anio: str, dia: str, id_grupo: int, id_profesor: int, id_nivel: int, id_modalidad: int):
        nuevo = Horario(
            anio=anio,
            diaSemana=dia,
            id_Grupo=id_grupo,
            id_profesor=id_profesor,
            id_Nivel=id_nivel,
            id_Modalidad=id_modalidad
        )
        self.session.add(nuevo)
        self.session.commit()
        return nuevo
