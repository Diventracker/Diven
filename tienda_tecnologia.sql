-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 05-06-2025 a las 07:19:05
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tienda_tecnologia`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `id_cliente` int(11) NOT NULL,
  `nombre_cliente` varchar(100) NOT NULL,
  `cedula` varchar(20) NOT NULL,
  `direccion_cliente` varchar(255) NOT NULL,
  `telefono_cliente` varchar(20) NOT NULL,
  `email_cliente` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `nombre_cliente`, `cedula`, `direccion_cliente`, `telefono_cliente`, `email_cliente`) VALUES
(5, 'Carlos Sánchez', '1034567890', 'Avenida 6 #30-40', '3003456789', 'carlos.sanchez@email.com'),
(6, 'Ana Gómez', '1045678901', 'Avenida 9 #22-45', '3104567890', 'ana.gomez@email.com'),
(7, 'Pedro Martínez', '1056789012', 'Calle 5 #10-15', '3205678901', 'pedro.martinez@email.com'),
(8, 'Laura Fernández', '1067890123', 'Carrera 20 #50-60', '3306789012', 'laura.fernandez@email.com'),
(9, 'Luis Torres', '1078901234', 'Calle 8 #15-25', '3407890123', 'luis.torres@email.com'),
(10, 'Beatriz López', '1089012345', 'Avenida 11 #35-45', '3508901234', 'beatriz.lopez@email.com'),
(11, 'Raúl González', '1090123456', 'Carrera 14 #60-70', '3609012345', 'raul.gonzalez@email.com'),
(12, 'Isabel Pérez', '1101234567', 'Calle 3 #20-30', '3700123456', 'isabel.perez@email.com'),
(13, 'Eduardo Ramírez', '1112345678', 'Avenida 4 #25-35', '3801234567', 'eduardo.ramirez@email.com'),
(14, 'Carmen Díaz', '1123456789', 'Calle 12 #40-50', '3902345678', 'carmen.diaz@email.com'),
(15, 'José García', '1134567890', 'Carrera 7 #18-28', '4003456789', 'jose.garcia@email.com'),
(16, 'Patricia Martínez', '1145678901', 'Calle 4 #10-20', '4104567890', 'patricia.martinez@email.com'),
(17, 'Fernando López', '1156789012', 'Avenida 15 #55-65', '4205678901', 'fernando.lopez@email.com'),
(18, 'Sofía Martínez', '1167890123', 'Calle 6 #30-40', '4306789012', 'sofia.martinez@email.com'),
(19, 'Miguel Ángel García', '1178901234', 'Avenida 2 #10-20', '4407890123', 'miguel.garcia@email.com'),
(20, 'Rosa Hernández', '1189012345', 'Calle 10 #50-60', '4508901234', 'rosa.hernandez@email.com'),
(21, 'Antonio Jiménez', '1190123456', 'Carrera 18 #15-25', '4609012345', 'antonio.jimenez@email.com'),
(22, 'Marta Pérez', '1201234567', 'Calle 20 #30-40', '4700123456', 'marta.perez@email.com'),
(23, 'Javier Sánchez', '1212345678', 'Avenida 8 #22-32', '4801234567', 'javier.sanchez@email.com'),
(24, 'Julia Díaz', '1223456789', 'Calle 25 #10-20', '4902345678', 'julia.diaz@email.com'),
(25, 'Ricardo López', '1234567890', 'Carrera 12 #40-50', '5003456789', 'ricardo.lopez@email.com'),
(26, 'Nuria González', '1245678901', 'Calle 17 #60-70', '5104567890', 'nuria.gonzalez@email.com'),
(27, 'Fernando Pérez', '1256789012', 'Avenida 14 #35-45', '5205678901', 'fernando.perez@email.com'),
(28, 'Patricia Rodríguez', '1267890123', 'Calle 13 #25-35', '5306789012', 'patricia.rodriguez@email.com'),
(29, 'Roberto Torres', '1278901234', 'Avenida 18 #45-55', '5407890123', 'roberto.torres@email.com'),
(45, 'Zoeeee Guadalupe', '129012345', 'Diagonal 78', '3222323232', 'andw@gmail.com'),
(52, 'Harol', '123222323', 'diagonal 56', '3224354565', 'harol@gmail.com'),
(53, 'Joaquin Cañon', '1012443507', 'tv 77 i # 65 j 16 sur ', '3053970242', 'Danielcf97@hotmail.com'),
(55, 'Cliente Mostrador ', '00000000', 'Direcion General', '0000000000', 'Cliente@cliente.com'),
(56, 'Mario', '1548652458', 'tv 8 cll 123 x2 ', '3122015614', 'mariio@cliente.com'),
(67, 'Carlos', '6465645', 'Cra 90 A No 45 A 05 Sur ', '3223295822', 'carlos74937@gmail.com'),
(68, 'Marcos', '3242342342', 'cra 90798', '3213123123', 'marcosq@gmail.com'),
(83, 'MArcos', '3242342545', 'cra 98798689', '3123123123', 'marcosq22@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `id_detalle` int(11) NOT NULL,
  `id_venta` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_venta`
