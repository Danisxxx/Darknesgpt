import pymysql

db_config = {
    "host": "mysql.railway.internal",
    "user": "root",
    "password": "JXyNzSbNJJHCbVNbcdvZWxyYwvlvFLwN",
    "database": "railway",
    "port": 3306
}

def create_table():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Command (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            command VARCHAR(255) NOT NULL,
            status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
            reason TEXT DEFAULT 'No especificada',
            date DATETIME DEFAULT NULL,
            owner VARCHAR(255) NOT NULL
        );
        """
        
        cursor.execute(create_table_query)
        conn.commit()
        
        print("Tabla 'Command' creada correctamente.")
    
    except pymysql.MySQLError as err:
        print(f"Error al crear la tabla: {err}")
    
    finally:
        if conn.open:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_table()
