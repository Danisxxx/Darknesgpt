import mysql.connector

# Configuración de la base de datos
db_config = {
    "host": "mysql.railway.internal",
    "user": "root",
    "password": "JXyNzSbNJJHCbVNbcdvZWxyYwvlvFLwN",
    "database": "railway",
    "port": 3306
}

# Conexión a la base de datos y creación de la tabla
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Toolslist (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        command VARCHAR(255) NOT NULL,
        status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        owner VARCHAR(255) NOT NULL
    );
    """
    
    cursor.execute(create_table_query)
    conn.commit()
    print("Tabla 'Toolslist' creada con éxito.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
