-- 1. Tabla de Catálogos: Tipos de Documento
CREATE TABLE tipos_documento (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- 2. Tabla de Usuarios (Funcionarios)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    codigo_empleado VARCHAR(20) NOT NULL UNIQUE,
    nombre_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE, 
    cargo VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla de Documentos (Inventario)
CREATE TABLE documentos (
    id SERIAL PRIMARY KEY,
    codigo_barras VARCHAR(50) NOT NULL UNIQUE,
    tipo_id INT NOT NULL REFERENCES tipos_documento(id),
    identificador_fisico VARCHAR(100) NOT NULL,
    ubicacion_fisica VARCHAR(50) NOT NULL,
    estado VARCHAR(20) DEFAULT 'DISPONIBLE' CHECK (estado IN ('DISPONIBLE', 'PRESTADO', 'MANTENIMIENTO', 'EXTRAVIADO')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabla de Préstamos
CREATE TABLE prestamos (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id),
    documento_id INT NOT NULL REFERENCES documentos(id),
    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_limite TIMESTAMP NOT NULL,
    fecha_devolucion TIMESTAMP NULL,
    observaciones TEXT,
    CONSTRAINT check_fechas CHECK (fecha_devolucion IS NULL OR fecha_devolucion >= fecha_prestamo)
);

-- 5. Índices de Rendimiento
CREATE INDEX idx_usuarios_codigo ON usuarios(codigo_empleado);
CREATE INDEX idx_documentos_barras ON documentos(codigo_barras);
CREATE INDEX idx_prestamos_activos ON prestamos(usuario_id) WHERE fecha_devolucion IS NULL;

-- 6. Vista de Auditoría
CREATE OR REPLACE VIEW vista_prestamos_activos AS
SELECT 
    p.id as prestamo_id,
    u.nombre_completo as funcionario,
    u.codigo_empleado,
    d.identificador_fisico as documento,
    d.codigo_barras,
    p.fecha_prestamo,
    p.fecha_limite
FROM prestamos p
JOIN usuarios u ON p.usuario_id = u.id
JOIN documentos d ON p.documento_id = d.id
WHERE p.fecha_devolucion IS NULL;

-- 7. Datos de Prueba Iniciales (Seed Data)
INSERT INTO tipos_documento (nombre) VALUES ('Nacimiento'), ('Matrimonio'), ('Defunción');

INSERT INTO usuarios (codigo_empleado, nombre_completo, cargo) 
VALUES 
('EMP001', 'Juan Pérez', 'Archivista Senior'),
('EMP002', 'Maria Lopez', 'Auxiliar Administrativo');

INSERT INTO documentos (codigo_barras, tipo_id, identificador_fisico, ubicacion_fisica) 
VALUES 
('LIB-NAC-1990-T1', 1, 'Libro Nacimientos 1990 Tomo 1', 'Pasillo A, Estante 2'),
('LIB-MAT-2005-T4', 2, 'Libro Matrimonios 2005 Tomo 4', 'Pasillo B, Estante 1');
