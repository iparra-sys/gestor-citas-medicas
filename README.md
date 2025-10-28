# 🏥 Gestor de Citas Médicas

Aplicación web desarrollada con **Flask** y **MySQL** que permite registrar, editar, eliminar y consultar pacientes en un entorno médico.  
Su objetivo es brindar una interfaz sencilla y eficiente para la administración de citas y control básico de pacientes.

---

## 🚀 Características principales

✅ Registro de pacientes con validación de datos  
✅ Edición y eliminación de registros  
✅ Prevención de duplicados por documento  
✅ Integración con base de datos **MySQL**  
✅ Interfaz moderna con **Bootstrap** y alertas visuales  
✅ Gestión completa desde navegador local

---

## 🧠 Tecnologías utilizadas

- **Python 3**
- **Flask**
- **MySQL**
- **Bootstrap 5**
- **HTML5 / CSS3 / Jinja2**

---

## ⚙️ Instalación y ejecución

1. Clona este repositorio:
   ```bash
   git clone https://github.com/iparra-sys/gestor-citas-medicas.git
2. Ingresa al directorio:
cd gestor-citas-medicas
3.Crea un entorno virtual y actívalo:
python -m venv venv
venv\Scripts\activate
4.Instala las dependencias:
pip install -r requirements.txt
5.Configura tu base de datos MySQL y ajusta los datos de conexión en app.py:
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tu_contraseña'
app.config['MYSQL_DB'] = 'gestion_pacientes'
6.Ejecuta la aplicación:
python app.py
7.Abre tu navegador en:
http://127.0.0.1:5000

----


🧩 Estructura del proyecto

gestor-citas-medicas/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── /templates
│   ├── index.html
│   ├── pacientes.html
│   ├── editar_paciente.html
│   └── base.html
│
├── /static
│   ├── css/
│   └── js/
│
└── /instance

----

🌟 Capturas sugeridas

Agrega imágenes del sistema en acción:


























👩‍💻 Autora

Iveth Parra Herrera
🔗 LinkedIn

📧 Desarrolladora Python en formación | Enfocada en backend y soluciones web prácticas

💡 “El código es una herramienta para construir soluciones reales y dejar huella.”

✨ Proyecto desarrollado como parte del Portafolio 2025 - Iveth Parra Herrera ✨


🧾 Licencia

Este proyecto se publica con fines educativos y de portafolio.
Eres libre de revisarlo, mejorarlo o inspirarte en su estructura.


