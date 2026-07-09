from flask import Flask, request, jsonify
from database import get_connection

app = Flask(__name__)

# Función utilitaria para convertir las tuplas de la base de datos en diccionarios (clave-valor)
# Esto es necesario para que Flask pueda transformarlo a JSON correctamente.
def dict_artista(row):
    if not row: return None
    return {
        "id_artista": row[0],
        "nombre_artistico": row[1],
        "nombre_real": row[2],
        "pais": row[3],
        "fecha_nacimiento": str(row[4]), # Convertido a string por si es un objeto date de Python
        "genero_musical": row[5],
        "biografia": row[6]
    }

def dict_usuario(row):
    if not row: return None
    return {
        "id_usuario": row[0],
        "nombre": row[1],
        "apellido": row[2],
        "nombre_usuario": row[3],
        "correo": row[4],
        # Nota: Por seguridad, normalmente no se debería retornar la contraseña
        "contrasena": row[5] 
    }

# --- RUTAS DE ARTISTAS ---

@app.route("/artistas", methods=["GET"]) # Cambiado de "/" a "/artistas" para mayor claridad de API
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artista ORDER BY id_artista")
    artistas_raw = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Convertimos cada fila en un diccionario
    artistas = [dict_artista(row) for row in artistas_raw]
    return jsonify(artistas), 200

@app.route("/guardar_artista", methods=["POST"])
def guardar_artista():
    # En una API JSON, los datos suelen venir en request.json en vez de request.form
    data = request.json 
    
    nombre_artistico = data.get("nombre_artistico")
    nombre_real = data.get("nombre_real")
    pais = data.get("pais")
    fecha_nacimiento = data.get("fecha_nacimiento")
    genero_musical = data.get("genero_musical")
    biografia = data.get("biografia")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO artista
        (nombre_artistico,nombre_real,pais,fecha_nacimiento,genero_musical,biografia)
        VALUES(%s,%s,%s,%s,%s,%s)
    """, (nombre_artistico, nombre_real, pais, fecha_nacimiento, genero_musical, biografia))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Artista guardado con éxito"}), 201

@app.route("/editar_artista/<int:id>", methods=["GET"])
def editar_artista(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artista WHERE id_artista=%s", (id,))
    artista_raw = cursor.fetchone()
    cursor.close()
    conn.close()

    if artista_raw:
        return jsonify(dict_artista(artista_raw)), 200
    return jsonify({"error": "Artista no encontrado"}), 404

@app.route("/actualizar_artista/<int:id>", methods=["PUT"]) # Cambiado a PUT, estándar para actualizar
def actualizar_artista(id):
    data = request.json

    nombre_artistico = data.get("nombre_artistico")
    nombre_real = data.get("nombre_real")
    pais = data.get("pais")
    fecha_nacimiento = data.get("fecha_nacimiento")
    genero_musical = data.get("genero_musical")
    biografia = data.get("biografia")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE artista
        SET nombre_artistico=%s, nombre_real=%s, pais=%s, fecha_nacimiento=%s, genero_musical=%s, biografia=%s
        WHERE id_artista=%s
    """, (nombre_artistico, nombre_real, pais, fecha_nacimiento, genero_musical, biografia, id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Artista actualizado con éxito"}), 200

@app.route("/eliminar_artista/<int:id>", methods=["DELETE"]) # Cambiado a DELETE
def eliminar_artista(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM artista WHERE id_artista=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Artista eliminado con éxito"}), 200


# --- RUTAS DE USUARIOS ---
@app.route("/guardar_usuario", methods=["POST"])
def guardar_usuario():
    data = request.json

    nombre = data.get("nombre")
    apellido = data.get("apellido")
    nombre_usuario = data.get("nombre_usuario")
    correo = data.get("correo")
    contrasena = data.get("contrasena")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios
        (nombre,apellido,nombre_usuario,correo,contrasena)
        VALUES(%s,%s,%s,%s,%s)
    """, (nombre, apellido, nombre_usuario, correo, contrasena))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Usuario guardado con éxito"}), 201


if __name__ == "__main__":
    app.run(debug=True)