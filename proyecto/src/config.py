import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (desarrollo local)
load_dotenv()

# Configuración de base de datos
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://admin_ingles:Gui11ermo1@mysqlingles.mysql.database.azure.com/proyectoIngles'
)

# Configuración de seguridad
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'tu_clave_secreta_super_segura_cambiala_en_produccion'
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
