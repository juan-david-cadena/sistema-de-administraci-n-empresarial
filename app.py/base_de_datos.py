import psycopg2

def conectar():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="sistema administrativo",
            user="postgres",
            password="123456"
        )
        print("conexión exitosa a la base de datos")
        return conexion
    except Exception as e:
        print(f"error al conectar a la base de datos:")

if __name__ == "__main__":
    conectar()