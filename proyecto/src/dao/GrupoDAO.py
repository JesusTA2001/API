from sqlmodel import Session
from models.UsuariosModel import Grupo

class GrupoDAO():
    def __init__(self, session: Session):
        self.session = session

    def listar_grupos(self):
        return self.session.query(Grupo).all()

    def agregar_grupo(self, nombre: str):
        nuevo = Grupo(Grupo=nombre)
        self.session.add(nuevo)
        self.session.commit()
        return nuevo
