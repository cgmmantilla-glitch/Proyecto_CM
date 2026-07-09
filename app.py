from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)

@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artista ORDER BY id_artista")
    artistas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", artistas=artistas)

@app.route("/guardar_artista", methods=["POST"])
def guardar_artista():
    nombre_artistico = request.form["nombre_artistico"]
    nombre_real = request.form["nombre_real"]
    pais = request.form["pais"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    genero_musical = request.form["genero_musical"]
    biografia = request.form["biografia"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO artista
        (nombre_artistico,nombre_real,pais,fecha_nacimiento,genero_musical,biografia)
        VALUES(%s,%s,%s,%s,%s,%s)
    """,(nombre_artistico,nombre_real,pais,fecha_nacimiento,genero_musical,biografia))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/editar_artista/<int:id>")
def editar_artista(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM artista WHERE id_artista=%s",(id,))
    artista = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("editar_artista.html", artista=artista)

@app.route("/actualizar_artista/<int:id>", methods=["POST"])
def actualizar_artista(id):

    nombre_artistico=request.form["nombre_artistico"]
    nombre_real=request.form["nombre_real"]
    pais=request.form["pais"]
    fecha_nacimiento=request.form["fecha_nacimiento"]
    genero_musical=request.form["genero_musical"]
    biografia=request.form["biografia"]

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
        UPDATE artista
        SET nombre_artistico=%s, nombre_real=%s, pais=%s, fecha_nacimiento=%s, genero_musical=%s, biografia=%s
        WHERE id_artista=%s
    """,(nombre_artistico,nombre_real,pais,fecha_nacimiento,genero_musical,biografia,id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/eliminar_artista/<int:id>")
def eliminar_artista(id):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute(
        "DELETE FROM artista WHERE id_artista=%s",
        (id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/")

#---USUARIOS

@app.route("/usuarios")
def usuarios():

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
        SELECT * FROM usuarios ORDER BY id_usuario
    """)

    usuarios=cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/guardar_usuario", methods=["POST"])
def guardar_usuario():

    nombre=request.form["nombre"]
    apellido=request.form["apellido"]
    nombre_usuario=request.form["nombre_usuario"]
    correo=request.form["correo"]
    contrasena=request.form["contrasena"]

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios
        (nombre,apellido,nombre_usuario,correo,contrasena)
        VALUES(%s,%s,%s,%s,%s)
    """,(nombre,apellido,nombre_usuario,correo,contrasena))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/usuarios")



if __name__ == "__main__":
    app.run(debug=True)