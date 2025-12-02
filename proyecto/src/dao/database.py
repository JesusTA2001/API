from sqlmodel import create_engine,Session
DATABASE_URL='mysql+pymysql://root:root@localhost/proyectoIngles'

engine=create_engine(DATABASE_URL)

class Conexion:
    def __init__(self):
        self.session=None
    def getSession(self):
        self.session=Session(engine)
        return self.session
    def cerrarSession(self):
        self.session.close()
