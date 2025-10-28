from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = "clave_secreta_eps"

# ========================
# 🔧 CONFIGURACIÓN BD
# ========================
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "iveth_user"
app.config["MYSQL_PASSWORD"] = "Angel1308."
app.config["MYSQL_DB"] = "eps_db"
mysql = MySQL(app)

# ========================
# 🔐 LOGIN
# ========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario=%s AND password=%s", (usuario, password))
        user = cur.fetchone()
        print("DEBUG: user fetched from DB ->", user)
        cur.close()

        if user:
            session["usuario"] = usuario
            flash("✅ Bienvenido al panel de gestión", "success")
            return redirect(url_for("panel"))
        else:
            flash("❌ Credenciales incorrectas", "danger")
            return render_template("login.html")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("🔒 Sesión cerrada correctamente", "info")
    return redirect(url_for("login"))


# ========================
# 🏠 PANEL PRINCIPAL
# ========================
@app.route("/panel")
def panel():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("panel.html")


# ========================
# 👥 PACIENTES
# ========================

@app.route("/pacientes", methods=["GET", "POST"])
def pacientes():
    # 🧩 Crear cursor
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        documento = request.form["documento"].strip()
        telefono = request.form["telefono"].strip()
        email = request.form["email"].strip()
        fecha_nacimiento = request.form["fecha_nacimiento"].strip()

        # 🔍 Verificar si ya existe el documento
        cur.execute("SELECT * FROM pacientes WHERE documento = %s", (documento,))
        existente = cur.fetchone()

        if existente:
            flash("⚠️ Ya existe un paciente registrado con este documento.", "warning")
        else:
            # ✅ Insertar nuevo paciente
            cur.execute("""
                INSERT INTO pacientes (nombre, documento, telefono, email, fecha_nacimiento)
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre, documento, telefono, email, fecha_nacimiento))
            mysql.connection.commit()
            flash("✅ Paciente agregado correctamente.", "success")

    # 🩺 Listar pacientes (modo diccionario)
    cur.execute("SELECT * FROM pacientes ORDER BY id DESC")
    data = cur.fetchall()
    cur.close()

    return render_template("pacientes.html", pacientes=data)


@app.route("/pacientes/editar/<int:id>", methods=["GET", "POST"])
def editar_paciente(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == "POST":
        nombre = request.form["nombre"]
        documento = request.form["documento"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        fecha_nacimiento = request.form["fecha_nacimiento"]

        # 🔍 Verificar si el documento ya pertenece a otro paciente
        cur.execute("SELECT id FROM pacientes WHERE documento = %s AND id != %s", (documento, id))
        duplicado = cur.fetchone()

        if duplicado:
            flash("⚠️ No se puede actualizar: el documento ya está registrado en otro paciente.", "warning")
            return redirect(url_for("editar_paciente", id=id))

        # ✅ Actualizar datos del paciente
        cur.execute("""
            UPDATE pacientes
            SET nombre=%s, documento=%s, telefono=%s, email=%s, fecha_nacimiento=%s
            WHERE id=%s
        """, (nombre, documento, telefono, email, fecha_nacimiento, id))

        mysql.connection.commit()
        cur.close()
        flash("✅ Paciente actualizado correctamente", "success")
        return redirect(url_for("pacientes"))

    # GET → mostrar datos del paciente
    cur.execute("SELECT * FROM pacientes WHERE id = %s", (id,))
    paciente = cur.fetchone()
    cur.close()

    return render_template("editar_paciente.html", paciente=paciente)


@app.route("/actualizar_paciente/<int:id>", methods=["POST"])
def actualizar_paciente(id):
    nombre = request.form["nombre"]
    documento = request.form["documento"]
    telefono = request.form["telefono"]
    email = request.form["email"]
    fecha_nacimiento = request.form["fecha_nacimiento"]

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE pacientes
        SET nombre=%s, documento=%s, telefono=%s, email=%s, fecha_nacimiento=%s
        WHERE id=%s
    """, (nombre, documento, telefono, email, fecha_nacimiento, id))
    mysql.connection.commit()
    cur.close()

    flash("✅ Paciente actualizado correctamente", "success")
    return redirect(url_for("pacientes"))


