from sqlmodel import Session
from models.UsuariosModel import Carrera

class CarreraDAO():
    def __init__(self, session: Session):
        self.session = session

    def listar_carrera(self):
        return self.session.query(Carrera).all()

    def agregar_carrera(self, nombre: str):
        nueva = Carrera(Carrera=nombre)
        self.session.add(nueva)
        self.session.commit()
        return nueva
