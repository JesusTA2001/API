from sqlmodel import Session
from models.UsuariosModel import Modalidad

class ModalidadDAO():
    def __init__(self, session: Session):
        self.session = session

    def listar_modalidades(self):
        return self.session.query(Modalidad).all()

    def agregar_modalidad(self, nombre: str):
        nueva = Modalidad(Modalidad=nombre)
        self.session.add(nueva)
        self.session.commit()
        return nueva
