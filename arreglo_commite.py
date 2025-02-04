import os
import sys
import pandas as pd
from django.core.wsgi import get_wsgi_application

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pryiberoamericano.settings')
application = get_wsgi_application()

# Importar modelo
from landing.models import CommitteeMember, CommitteeCategory

# Ruta del archivo Excel (cámbiala según sea necesario)
EXCEL_FILE_PATH = "ruta/del/archivo.xlsx"

def importar_committee_members():
    try:
        # Leer el archivo Excel (ignorar la primera fila)
        df = pd.read_excel(EXCEL_FILE_PATH, skiprows=1, usecols=[0, 1, 2], names=['nombre', 'comite', 'cargo'])

        for _, row in df.iterrows():
            nombre = row['nombre']
            comite = row['comite']
            cargo = row['cargo']
            orden = row['orden']
            comite = CommitteeCategory.objects.get_or_create(nombre=comite)
            # Crear o actualizar el registro en la base de datos
            CommitteeMember.objects.update_or_create(
                nombre=nombre,  # Clave para buscar si ya existe
                category=comite,  # Comité
                defaults={'category': comite, 'rol': cargo}
            )

        print("Importación completada correctamente.")

    except Exception as ex:
        linea_ = 'Error en la línea {}'.format(sys.exc_info()[-1].tb_lineno)
        print(f"{linea_}: {ex}")

# Ejecutar la importación
importar_committee_members()