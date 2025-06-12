-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 12-06-2025 a las 21:19:26
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
  `numero_documento` varchar(20) NOT NULL,
  `direccion_cliente` varchar(255) NOT NULL,
  `telefono_cliente` varchar(20) NOT NULL,
  `email_cliente` varchar(100) NOT NULL,
  `tipo_documento` varchar(20) NOT NULL,
  `fecha_registro` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `nombre_cliente`, `numero_documento`, `direccion_cliente`, `telefono_cliente`, `email_cliente`, `tipo_documento`, `fecha_registro`) VALUES
(1, 'Carlos Rodríguez', '1001234567', 'Calle 12 #45-67', '3104567890', 'carlosr@example.com', 'CC', '2025-01-15'),
(2, 'María Gómez', '2009876543', 'Carrera 7 #34-56', '3112345678', 'mariag@example.com', 'TI', '2025-02-10'),
(3, 'Andrés Torres', '3004567890', 'Avenida 9 #65-32', '3123456789', 'andrest@example.com', 'CE', '2025-03-08'),
(4, 'Laura Fernández', '4007654321', 'Transversal 4 #12-34', '3134567890', 'lauraf@example.com', 'Pasaporte', '2025-04-21'),
(5, 'Paola Ríos', '6009873210', 'Calle 22 #33-44', '3156789012', 'paolar@example.com', 'TI', '2025-06-01'),
(6, 'David Ruiz', '7004561239', 'Carrera 11 #55-66', '3167890123', 'davidr@example.com', 'CE', '2025-06-20'),
(7, 'Camila Herrera', '8007418529', 'Calle 5 #20-18', '3178901234', 'camilah@example.com', 'Pasaporte', '2025-05-14'),
(8, 'Esteban Quintero', '9001597538', 'Avenida 6 #44-77', '3189012345', 'estebanq@example.com', 'CC', '2025-02-19'),
(9, 'Natalia Castro', '1000473829', 'Carrera 2 #29-89', '3190123456', 'nataliac@example.com', 'TI', '2025-04-03'),
(10, 'Sebastián Márquez', '1011234560', 'Calle 8 #17-19', '3201234567', 'sebastianm@example.com', 'CE', '2025-05-18'),
(11, 'Daniela Nieto', '1024567891', 'Carrera 4 #22-80', '3212345678', 'danielan@example.com', 'Pasaporte', '2025-03-25'),
(12, 'Luis Pérez', '1037894562', 'Avenida 1 #30-20', '3223456789', 'luisp@example.com', 'CC', '2025-04-12'),
(13, 'Valentina Mora', '1043216543', 'Calle 17 #5-10', '3234567890', 'valentinam@example.com', 'TI', '2025-01-28'),
(14, 'Tomás Arias', '1056549874', 'Carrera 10 #9-40', '3245678901', 'tomasa@example.com', 'CE', '2025-05-06'),
(15, 'Isabella Salazar', '1069873215', 'Calle 3 #13-70', '3256789012', 'isabellas@example.com', 'Pasaporte', '2025-06-20'),
(16, 'Mateo Romero', '1071237896', 'Diagonal 2 #18-65', '3267890123', 'mateor@example.com', 'CC', '2025-04-05'),
(17, 'Sofía Méndez', '1084561237', 'Carrera 12 #40-12', '3278901234', 'sofiam@example.com', 'TI', '2025-03-18'),
(18, 'Gabriel Castaño', '1097894568', 'Avenida 7 #16-90', '3289012345', 'gabrielc@example.com', 'CE', '2025-04-02'),
(19, 'Luciana Ramírez', '1103216549', 'Calle 15 #28-88', '3290123456', 'lucianar@example.com', 'Pasaporte', '2025-04-08'),
(20, 'Emilia Vargas', '1112345670', 'Calle 10 #20-30', '3011234567', 'emiliav@example.com', 'TI', '2025-01-22'),
(21, 'Juan Méndez', '1123456781', 'Carrera 15 #5-60', '3022345678', 'juanm@example.com', 'CC', '2025-02-14'),
(22, 'Sara Ocampo', '1134567892', 'Calle 33 #44-22', '3033456789', 'sarao@example.com', 'CE', '2025-03-11'),
(23, 'Pedro Morales', '1145678903', 'Avenida 12 #7-77', '3044567890', 'pedrom@example.com', 'Pasaporte', '2025-04-01'),
(24, 'Juliana Gil', '1156789014', 'Transversal 8 #6-12', '3055678901', 'julianag@example.com', 'CC', '2025-04-27'),
(25, 'Felipe Lozano', '1167890125', 'Calle 19 #10-50', '3066789012', 'felipel@example.com', 'TI', '2025-05-16'),
(26, 'Ana Beltrán', '1178901236', 'Carrera 9 #55-32', '3077890123', 'anab@example.com', 'CE', '2025-06-09'),
(27, 'Ricardo Duarte', '1189012347', 'Diagonal 7 #22-15', '3088901234', 'ricardod@example.com', 'Pasaporte', '2025-06-11'),
(28, 'Valeria Rincón', '1190123458', 'Calle 6 #18-80', '3099012345', 'valeriar@example.com', 'CC', '2025-07-25'),
(29, 'Nicolás Torres', '1201234569', 'Carrera 18 #40-44', '3100123456', 'nicolast@example.com', 'TI', '2025-08-19'),
(30, 'Daniela Suárez', '1212345670', 'Avenida 5 #30-70', '3111234567', 'danielas@example.com', 'Pasaporte', '2025-09-10'),
(31, 'Joaquin Cañon', '1012443507', 'tv 77 i # 65 j 16 sur ', '3053970242', 'Danielcf97@hotmail.com', 'CC', '2025-06-12');

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
(1, 1, 22, 1, 58000),
(2, 2, 1, 1, 45000),
(3, 2, 2, 1, 50000),
(4, 3, 22, 1, 58000),
(5, 4, 5, 1, 100000),
(6, 4, 11, 1, 8000),
(7, 5, 22, 1, 58000),
(8, 6, 4, 1, 45000),
(9, 6, 8, 1, 40000),
(10, 7, 26, 1, 48000),
(11, 8, 9, 1, 130000),
(12, 9, 7, 2, 27000),
(13, 10, 14, 1, 110000),
(14, 11, 10, 1, 95000),
(15, 11, 7, 1, 7000),
(16, 12, 9, 1, 130000),
(17, 13, 17, 1, 85000),
(18, 14, 6, 1, 96000),
(19, 15, 15, 1, 130000),
(20, 16, 22, 1, 58000),
(21, 17, 4, 1, 45000),
(22, 17, 8, 1, 48000),
(23, 18, 10, 1, 95000),
(24, 19, 5, 1, 100000),
(25, 20, 4, 2, 54000),
(26, 21, 1, 1, 45000),
(27, 22, 22, 1, 58000),
(28, 23, 3, 1, 33000),
(29, 23, 10, 1, 64000),
(30, 24, 16, 2, 33000),
(31, 25, 14, 1, 110000),
(32, 26, 22, 1, 58000),
(33, 27, 13, 1, 89000),
(34, 28, 8, 1, 48000),
(35, 28, 12, 1, 44000),
(36, 29, 17, 1, 85000),
(37, 30, 23, 1, 60000);

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
(1, 1, '2025-01-15', '2025-03-15'),
(2, 2, '2025-01-29', '2025-02-28'),
(3, 3, '2025-02-05', '2025-05-05'),
(4, 4, '2025-02-13', '2025-04-13'),
(5, 5, '2025-02-18', '2025-03-18'),
(6, 6, '2025-02-27', '2025-05-27'),
(7, 7, '2025-03-05', '2025-05-05'),
(8, 8, '2025-03-10', '2025-04-10'),
(9, 9, '2025-03-16', '2025-06-16'),
(10, 10, '2025-03-25', '2025-05-25'),
(11, 11, '2025-04-01', '2025-05-01'),
(12, 12, '2025-04-07', '2025-06-07'),
(13, 13, '2025-04-15', '2025-07-15'),
(14, 14, '2025-04-22', '2025-06-22'),
(15, 15, '2025-04-30', '2025-05-30'),
(16, 16, '2025-05-08', '2025-07-08'),
(17, 17, '2025-05-15', '2025-06-15'),
(18, 18, '2025-05-22', '2025-08-22'),
(19, 19, '2025-05-30', '2025-07-30'),
(20, 20, '2025-06-03', '2025-07-03'),
(21, 21, '2025-06-07', '2025-08-07'),
(22, 22, '2025-06-10', '2025-07-10'),
(23, 23, '2025-06-12', '2025-09-12'),
(24, 24, '2025-06-14', '2025-08-14'),
(25, 25, '2025-06-17', '2025-07-17');

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
(1, 'Teclado USB', 'KB-100', 'Teclado básico alámbrico USB', 30000, 25, 1, 12, '2025-01-10 05:00:00', 45000),
(2, 'Cable HDMI 2m', 'HDMI-2M', 'Cable HDMI de 2 metros', 15000, 40, 2, 6, '2025-01-17 05:00:00', 25000),
(3, 'Adaptador HDMI a VGA', 'AD-HDVGA', 'Convertidor HDMI a VGA con audio', 18000, 35, 13, 6, '2025-02-03 05:00:00', 28000),
(4, 'Memoria USB 32GB', 'USB-32', 'Memoria flash 32GB USB 3.0', 28000, 50, 10, 24, '2025-02-11 05:00:00', 40000),
(5, 'Disco duro externo 1TB', 'HDD-1TB', 'Disco portátil 1TB USB 3.1', 160000, 12, 20, 12, '2025-02-26 05:00:00', 200000),
(6, 'Teclado mecánico RGB', 'KBG-500', 'Teclado gamer mecánico con retroiluminación', 120000, 10, 14, 12, '2025-03-02 05:00:00', 165000),
(7, 'Cable VGA 1.5m', 'VGA-1.5', 'Cable VGA estándar de 1.5 metros', 10000, 45, 17, 6, '2025-03-09 05:00:00', 17000),
(8, 'Memoria USB 64GB', 'USB-64', 'Memoria flash USB 64GB 3.0', 40000, 40, 30, 24, '2025-03-20 05:00:00', 58000),
(9, 'Disco SSD 256GB', 'SSD-256', 'Unidad sólida 256GB SATA3', 95000, 20, 15, 24, '2025-03-30 05:00:00', 130000),
(10, 'Teclado inalámbrico', 'KB-WL', 'Teclado sin cables con receptor USB', 70000, 15, 25, 12, '2025-04-05 05:00:00', 95000),
(11, 'Cable HDMI 5m', 'HDMI-5M', 'Cable HDMI largo de 5 metros', 22000, 25, 26, 6, '2025-04-12 05:00:00', 32000),
(12, 'Adaptador VGA a HDMI', 'AD-VGAHD', 'Conversor VGA a HDMI con audio incluido', 25000, 30, 18, 6, '2025-04-23 05:00:00', 36000),
(13, 'Memoria RAM 8GB DDR4', 'RAM-8GB', 'RAM 8GB DDR4 2666MHz', 130000, 12, 23, 36, '2025-05-02 05:00:00', 180000),
(14, 'Disco duro 500GB', 'HDD-500', 'HDD interno 500GB SATA', 80000, 10, 22, 12, '2025-05-10 05:00:00', 110000),
(15, 'Teclado ergonómico', 'KB-ERGO', 'Teclado ergonómico para oficina', 95000, 8, 19, 12, '2025-05-18 05:00:00', 130000),
(16, 'Cable VGA 3m', 'VGA-3M', 'Cable VGA reforzado de 3 metros', 16000, 20, 29, 6, '2025-05-27 05:00:00', 22000),
(17, 'Memoria USB 128GB', 'USB-128', 'Memoria flash 128GB 3.0', 68000, 18, 24, 24, '2025-06-01 05:00:00', 85000),
(18, 'SSD 512GB', 'SSD-512', 'Unidad de estado sólido 512GB NVMe', 150000, 10, 12, 24, '2025-06-05 05:00:00', 200000),
(19, 'Teclado multimedia', 'KB-MULTI', 'Teclado con teclas multimedia dedicadas', 48000, 18, 28, 12, '2025-06-08 05:00:00', 65000),
(20, 'Adaptador USB a HDMI', 'AD-USBHD', 'Adaptador USB 3.0 a HDMI full HD', 33000, 20, 27, 6, '2025-06-10 05:00:00', 48000),
(21, 'Memoria RAM 16GB DDR4', 'RAM-16GB', 'RAM 16GB DDR4 3200MHz', 250000, 6, 21, 36, '2025-06-11 05:00:00', 330000),
(22, 'Cartucho HP 664 Negro', 'HP-664BK', 'Cartucho original HP 664 negro para impresoras DeskJet', 40000, 20, 7, 12, '2025-01-12 05:00:00', 58000),
(23, 'Cartucho HP 664 Tricolor', 'HP-664C', 'Cartucho original HP 664 tricolor (C/M/Y)', 42000, 18, 7, 12, '2025-01-25 05:00:00', 60000),
(24, 'Cartucho Canon PG-145 Negro', 'CN-145BK', 'Cartucho Canon PG-145 negro para PIXMA', 38000, 15, 12, 12, '2025-02-08 05:00:00', 55000),
(25, 'Cartucho Canon CL-146 Tricolor', 'CN-146C', 'Cartucho Canon CL-146 tricolor compatible con PIXMA', 41000, 12, 12, 12, '2025-02-18 05:00:00', 59000),
(26, 'Cartucho Epson T664 Negro', 'EP-T664BK', 'Botella de tinta Epson T664 negra para L220/L365', 35000, 30, 13, 24, '2025-03-03 05:00:00', 48000),
(27, 'Cartucho Epson T664 Tricolor', 'EP-T664C', 'Botellas de tinta Epson T664 C/M/Y para L-series', 36000, 28, 13, 24, '2025-03-15 05:00:00', 50000),
(28, 'Cartucho Brother LC-3011 Negro', 'BR-3011BK', 'Cartucho Brother negro LC3011 para DCP-T510W', 37000, 10, 21, 12, '2025-04-02 05:00:00', 52000),
(29, 'Cartucho Brother LC-3011 Tricolor', 'BR-3011C', 'Cartucho Brother tricolor LC3011 para multifuncionales', 39000, 10, 21, 12, '2025-04-11 05:00:00', 54000),
(30, 'Cartucho genérico HP 662 Negro', 'HP-662GEN-BK', 'Cartucho compatible con HP 662 negro', 30000, 25, 24, 6, '2025-05-06 05:00:00', 45000),
(31, 'Cartucho genérico HP 662 Tricolor', 'HP-662GEN-C', 'Cartucho compatible con HP 662 tricolor', 32000, 25, 24, 6, '2025-05-12 05:00:00', 47000);

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
  `direccion_proveedor` varchar(255) NOT NULL,
  `fecha_registro` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedor`
--

INSERT INTO `proveedor` (`id_proveedor`, `nit`, `nombre_proveedor`, `representante_ventas`, `telefono_representante_ventas`, `direccion_proveedor`, `fecha_registro`) VALUES
(1, '900123456', 'Proveedor Tech', 'Carlos López', '3112345678', 'Calle 123 #45-67, Ciudad', '2025-04-20'),
(2, '900654321', 'Electro S.A.', 'Ana Gómez', '3223456789', 'Avenida 78 #12-34, Ciudad', '2025-04-20'),
(7, '9001234561', 'Impresoras D', 'Carlos Quintero', '3223244343', 'cra 9789', '2025-04-20'),
(10, '7321879361', 'Memorias USb', 'Joseeee', '4223244434', 'cra 98-98', '2025-04-20'),
(12, '901234567', 'Soluciones Tech', 'Laura Martínez', '3101234567', 'Calle 45 #23-10, Bogotá', '2025-04-20'),
(13, '902345678', 'Insumos PC', 'Miguel Torres', '3139876543', 'Carrera 9 #12-45, Medellín', '2025-05-12'),
(14, '903456789', 'Componentes S.A.S.', 'Andrés Gutiérrez', '3147654321', 'Transversal 33 #56-78, Cali', '2025-05-12'),
(15, '904567890', 'Distribuciones Norte', 'Diana Ríos', '3112233445', 'Calle 12 #34-56, Bucaramanga', '2025-05-12'),
(16, '905678901', 'TecnoPartes', 'Juan Ruiz', '3123344556', 'Av. Simón Bolívar #78-90, Barranquilla', '2025-05-12'),
(17, '906789012', 'Electronix Plus', 'Patricia Peña', '3201239876', 'Cra 45A #67-89, Cartagena', '2025-05-20'),
(18, '907890123', 'Mayoristas Bogotá', 'Camilo Paredes', '3156677889', 'Calle 80 #45-67, Bogotá', '2025-05-20'),
(19, '908901234', 'Multiservicios Andes', 'Viviana Castro', '3167788990', 'Carrera 7 #98-76, Pasto', '2025-05-20'),
(20, '909012345', 'Repuestos Express', 'Luis Rodríguez', '3178899001', 'Av. El Dorado #10-50, Bogotá', '2025-05-20'),
(21, '910123456', 'Accesorios Tech', 'Natalia Velásquez', '3189900112', 'Cra 50 #60-30, Manizales', '2025-05-20'),
(22, '911234567', 'TecnoMundo Ltda.', 'Esteban Parra', '3111109876', 'Carrera 15 #45-89, Neiva', '2025-06-12'),
(23, '912345678', 'Suministros Globales', 'Carolina Méndez', '3122203344', 'Calle 100 #12-45, Bogotá', '2025-06-12'),
(24, '913456789', 'Distribuidora Omega', 'Ricardo Luna', '3133304455', 'Cra 18 #25-60, Medellín', '2025-06-12'),
(25, '914567890', 'Proveedora del Caribe', 'María Restrepo', '3144405566', 'Av. Circunvalar #89-20, Barranquilla', '2025-06-12'),
(26, '915678901', 'ElectroHogar', 'David Gómez', '3155506677', 'Calle 10 #34-90, Bucaramanga', '2025-06-12'),
(27, '916789012', 'Tech Parts Express', 'Daniela Vargas', '3166607788', 'Av. Roosevelt #56-78, Cali', '2025-06-12'),
(28, '917890123', 'Logística y Suministros SAS', 'Santiago Páez', '3177708899', 'Calle 72 #23-56, Cúcuta', '2025-06-12'),
(29, '918901234', 'Corporación Digital', 'Mónica Acosta', '3188809900', 'Cra 24 #70-80, Ibagué', '2025-06-12'),
(30, '919012345', 'Red Solutions', 'Felipe Hernández', '3199900111', 'Carrera 50 #10-45, Pereira', '2025-06-12'),
(31, '920123456', 'Zona Computadores', 'Sandra León', '3200011223', 'Calle 30 #40-50, Montería', '2025-06-12');

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
(1, 1, 1, 'Computador de mesa', 'HP ProDesk', 'No enciende, posible daño en fuente.', '2025-01-10', '2025-01-15', 'Finalizado', 2),
(2, 2, 1, 'Computador portátil', 'Lenovo ThinkPad', 'Pantalla parpadea.', '2025-01-22', '2025-01-29', 'Finalizado', 1),
(3, 3, 1, 'Impresora láser', 'Brother HL-1200', 'Atascos frecuentes de papel.', '2025-01-30', '2025-02-05', 'Finalizado', 3),
(4, 4, 1, 'Impresora de tinta', 'Canon PIXMA G2100', 'No imprime a color.', '2025-02-06', '2025-02-13', 'Finalizado', 2),
(5, 5, 1, 'Impresora térmica', 'Zebra TLP2844', 'Impresión borrosa.', '2025-02-12', '2025-02-18', 'Finalizado', 1),
(6, 6, 1, 'Computador de mesa', 'Dell OptiPlex 3080', 'Reinicios aleatorios.', '2025-02-20', '2025-02-27', 'Finalizado', 3),
(7, 7, 1, 'Computador portátil', 'HP Pavilion', 'Se apaga al desconectar el cargador.', '2025-02-28', '2025-03-05', 'Finalizado', 2),
(8, 8, 1, 'Impresora láser', 'Samsung Xpress M2020', 'Tóner nuevo no reconocido.', '2025-03-04', '2025-03-10', 'Finalizado', 1),
(9, 9, 1, 'Impresora de tinta', 'Epson L3150', 'Fugas de tinta.', '2025-03-09', '2025-03-16', 'Finalizado', 3),
(10, 10, 1, 'Impresora térmica', 'Xprinter XP-58IIH', 'No imprime nada.', '2025-03-18', '2025-03-25', 'Finalizado', 2),
(11, 11, 1, 'Computador de mesa', 'Asus VivoPC', 'Se congela al iniciar.', '2025-03-25', '2025-04-01', 'Finalizado', 1),
(12, 12, 1, 'Computador portátil', 'Acer Aspire 5', 'Teclado no responde.', '2025-04-01', '2025-04-07', 'Finalizado', 2),
(13, 13, 1, 'Impresora láser', 'HP LaserJet 1020', 'Líneas negras al imprimir.', '2025-04-09', '2025-04-15', 'Finalizado', 3),
(14, 14, 1, 'Impresora de tinta', 'Canon MG3510', 'Impresión muy lenta.', '2025-04-15', '2025-04-22', 'Finalizado', 2),
(15, 15, 1, 'Impresora térmica', 'Epson TM-T20II', 'No alimenta el papel.', '2025-04-23', '2025-04-30', 'Finalizado', 1),
(16, 16, 1, 'Computador de mesa', 'Lenovo ThinkCentre', 'No detecta disco duro.', '2025-05-02', '2025-05-08', 'Finalizado', 2),
(17, 17, 1, 'Computador portátil', 'Dell Inspiron 15', 'Batería no carga.', '2025-05-09', '2025-05-15', 'Finalizado', 1),
(18, 18, 1, 'Impresora láser', 'Brother DCP-L2540DW', 'Pantalla muestra error general.', '2025-05-17', '2025-05-22', 'Finalizado', 3),
(19, 19, 1, 'Impresora de tinta', 'Epson EcoTank L3250', 'Cabezal tapado.', '2025-05-24', '2025-05-30', 'Finalizado', 2),
(20, 20, 1, 'Impresora térmica', 'Bixolon SRP-350', 'Luces intermitentes, no imprime.', '2025-05-28', '2025-06-03', 'Finalizado', 1),
(21, 21, 1, 'Computador de mesa', 'HP All-in-One', 'Lentitud extrema.', '2025-06-01', '2025-06-07', 'Pendiente', 2),
(22, 22, 1, 'Computador portátil', 'Lenovo IdeaPad', 'Ruido de ventilador.', '2025-06-03', '2025-06-10', 'Pendiente', 1),
(23, 23, 1, 'Impresora láser', 'Canon LBP6030', 'No imprime desde red.', '2025-06-06', '2025-06-12', 'Pendiente', 3),
(24, 24, 1, 'Impresora de tinta', 'HP DeskJet 2720', 'Se desconecta sola.', '2025-06-08', '2025-06-14', 'Pendiente', 2),
(25, 25, 1, 'Impresora térmica', 'Xprinter XP-C260H', 'No corta papel automáticamente.', '2025-06-10', '2025-06-17', 'Pendiente', 1);

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
(1, 1, 1, '2025-01-05', 58000),
(2, 2, 1, '2025-01-15', 95000),
(3, 3, 1, '2025-01-28', 58000),
(4, 4, 1, '2025-02-06', 108000),
(5, 5, 1, '2025-02-12', 58000),
(6, 6, 1, '2025-02-20', 85000),
(7, 7, 1, '2025-02-28', 48000),
(8, 8, 1, '2025-03-04', 130000),
(9, 9, 1, '2025-03-10', 54000),
(10, 10, 1, '2025-03-15', 110000),
(11, 11, 1, '2025-03-20', 92000),
(12, 12, 1, '2025-03-30', 130000),
(13, 13, 1, '2025-04-05', 85000),
(14, 14, 1, '2025-04-12', 96000),
(15, 15, 1, '2025-04-18', 130000),
(16, 16, 1, '2025-04-25', 58000),
(17, 17, 1, '2025-05-02', 93000),
(18, 18, 1, '2025-05-08', 95000),
(19, 19, 1, '2025-05-15', 100000),
(20, 20, 1, '2025-05-22', 108000),
(21, 21, 1, '2025-05-28', 45000),
(22, 22, 1, '2025-06-01', 58000),
(23, 23, 1, '2025-06-05', 97000),
(24, 24, 1, '2025-06-10', 66000),
(25, 25, 1, '2025-06-12', 110000),
(26, 26, 1, '2025-06-15', 58000),
(27, 27, 1, '2025-06-18', 89000),
(28, 28, 1, '2025-06-22', 92000),
(29, 29, 1, '2025-06-26', 85000),
(30, 30, 1, '2025-06-30', 60000);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `cedula` (`numero_documento`),
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
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT de la tabla `garantia_producto`
--
ALTER TABLE `garantia_producto`
  MODIFY `id_garantia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `garantia_servicio`
--
ALTER TABLE `garantia_servicio`
  MODIFY `id_garantia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `servicio_tecnico`
--
ALTER TABLE `servicio_tecnico`
  MODIFY `id_servicio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT de la tabla `venta`
--
ALTER TABLE `venta`
  MODIFY `id_venta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

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
