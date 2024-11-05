import pyodbc

try:
    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=tu_servidor;DATABASE=tu_base_de_datos;UID=tu_usuario;PWD=tu_contraseña')
    print("Conectado exitosamente")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