@app.route('/eliminar_paciente/<int:id>')
def eliminar_paciente(id):
    cur = mysql.connection.cursor()

    # 🔍 Verificar si el paciente tiene citas registradas
    cur.execute("SELECT COUNT(*) FROM citas WHERE paciente_id = %s", (id,))
    count = cur.fetchone()[0]

    if count > 0:
        flash("⚠️ No puedes eliminar este paciente porque tiene citas registradas.", "danger")
        cur.close()
        return redirect(url_for('pacientes'))

    # 🗑️ Eliminar si no tiene citas asociadas
    cur.execute("DELETE FROM pacientes WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    flash("✅ Paciente eliminado correctamente.", "success")
    return redirect(url_for('pacientes'))


# ========================
# 📅 CITAS MÉDICAS
# ========================
@app.route("/citas")
def citas():
    if "usuario" not in session:
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT citas.id, 
                pacientes.nombre, 
                especialidades.nombre, 
                especialistas.nombre, 
                citas.fecha, 
                citas.hora, 
                citas.estado
        FROM citas
        JOIN pacientes ON citas.paciente_id = pacientes.id
        JOIN especialidades ON citas.especialidad_id = especialidades.id
        JOIN especialistas ON citas.especialista_id = especialistas.id
        ORDER BY citas.fecha ASC
    """)
    data = cur.fetchall()
    cur.close()

    citas_data = [
        {
            "id": row[0],
            "nombre": row[1],
            "especialidad": row[2],
            "especialista": row[3],
            "fecha": row[4],
            "hora": row[5],
            "estado": row[6]
        }
        for row in data
    ]

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre FROM especialidades")
    especialidades = cur.fetchall()

    cur.execute("SELECT id, nombre FROM especialistas")
    especialistas = cur.fetchall()
    cur.close()

    return render_template("citas.html", citas=citas_data, especialidades=especialidades, especialistas=especialistas)


@app.route("/guardar_cita", methods=["POST"])
def guardar_cita():
    nombre_paciente = request.form["nombre_paciente"]
    documento = request.form["documento"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]
    especialidad_id = request.form["especialidad_id"]
    especialista_id = request.form["especialista_id"]
    

    cur = mysql.connection.cursor()

    # Verificar si el paciente ya existe
    cur.execute("SELECT id FROM pacientes WHERE documento = %s", (documento,))
    paciente = cur.fetchone()

    if paciente:
        paciente_id = paciente[0]
    else:
        # Crear nuevo paciente con nombre y documento
        cur.execute(
            "INSERT INTO pacientes (nombre, documento) VALUES (%s, %s)",
            (nombre_paciente, documento),
        )
        mysql.connection.commit()
        paciente_id = cur.lastrowid

    # Insertar la cita
    cur.execute("""
        INSERT INTO citas (paciente_id, especialidad_id, especialista_id, fecha, hora, estado)
        VALUES (%s, %s, %s, %s, %s, 'Pendiente')
    """, (paciente_id, especialidad_id, especialista_id, fecha, hora))
    mysql.connection.commit()
    cur.close()

    flash("✅ Cita registrada correctamente", "success")
    return redirect(url_for("citas"))


@app.route("/citas/editar/<int:id>", methods=["GET", "POST"])
def editar_cita(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == "POST":
        paciente = request.form["paciente"].strip()
        documento = request.form["documento"].strip()
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        especialidad_id = request.form["especialidad_id"]
        especialista_id = request.form["especialista_id"]
        estado = request.form["estado"]

        # 🔍 Verificar si el paciente ya existe
        cur.execute("SELECT id FROM pacientes WHERE documento = %s", (documento,))
        paciente_existente = cur.fetchone()

        if paciente_existente:
            # Si existe, usar su ID (sin crear duplicado)
            paciente_id = paciente_existente["id"]

            # Actualizar nombre si cambió
            cur.execute("""
                UPDATE pacientes SET nombre = %s
                WHERE id = %s
            """, (paciente, paciente_id))
        else:
            # Crear nuevo paciente si no existe
            cur.execute("""
                INSERT INTO pacientes (nombre, documento)
                VALUES (%s, %s)
            """, (paciente, documento))
            mysql.connection.commit()
            paciente_id = cur.lastrowid

        # 🔧 Actualizar la cita
        cur.execute("""
            UPDATE citas
            SET paciente_id=%s,
                fecha=%s,
                hora=%s,
                especialidad_id=%s,
                especialista_id=%s,
                estado=%s
            WHERE id=%s
        """, (paciente_id, fecha, hora, especialidad_id, especialista_id, estado, id))

        mysql.connection.commit()
        cur.close()
        flash("✅ Cita actualizada correctamente", "success")
        return redirect(url_for("citas"))

    # 🧠 GET → obtener datos de la cita a editar
    cur.execute("""
        SELECT c.id, p.nombre AS paciente, p.documento, c.fecha, c.hora, c.estado,
               e.id AS especialidad_id, e.nombre AS especialidad,
               es.id AS especialista_id, es.nombre AS especialista
        FROM citas c
        JOIN pacientes p ON c.paciente_id = p.id
        LEFT JOIN especialidades e ON c.especialidad_id = e.id
        LEFT JOIN especialistas es ON c.especialista_id = es.id
        WHERE c.id = %s
    """, (id,))
    cita = cur.fetchone()

    # 📋 Listas para selects
    cur.execute("SELECT id, nombre FROM especialidades")
    especialidades = cur.fetchall()
    cur.execute("SELECT id, nombre FROM especialistas")
    especialistas = cur.fetchall()
    cur.close()

    if not cita:
        flash("⚠️ No se encontró la cita seleccionada.", "warning")
        return redirect(url_for("citas"))

    return render_template(
        "editar_cita.html",
        cita=cita,
        especialidades=especialidades,
        especialistas=especialistas
    )

@app.route("/citas/eliminar/<int:id>")
def eliminar_cita(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM citas WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    flash("🗑️ Cita eliminada correctamente", "warning")
    return redirect(url_for("citas"))


# ========================
# 🚀 EJECUCIÓN
# ========================
if __name__ == "__main__":
    app.run(debug=True)