--

INSERT INTO `detalle_venta` (`id_detalle`, `id_venta`, `id_producto`, `cantidad`, `precio_unitario`) VALUES
(1, 1, 4, 1, 10000),
(2, 2, 4, 30, 10000),
(3, 3, 5, 1, 180000),
(4, 4, 5, 5, 180000),
(5, 5, 1, 1, 40000),
(6, 6, 9, 1, 40000),
(7, 7, 4, 1, 10000),
(8, 8, 18, 1, 43000),
(9, 9, 2, 1, 50000),
(10, 9, 8, 1, 1400000),
(11, 10, 14, 1, 49000),
(12, 11, 5, 1, 180000),
(13, 11, 8, 1, 1400000),
(14, 12, 5, 1, 180000),
(15, 13, 8, 1, 1400000),
(16, 14, 1, 1, 40000),
(17, 15, 5, 1, 180000),
(18, 16, 2, 2, 50000),
(19, 16, 10, 1, 45000),
(20, 16, 12, 3, 47000),
(21, 16, 14, 3, 49000),
(22, 16, 16, 2, 37000),
(23, 17, 1, 1, 40000),
(24, 17, 2, 1, 50000),
(25, 17, 5, 1, 180000),
(26, 18, 1, 1, 40000),
(27, 19, 1, 1, 40000),
(28, 20, 9, 1, 40000),
(29, 20, 10, 1, 45000),
(30, 20, 11, 1, 42000),
(31, 21, 2, 1, 50000),
(32, 21, 5, 1, 180000),
(33, 21, 10, 1, 45000),
(34, 22, 1, 1, 40000),
(35, 22, 5, 1, 180000),
(36, 25, 1, 3, 40000),
(37, 26, 1, 1, 40000),
(38, 26, 5, 2, 180000),
(39, 26, 17, 3, 39000),
(40, 27, 17, 3, 39000),
(41, 27, 13, 3, 42000),
(42, 28, 13, 1, 42000),
(43, 29, 11, 3, 42000),
(44, 29, 14, 3, 49000),
(45, 30, 10, 4, 45000),
(46, 30, 11, 1, 42000),
(47, 31, 12, 1, 47000),
(48, 31, 13, 1, 42000),
(49, 32, 17, 5, 39000),
(50, 33, 17, 2, 39000),
(51, 33, 9, 18, 40000),
(52, 33, 5, 18, 180000),
(53, 34, 2, 14, 50000),
(54, 34, 1, 11, 40000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `garantia_producto`
--

CREATE TABLE `garantia_producto` (
  `id_garantia` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `origen_garantia` enum('compra_proveedor','venta_cliente') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `garantia_servicio`
--

CREATE TABLE `garantia_servicio` (
  `id_garantia` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `garantia_servicio`
--

INSERT INTO `garantia_servicio` (`id_garantia`, `id_servicio`, `fecha_inicio`, `fecha_fin`) VALUES
(3, 22, '2025-05-17', '2025-07-17'),
(4, 23, '2025-05-19', '2025-08-19'),
(5, 24, '2025-05-18', '2025-07-18'),
(6, 25, '2025-05-17', '2025-10-17'),
(7, 26, '2025-06-02', '2025-09-02'),
(8, 27, '2025-05-31', '2025-06-30'),
(9, 28, '2025-05-28', '2025-10-28'),
(10, 38, '2025-04-17', '2025-04-17'),
(11, 39, '2025-05-17', '2025-07-17'),
(12, 40, '2025-05-19', '2025-08-19'),
(13, 41, '2025-05-18', '2025-07-18'),
(14, 42, '2025-05-17', '2025-10-17'),
(15, 43, '2025-06-02', '2025-09-02'),
(16, 44, '2025-05-31', '2025-06-30'),
(17, 45, '2025-05-28', '2025-10-28'),
(18, 46, '2025-05-05', '2025-07-05'),
(19, 47, '2025-05-06', '2025-06-06'),
(20, 48, '2025-05-07', '2025-05-07'),
(21, 49, '2025-05-08', '2025-08-08'),
(22, 50, '2025-05-10', '2025-06-10'),
(23, 51, '2025-05-09', '2025-07-09'),
(24, 52, '2025-05-11', '2025-05-11'),
(25, 53, '2025-05-13', '2025-09-13'),
(26, 54, '2025-05-14', '2025-08-14'),
(27, 55, '2025-05-15', '2025-06-15'),
(28, 56, '2025-05-16', '2025-07-16'),
(29, 57, '2025-05-17', '2025-10-17'),
(30, 58, '2025-05-18', '2025-05-18'),
(31, 59, '2025-05-19', '2025-07-19'),
(32, 60, '2025-05-20', '2025-08-20'),
(33, 61, '2025-06-03', '2025-06-03');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id_producto` int(11) NOT NULL,
  `nombre_producto` varchar(100) NOT NULL,
  `modelo` varchar(50) NOT NULL,
  `descripcion` text NOT NULL,
  `precio` int(10) NOT NULL,
  `stock` int(11) NOT NULL,
  `id_proveedor` int(11) NOT NULL,
  `meses_garantia` int(11) DEFAULT NULL,
  `fecha_compra` timestamp NOT NULL DEFAULT current_timestamp(),
  `precio_venta` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id_producto`, `nombre_producto`, `modelo`, `descripcion`, `precio`, `stock`, `id_proveedor`, `meses_garantia`, `fecha_compra`, `precio_venta`) VALUES
(1, 'Laptop Gamer', 'ROG Strix', 'Laptop de alto rendimiento para gaming', 4500000, 0, 1, 10, '2024-01-01 05:00:00', 40000),
(2, 'Laptop Gamer', 'ROG Strix', 'Laptop de alto rendimiento para gaming', 4400000, 0, 2, 20, '2024-02-01 05:00:00', 50000),
(4, 'Usb Kingston', '2TB', '2 terabytes de almacenamiento', 5000, 11, 2, 20, '2025-04-11 05:00:00', 10000),
(5, 'Tecladinho', 'K552', 'White', 100000, 15, 7, 20, '2025-04-04 05:00:00', 180000),
(8, 'Computador', 'paser76', 'Amd, 16gb ram', 1000000, 11, 1, 20, '2025-04-07 05:00:00', 1400000),
(9, 'Cartucho Negro 664', '664', 'Tinta negra original HP', 25000, 11, 7, 20250501, '2025-05-01 05:00:00', 40000),
(10, 'Cartucho Color 664', '664 Color', 'Tinta color original HP', 28000, 19, 7, 20, '2025-05-01 05:00:00', 45000),
(11, 'Cartucho Negro 21', '21', 'Cartucho tinta negra HP 21', 27000, 21, 7, 20, '2025-05-02 05:00:00', 42000),
(12, 'Cartucho Color 22', '22', 'Cartucho tinta color HP 22', 30000, 10, 7, 20, '2025-05-02 05:00:00', 47000),
(13, 'Cartucho PG-145 Negro', 'PG-145', 'Tinta negra para Canon Pixma', 26000, 13, 7, 20, '2025-05-03 05:00:00', 42000),
(14, 'Cartucho CL-146 Color', 'CL-146', 'Tinta color Canon original', 32000, 9, 7, 20, '2025-05-03 05:00:00', 49000),
(16, 'Cartucho T664 Color', 'T664 Color', 'Botella tinta color Epson EcoTank', 20000, 20, 2, 20, '2025-05-04 05:00:00', 37000),
(17, 'Cartucho LC103BK', 'LC103BK', 'Tinta negra original Brother', 23000, 1, 1, 20250505, '2025-05-05 05:00:00', 39000),
(18, 'Cartucho LC103CL', 'LC103CL', 'Tinta color original Brother', 26000, 10, 1, 20, '2025-05-05 05:00:00', 43000),
(20, 'Tarjetas Diitales', 'transmi', 'trajetas xd', 6000, 2, 14, 0, '2025-06-05 04:43:37', 10000),
(21, 'Mouse Logitech', 'g879', 'Mouse negro y blanco xd', 50000, 7, 15, 0, '2025-06-05 05:06:32', 70000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `id_proveedor` int(11) NOT NULL,
  `nit` varchar(20) NOT NULL,
  `nombre_proveedor` varchar(100) NOT NULL,
  `representante_ventas` varchar(100) NOT NULL,
  `telefono_representante_ventas` varchar(20) NOT NULL,
  `direccion_proveedor` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedor`
--

INSERT INTO `proveedor` (`id_proveedor`, `nit`, `nombre_proveedor`, `representante_ventas`, `telefono_representante_ventas`, `direccion_proveedor`) VALUES
(1, '900123456', 'Proveedor Tech', 'Carlos López', '3112345678', 'Calle 123 #45-67, Ciudad'),
(2, '900654321', 'Electro S.A.', 'Ana Gómez', '3223456789', 'Avenida 78 #12-34, Ciudad'),
(7, '9001234561', 'Impresoras D', 'Carlos Quintero', '3223244343', 'cra 9789'),
(10, '7321879361', 'Memorias USb', 'Joseeee', '4223244434', 'cra 98-98'),
(12, '901234567', 'Soluciones Tech', 'Laura Martínez', '3101234567', 'Calle 45 #23-10, Bogotá'),
(13, '902345678', 'Insumos PC', 'Miguel Torres', '3139876543', 'Carrera 9 #12-45, Medellín'),
(14, '903456789', 'Componentes S.A.S.', 'Andrés Gutiérrez', '3147654321', 'Transversal 33 #56-78, Cali'),
(15, '904567890', 'Distribuciones Norte', 'Diana Ríos', '3112233445', 'Calle 12 #34-56, Bucaramanga'),
(16, '905678901', 'TecnoPartes', 'Juan Ruiz', '3123344556', 'Av. Simón Bolívar #78-90, Barranquilla'),
(17, '906789012', 'Electronix Plus', 'Patricia Peña', '3201239876', 'Cra 45A #67-89, Cartagena'),
(18, '907890123', 'Mayoristas Bogotá', 'Camilo Paredes', '3156677889', 'Calle 80 #45-67, Bogotá'),
(19, '908901234', 'Multiservicios Andes', 'Viviana Castro', '3167788990', 'Carrera 7 #98-76, Pasto'),
(20, '909012345', 'Repuestos Express', 'Luis Rodríguez', '3178899001', 'Av. El Dorado #10-50, Bogotá'),
(21, '910123456', 'Accesorios Tech', 'Natalia Velásquez', '3189900112', 'Cra 50 #60-30, Manizales'),
(22, '911234567', 'TecnoMundo Ltda.', 'Esteban Parra', '3111109876', 'Carrera 15 #45-89, Neiva'),
(23, '912345678', 'Suministros Globales', 'Carolina Méndez', '3122203344', 'Calle 100 #12-45, Bogotá'),
(24, '913456789', 'Distribuidora Omega', 'Ricardo Luna', '3133304455', 'Cra 18 #25-60, Medellín'),
(25, '914567890', 'Proveedora del Caribe', 'María Restrepo', '3144405566', 'Av. Circunvalar #89-20, Barranquilla'),
(26, '915678901', 'ElectroHogar', 'David Gómez', '3155506677', 'Calle 10 #34-90, Bucaramanga'),
(27, '916789012', 'Tech Parts Express', 'Daniela Vargas', '3166607788', 'Av. Roosevelt #56-78, Cali'),
(28, '917890123', 'Logística y Suministros SAS', 'Santiago Páez', '3177708899', 'Calle 72 #23-56, Cúcuta'),
(29, '918901234', 'Corporación Digital', 'Mónica Acosta', '3188809900', 'Cra 24 #70-80, Ibagué'),
(30, '919012345', 'Red Solutions', 'Felipe Hernández', '3199900111', 'Carrera 50 #10-45, Pereira'),
(31, '920123456', 'Zona Computadores', 'Sandra León', '3200011223', 'Calle 30 #40-50, Montería');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicio_tecnico`
--

CREATE TABLE `servicio_tecnico` (
  `id_servicio` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tipo_equipo` varchar(50) NOT NULL,
  `modelo_equipo` varchar(50) NOT NULL,
  `descripcion_problema` text NOT NULL,
  `fecha_recepcion` date NOT NULL,
  `fecha_entrega_estimada` date NOT NULL,
  `estado_servicio` varchar(50) NOT NULL,
  `mes_garantia` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicio_tecnico`
--

INSERT INTO `servicio_tecnico` (`id_servicio`, `id_cliente`, `id_usuario`, `tipo_equipo`, `modelo_equipo`, `descripcion_problema`, `fecha_recepcion`, `fecha_entrega_estimada`, `estado_servicio`, `mes_garantia`) VALUES
(10, 18, 1, 'sdasda', 'asus rog', 'se calienta mucho', '2025-04-01', '2025-04-17', 'Pendiente', 0),
(22, 45, 1, 'HP', 'Samsung', 'No prende', '2025-05-16', '2025-05-17', 'Finalizado', 2),
(23, 15, 1, 'Celular', 'S24', 'No tiene volumen', '2025-05-16', '2025-05-19', 'Finalizado', 3),
(24, 8, 1, 'Reloj de mano', 'reloj rojo', 'sin manilla', '2025-05-16', '2025-05-18', 'En Progreso', 2),
(25, 45, 1, 'PC', '2093', 'No prende', '2025-05-16', '2025-05-17', 'En Progreso', 5),
(26, 15, 1, 'lenovo', 'asus rog', 'no prende', '2025-05-26', '2025-06-02', 'En Progreso', 3),
(27, 15, 1, 'Impresora termica', 'samsung', 'no imprime', '2025-05-26', '2025-05-31', 'En Progreso', 1),
(28, 15, 1, 'Impresora de tinta', 'epson l3290', 'no imprime', '2025-05-26', '2025-05-28', 'En Progreso', 5),
(38, 18, 1, 'sdasda', 'asus rog', 'se calienta mucho', '2025-04-01', '2025-04-17', 'Pendiente', 0),
(39, 45, 1, 'HP', 'Samsung', 'No prende', '2025-05-16', '2025-05-17', 'Finalizado', 2),
(40, 15, 1, 'Celular', 'S24', 'No tiene volumen', '2025-05-16', '2025-05-19', 'Finalizado', 3),
(41, 8, 1, 'Reloj de mano', 'reloj rojo', 'sin manilla', '2025-05-16', '2025-05-18', 'En Progreso', 2),
(42, 45, 1, 'PC', '2093', 'No prende', '2025-05-16', '2025-05-17', 'En Progreso', 5),
(43, 15, 1, 'lenovo', 'asus rog', 'no prende', '2025-05-26', '2025-06-02', 'En Progreso', 3),
(44, 15, 1, 'Impresora termica', 'samsung', 'no imprime', '2025-05-26', '2025-05-31', 'En Progreso', 1),
(45, 15, 1, 'Impresora de tinta', 'epson l3290', 'no imprime', '2025-05-26', '2025-05-28', 'En Progreso', 5),
(46, 10, 1, 'Laptop', 'Dell XPS 13', 'Pantalla parpadea', '2025-05-01', '2025-05-05', 'Pendiente', 2),
(47, 12, 1, 'Tablet', 'iPad Pro', 'No carga', '2025-05-02', '2025-05-06', 'En Progreso', 1),
(48, 13, 1, 'Smartphone', 'iPhone 13', 'Batería se descarga rápido', '2025-05-03', '2025-05-07', 'Pendiente', 0),
(49, 9, 1, 'PC', 'Ryzen 7', 'No da video', '2025-05-04', '2025-05-08', 'Finalizado', 3),
(50, 20, 1, 'Impresora', 'Canon G3110', 'Manchas al imprimir', '2025-05-05', '2025-05-10', 'Finalizado', 1),
(51, 11, 1, 'Monitor', 'LG 24MK430H', 'No prende', '2025-05-06', '2025-05-09', 'En Progreso', 2),
(52, 22, 1, 'Celular', 'Motorola G60', 'No vibra', '2025-05-07', '2025-05-11', 'Pendiente', 0),
(53, 18, 1, 'Laptop', 'Acer Nitro 5', 'Teclado no funciona', '2025-05-08', '2025-05-13', 'En Progreso', 4),
(54, 14, 1, 'PC', 'Intel i5', 'Reinicios constantes', '2025-05-09', '2025-05-14', 'Finalizado', 3),
(55, 17, 1, 'Smartwatch', 'Huawei GT2', 'Pantalla congelada', '2025-05-10', '2025-05-15', 'Pendiente', 1),
(56, 21, 1, 'Router', 'TP-Link Archer C6', 'Sin señal WiFi', '2025-05-11', '2025-05-16', 'En Progreso', 2),
(57, 16, 1, 'Notebook', 'MacBook Air', 'Trackpad dañado', '2025-05-12', '2025-05-17', 'Finalizado', 5),
(58, 19, 1, 'Tablet', 'Samsung Tab A7', 'No se conecta a internet', '2025-05-13', '2025-05-18', 'Pendiente', 0),
(59, 15, 1, 'Celular', 'Redmi Note 12', 'Micrófono no sirve', '2025-05-14', '2025-05-19', 'Finalizado', 2),
(60, 23, 1, 'PC', 'HP Pavilion', 'Ventilador ruidoso', '2025-05-15', '2025-05-20', 'En Progreso', 3),
(61, 45, 1, 'Computador portatil', 'Acer', 'No enicendeeeee', '2025-06-02', '2025-06-03', 'En Progreso', 0);

--
-- Disparadores `servicio_tecnico`
--
DELIMITER $$
CREATE TRIGGER `crear_garantia_servicio` AFTER INSERT ON `servicio_tecnico` FOR EACH ROW BEGIN
    DECLARE fecha_inicio DATE;
    DECLARE fecha_fin DATE;

    SET fecha_inicio = NEW.fecha_entrega_estimada;
    SET fecha_fin = DATE_ADD(fecha_inicio, INTERVAL NEW.mes_garantia MONTH);

    INSERT INTO garantia_servicio (id_servicio, fecha_inicio, fecha_fin)
    VALUES (NEW.id_servicio, fecha_inicio, fecha_fin);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `nombre_usuario` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `telefono_usuario` varchar(20) NOT NULL,
  `clave` varchar(255) NOT NULL,
  `rol` varchar(50) NOT NULL,
  `token_recuperacion` varchar(6) DEFAULT NULL,
  `token_expiracion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `nombre_usuario`, `correo`, `telefono_usuario`, `clave`, `rol`, `token_recuperacion`, `token_expiracion`) VALUES
(1, 'The Main', 'admin@tienda.com', '3102399888', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Administrador', NULL, NULL),
(12, 'Carlos Gómez', 'carlos.gomez@tienda.com', '3101112233', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Vendedor', NULL, NULL),
(13, 'Laura Pérez', 'laura.perez@tienda.com', '3112223344', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Técnico', NULL, NULL),
(14, 'Andrés Rodríguez', 'andres.rod@tienda.com', '3123334455', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Vendedor', NULL, NULL),
(15, 'Sofía Martínez', 'sofia.martinez@tienda.com', '3134445566', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Técnico', NULL, NULL),
(16, 'Daniel Torres', 'daniel.torres@tienda.com', '3145556677', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Vendedor', NULL, NULL),
(17, 'Mariana Ruiz', 'mariana.ruiz@tienda.com', '3156667788', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Técnico', NULL, NULL),
(18, 'Camilo Vargas', 'camilo.vargas@tienda.com', '3167778899', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Vendedor', NULL, NULL),
(19, 'Valentina Acosta', 'valentina.acosta@tienda.com', '3178889900', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Técnico', NULL, NULL),
(20, 'Luis Fernández', 'luis.fernandez@tienda.com', '3189990011', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Vendedor', NULL, NULL),
(21, 'Natalia Ríos', 'natalia.rios@tienda.com', '3190001122', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Técnico', NULL, NULL),
(22, 'Julián Castro', 'julian.castro@tienda.com', '3201112233', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Vendedor', NULL, NULL),
(23, 'Isabela Romero', 'isabela.romero@tienda.com', '3212223344', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Técnico', NULL, NULL),
(24, 'Tomás Navarro', 'tomas.navarro@tienda.com', '3223334455', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Vendedor', NULL, NULL),
(25, 'Gabriela Pardo', 'gabriela.pardo@tienda.com', '3234445566', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Técnico', NULL, NULL),
(26, 'Sebastián León', 'sebastian.leon@tienda.com', '3245556677', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Vendedor', NULL, NULL),
(27, 'Emma Salazar', 'emma.salazar@tienda.com', '3256667788', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Técnico', NULL, NULL),
(28, 'Mateo Niño', 'mateo.nino@tienda.com', '3267778899', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Vendedor', NULL, NULL),
(29, 'Lucía Peña', 'lucia.pena@tienda.com', '3278889900', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Técnico', NULL, NULL),
(30, 'Simón Garzón', 'simon.garzon@tienda.com', '3289990011', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Vendedor', NULL, NULL),
(31, 'Daniela Mora', 'daniela.mora@tienda.com', '3290001122', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Técnico', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `venta`
--

CREATE TABLE `venta` (
  `id_venta` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha_venta` date NOT NULL,
  `total_venta` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `venta`
--

INSERT INTO `venta` (`id_venta`, `id_cliente`, `id_usuario`, `fecha_venta`, `total_venta`) VALUES
(1, 5, 1, '2025-05-27', 10000),
(2, 5, 1, '2025-05-27', 300000),
(3, 5, 1, '2025-05-27', 180000),
(4, 6, 1, '2025-05-27', 900000),
(5, 53, 1, '2025-05-28', 40000),
(6, 53, 1, '2025-05-28', 40000),
(7, 53, 1, '2025-05-28', 10000),
(8, 55, 1, '2025-05-28', 43000),
(9, 5, 1, '2025-05-28', 1450000),
(10, 14, 1, '2025-05-28', 49000),
(11, 55, 1, '2025-05-28', 1580000),
(12, 53, 1, '2025-05-29', 180000),
(13, 53, 1, '2025-05-29', 1400000),
(14, 55, 1, '2025-05-29', 40000),
(15, 55, 1, '2025-05-29', 180000),
(16, 53, 1, '2025-05-29', 507000),
(17, 53, 1, '2025-05-29', 270000),
(18, 53, 1, '2025-05-29', 40000),
(19, 53, 1, '2025-05-29', 40000),
(20, 53, 1, '2025-05-29', 127000),
(21, 55, 1, '2025-05-29', 275000),
(22, 55, 1, '2025-05-29', 220000),
(25, 55, 1, '2025-05-30', 120000),
(26, 67, 1, '2025-05-30', 517000),
(27, 67, 1, '2025-05-30', 243000),
(28, 55, 1, '2025-05-30', 42000),
(29, 55, 1, '2025-05-30', 273000),
(30, 55, 1, '2025-05-30', 222000),
(31, 55, 1, '2025-05-30', 89000),
(32, 55, 1, '2025-06-01', 195000),
(33, 55, 1, '2025-06-01', 4038000),
(34, 5, 1, '2025-06-04', 1140000);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `cedula` (`cedula`),
  ADD UNIQUE KEY `email_cliente` (`email_cliente`);

--
-- Indices de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_venta` (`id_venta`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `garantia_producto`
--
ALTER TABLE `garantia_producto`
  ADD PRIMARY KEY (`id_garantia`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `garantia_servicio`
--
ALTER TABLE `garantia_servicio`
  ADD PRIMARY KEY (`id_garantia`),
  ADD KEY `id_servicio` (`id_servicio`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `id_proveedor` (`id_proveedor`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`id_proveedor`),
  ADD UNIQUE KEY `nit` (`nit`);

--
-- Indices de la tabla `servicio_tecnico`
--
ALTER TABLE `servicio_tecnico`
  ADD PRIMARY KEY (`id_servicio`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `venta`
--
ALTER TABLE `venta`
  ADD PRIMARY KEY (`id_venta`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT de la tabla `garantia_producto`
--
ALTER TABLE `garantia_producto`
  MODIFY `id_garantia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `garantia_servicio`
--
ALTER TABLE `garantia_servicio`
  MODIFY `id_garantia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `servicio_tecnico`
--
ALTER TABLE `servicio_tecnico`
  MODIFY `id_servicio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT de la tabla `venta`
--
ALTER TABLE `venta`
  MODIFY `id_venta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `Detalle_Venta_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `venta` (`id_venta`),
  ADD CONSTRAINT `Detalle_Venta_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`);

--
-- Filtros para la tabla `garantia_producto`
--
ALTER TABLE `garantia_producto`
  ADD CONSTRAINT `Garantia_Producto_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`);

--
-- Filtros para la tabla `garantia_servicio`
--
ALTER TABLE `garantia_servicio`
  ADD CONSTRAINT `Garantia_Servicio_ibfk_1` FOREIGN KEY (`id_servicio`) REFERENCES `servicio_tecnico` (`id_servicio`);

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `Producto_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedor` (`id_proveedor`);

--
-- Filtros para la tabla `servicio_tecnico`
--
ALTER TABLE `servicio_tecnico`
  ADD CONSTRAINT `Servicio_Tecnico_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `Servicio_Tecnico_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `venta`
--
ALTER TABLE `venta`
  ADD CONSTRAINT `Venta_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `Venta_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
