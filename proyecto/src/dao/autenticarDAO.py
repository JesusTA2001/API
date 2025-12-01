from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, status

class AutenticacionDAO:
    def __init__(self, session: Session):
        self.session = session

    def autenticar(self, email: str, password: str) -> dict:
        tablas = [
            {"nombre": "alumnos", "rol": "Alumno"},
            {"nombre": "profesores", "rol": "Docente"},
            {"nombre": "administrador", "rol": "Administrativo"}
        ]

        for tabla in tablas:
            sql = text(f"SELECT * FROM {tabla['nombre']} WHERE email = :email AND password = :password")
            resultado = self.session.execute(sql, {"email": email, "password": password}).first()
            if resultado:
                usuario = dict(resultado._mapping)
                return {"estatus": True, "usuario": usuario, "rol": tabla["rol"]}

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Basic"},
        )
