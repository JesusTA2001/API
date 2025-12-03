from sqlmodel import create_engine, Session
from src.config import DATABASE_URL

# Configuración SSL para Azure MySQL
connect_args = {
    "ssl": {
        "ssl_mode": "required"
    }
}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

class Conexion:
    def __init__(self):
        self.session=None
    def getSession(self):
        self.session=Session(engine)
        return self.session
    def cerrarSession(self):
        self.session.close()
