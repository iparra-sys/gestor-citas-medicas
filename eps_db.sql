-- Crear base de datos
/*CREATE DATABASE IF NOT EXISTS eps_db;
USE eps_db;*/

-- =======================
-- 🧍 Tabla de Pacientes
-- =======================
/*CREATE TABLE IF NOT EXISTS pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    fecha_nacimiento DATE
);

-- =======================
-- 📅 Tabla de Citas
-- =======================
CREATE TABLE IF NOT EXISTS citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    especialista VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado ENUM('Pendiente','Confirmada','Cancelada') DEFAULT 'Pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

-- =======================
-- 👤 Tabla de Usuarios (para login)
-- =======================
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Insertar usuario por defecto
INSERT INTO usuarios (usuario, password)
VALUES ('admin', '1234');
*/
-- =======================
-- Datos de ejemplo
-- =======================
/*INSERT INTO pacientes (nombre, documento, fecha_nacimiento, telefono, email) VALUES
('Juan Pérez', '12345678', '1985-04-12', '3101234567', 'juan.perez@email.com'),
('María Gómez', '87654321', '1990-08-25', '3107654321', 'maria.gomez@email.com'),
('Carlos Rodríguez', '11223344', '1975-12-05', '3119876543', 'carlos.rodriguez@email.com'),
('Laura Martínez', '44332211', '2000-03-18', '3124567890', 'laura.martinez@email.com');

INSERT INTO citas (paciente_id, especialista, fecha, hora, estado) VALUES
(1, 'Dr. Juan Torres', '2025-10-25', '09:00', 'Pendiente'),
(2, 'Dra. Ana López', '2025-10-26', '10:30', 'Pendiente'),
(3, 'Dr. Luis Fernández', '2025-10-27', '14:00', 'Confirmada'),
(4, 'Dra. Carmen Ruiz', '2025-10-28', '16:15', 'Pendiente'),
(1, 'Dra. Ana López', '2025-10-29', '11:00', 'Pendiente');
*/
/*ALTER TABLE citas ADD COLUMN especialidad VARCHAR(100);*/
/*CREATE TABLE especialidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);*/

/*INSERT INTO especialidades (nombre) VALUES 
('Medicina General'),
('Pediatría'),
('Odontología'),
('Cardiología'),
('Oncología'),
('Nutrición'),
('Psicología'),
('Dermatología');*/

/*CREATE TABLE especialistas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad_id INT,
    FOREIGN KEY (especialidad_id) REFERENCES especialidades(id)
);*/
/*INSERT INTO especialistas (nombre, especialidad_id) VALUES 
('Dr. Luis Fernández', 1), 
('Dra. Carmen Ruiz', 2), 
('Dr. Felipe Rojas', 3),
('Dra. Melissa Pantoja', 4),
('Dr. Alejandro Salim', 5),
('Dra. Vanessa Pedraza', 6),
('Dra. Paula Merlano', 7),
('Dr. Sebastian Forero', 8);*/
/*ALTER TABLE citas
ADD COLUMN especialidad_id INT AFTER paciente_id,
ADD COLUMN especialista_id INT AFTER especialidad_id;*/
/*ALTER TABLE citas
ADD CONSTRAINT fk_especialidad FOREIGN KEY (especialidad_id) REFERENCES especialidades(id),
ADD CONSTRAINT fk_especialista FOREIGN KEY (especialista_id) REFERENCES especialistas(id);
*/
/*DESCRIBE citas;*/
/*ALTER TABLE citas DROP COLUMN especialista;*/
/*SHOW CREATE TABLE citas;*/
/*ALTER TABLE citas DROP COLUMN especialidad;*/

SHOW INDEXES FROM pacientes;













