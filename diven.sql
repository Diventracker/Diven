-- Eliminar todas las tablas si existen
DROP TABLE IF EXISTS detalle_servicio, detalle_venta, garantia_producto, garantia_servicio,
imagen_servicio, producto, proveedor, servicio_tecnico, usuario, venta, cliente;

-- Crear tablas desde cero

CREATE TABLE cliente (
  id_cliente INT(11) NOT NULL AUTO_INCREMENT,
  nombre_cliente VARCHAR(100) NOT NULL,
  numero_documento VARCHAR(20) NOT NULL UNIQUE,
  direccion_cliente VARCHAR(255) NOT NULL,
  telefono_cliente VARCHAR(20) NOT NULL,
  email_cliente VARCHAR(100) NOT NULL UNIQUE,
  tipo_documento VARCHAR(20) NOT NULL,
  fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_cliente)
);

CREATE TABLE usuario (
  id_usuario INT(11) NOT NULL AUTO_INCREMENT,
  nombre_usuario VARCHAR(100) NOT NULL,
  correo VARCHAR(100) NOT NULL UNIQUE,
  telefono_usuario VARCHAR(20) NOT NULL,
  clave VARCHAR(255) NOT NULL,
  rol VARCHAR(50) NOT NULL,
  token_recuperacion VARCHAR(6) DEFAULT NULL,
  token_expiracion DATETIME DEFAULT NULL,
  PRIMARY KEY (id_usuario)
);

CREATE TABLE proveedor (
  id_proveedor INT(11) NOT NULL AUTO_INCREMENT,
  nit VARCHAR(20) NOT NULL UNIQUE,
  nombre_proveedor VARCHAR(100) NOT NULL,
  representante_ventas VARCHAR(100) NOT NULL,
  telefono_representante_ventas VARCHAR(20) NOT NULL,
  direccion_proveedor VARCHAR(255) NOT NULL,
  fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_proveedor)
);

CREATE TABLE producto (
  id_producto INT(11) NOT NULL AUTO_INCREMENT,
  nombre_producto VARCHAR(100) NOT NULL,
  modelo VARCHAR(50) NOT NULL,
  descripcion TEXT NOT NULL,
  precio INT(10) NOT NULL,
  stock INT(11) NOT NULL DEFAULT 0,
  id_proveedor INT(11) NOT NULL,
  meses_garantia INT(11) DEFAULT NULL,
  fecha_compra TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  imagen VARCHAR(255) DEFAULT NULL,
  precio_venta INT(10) NOT NULL,
  PRIMARY KEY (id_producto),
  FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
);

CREATE TABLE servicio_tecnico (
  id_servicio INT(11) NOT NULL AUTO_INCREMENT,
  id_cliente INT(11) NOT NULL,
  id_usuario INT(11) NOT NULL,
  tipo_equipo VARCHAR(50) NOT NULL,
  modelo_equipo VARCHAR(50) NOT NULL,
  descripcion_problema TEXT NOT NULL,
  fecha_recepcion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_entrega DATE DEFAULT NULL,
  estado_servicio VARCHAR(50) NOT NULL DEFAULT 'En Progreso',
  meses_garantia INT(11) DEFAULT 0,
  tipo_servicio VARCHAR(50) NOT NULL,
  precio_servicio INT(10) NOT NULL,
  descripcion_trabajo TEXT DEFAULT NULL,
  PRIMARY KEY (id_servicio),
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
  FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE detalle_servicio (
  id_detalle INT(11) NOT NULL AUTO_INCREMENT,
  id_servicio INT(11) NOT NULL,
  id_usuario INT(11) DEFAULT NULL,
  valor_adicional INT(10) NOT NULL DEFAULT 0,
  motivo VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_detalle),
  FOREIGN KEY (id_servicio) REFERENCES servicio_tecnico(id_servicio) ON DELETE CASCADE,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE SET NULL
);

CREATE TABLE venta (
  id_venta INT(11) NOT NULL AUTO_INCREMENT,
  id_cliente INT(11) NOT NULL,
  id_usuario INT(11) NOT NULL,
  fecha_venta TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total_venta INT(10) NOT NULL,
  PRIMARY KEY (id_venta),
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
  FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE detalle_venta (
  id_detalle INT(11) NOT NULL AUTO_INCREMENT,
  id_venta INT(11) NOT NULL,
  id_producto INT(11) NOT NULL,
  cantidad INT(11) NOT NULL,
  precio_unitario INT(10) NOT NULL,
  PRIMARY KEY (id_detalle),
  FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
  FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

CREATE TABLE garantia_producto (
  id_garantia INT(11) NOT NULL AUTO_INCREMENT,
  id_producto INT(11) NOT NULL,
  id_venta INT(11) DEFAULT NULL,
  id_cliente INT(11) DEFAULT NULL,
  id_garantia_origen INT(11) DEFAULT NULL,
  fecha_inicio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_fin TIMESTAMP NOT NULL,
  origen_garantia ENUM('compra_proveedor','venta_cliente') NOT NULL,
  estado ENUM('activa','vencida','anulada','renovada') NOT NULL DEFAULT 'activa',
  PRIMARY KEY (id_garantia),
  FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
  FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
  FOREIGN KEY (id_garantia_origen) REFERENCES garantia_producto(id_garantia) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE garantia_servicio (
  id_garantia INT(11) NOT NULL AUTO_INCREMENT,
  id_servicio INT(11) NOT NULL,
  fecha_inicio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_fin TIMESTAMP NOT NULL,
  estado ENUM('activa','vencida','anulada') NOT NULL DEFAULT 'activa',
  PRIMARY KEY (id_garantia),
  FOREIGN KEY (id_servicio) REFERENCES servicio_tecnico(id_servicio)
);

CREATE TABLE imagen_servicio (
  id_imagen INT(11) NOT NULL AUTO_INCREMENT,
  id_servicio INT(11) NOT NULL,
  ruta_archivo VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_imagen),
  FOREIGN KEY (id_servicio) REFERENCES servicio_tecnico(id_servicio) ON DELETE CASCADE
);

INSERT INTO `usuario` (`id_usuario`, `nombre_usuario`, `correo`, `telefono_usuario`, `clave`, `rol`, `token_recuperacion`, `token_expiracion`) VALUES
(1, 'The Main', 'admin@tienda.com', '3102399888', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Administrador', NULL, NULL);