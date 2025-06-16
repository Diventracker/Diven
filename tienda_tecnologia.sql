-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 16-06-2025 a las 04:24:42
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

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
(83, 'MArcos', '3242342545', 'cra 98798689', '3123123123', 'marcosq22@gmail.com'),
(85, 'deivit', '1012328726', 'Dg 73 sur # 58 I 74', '1234567981', 'deivit@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_servicio`
--

CREATE TABLE `detalle_servicio` (
  `id_detalle` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `valor_adicional` int(10) NOT NULL DEFAULT 0,
  `motivo` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(5, 'Tecladinho', 'K552', 'White', 100000, 5, 7, 20, '2025-04-04 05:00:00', 180000),
(8, 'Computador', 'paser76', 'Amd, 16gb ram', 1000000, 10, 1, 20, '2025-04-07 05:00:00', 1400000),
(9, 'Cartucho Negro 664', '664', 'Tinta negra original HP', 25000, 10, 7, 20250501, '2025-05-01 05:00:00', 40000),
(10, 'Cartucho Color 664', '664 Color', 'Tinta color original HP', 28000, 9, 7, 20, '2025-05-01 05:00:00', 45000),
(11, 'Cartucho Negro 21', '21', 'Cartucho tinta negra HP 21', 27000, 21, 7, 20, '2025-05-02 05:00:00', 42000),
(12, 'Cartucho Color 22', '22', 'Cartucho tinta color HP 22', 30000, 10, 7, 20, '2025-05-02 05:00:00', 47000),
(13, 'Cartucho PG-145 Negro', 'PG-145', 'Tinta negra para Canon Pixma', 26000, 3, 7, 20, '2025-05-03 05:00:00', 42000),
(14, 'Cartucho CL-146 Color', 'CL-146', 'Tinta color Canon original', 32000, 9, 7, 20, '2025-05-03 05:00:00', 49000),
(16, 'Cartucho T664 Color', 'T664 Color', 'Botella tinta color Epson EcoTank', 20000, 9, 2, 20, '2025-05-04 05:00:00', 37000),
(17, 'Cartucho LC103BK', 'LC103BK', 'Tinta negra original Brother', 23000, 1, 1, 20250505, '2025-05-05 05:00:00', 39000),
(18, 'Cartucho LC103CL', 'LC103CL', 'Tinta color original Brother', 26000, 10, 1, 20, '2025-05-05 05:00:00', 43000),
(20, 'Tarjetas Diitales', 'transmi', 'trajetas xd', 6000, 1, 14, 0, '2025-06-05 04:43:37', 10000),
(21, 'Mouse Logitech', 'g879', 'Mouse negro y blanco xd', 50000, 6, 15, 0, '2025-06-05 05:06:32', 70000);

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
  `fecha_recepcion` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_entrega` date DEFAULT NULL,
  `estado_servicio` varchar(50) NOT NULL DEFAULT 'En Progreso',
  `meses_garantia` int(11) DEFAULT 0,
  `tipo_servicio` varchar(50) NOT NULL,
  `precio_servicio` int(10) NOT NULL,
  `descripcion_trabajo` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(31, 'Daniela Mora', 'daniela.mora@tienda.com', '3290001122', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Técnico', NULL, NULL),
(36, 'Andres', 'ortiz.andw@gmail.com', '3223295822', '$2b$12$xvrPtPOpbi1d2c4N5ou8Bu8DBLCOQLJWzYTQpZT1sEYDDHaA/RycK', 'Tecnico', NULL, NULL);

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
-- Indices de la tabla `detalle_servicio`
--
ALTER TABLE `detalle_servicio`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_servicio` (`id_servicio`),
  ADD KEY `id_usuario` (`id_usuario`);

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
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=86;

--
-- AUTO_INCREMENT de la tabla `detalle_servicio`
--
ALTER TABLE `detalle_servicio`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

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
  MODIFY `id_servicio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=68;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT de la tabla `venta`
--
ALTER TABLE `venta`
  MODIFY `id_venta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalle_servicio`
--
ALTER TABLE `detalle_servicio`
  ADD CONSTRAINT `detalle_servicio_ibfk_1` FOREIGN KEY (`id_servicio`) REFERENCES `servicio_tecnico` (`id_servicio`) ON DELETE CASCADE,
  ADD CONSTRAINT `detalle_servicio_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE SET NULL;

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
