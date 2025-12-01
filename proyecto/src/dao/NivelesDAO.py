from sqlmodel import Session
from models.UsuariosModel import Niveles

class NivelesDAO():
    def __init__(self, session: Session):
        self.session = session

    def listar_niveles(self):
        return self.session.query(Niveles).all()

    def agregar_nivel(self, nombre: str):
        nuevo = Niveles(Nivel=nombre)
        self.session.add(nuevo)
        self.session.commit()
        return nuevo
