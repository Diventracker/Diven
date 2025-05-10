-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 10-05-2025 a las 21:12:58
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
-- Estructura de tabla para la tabla `Cliente`
--

CREATE TABLE `Cliente` (
  `id_cliente` int(11) NOT NULL,
  `nombre_cliente` varchar(100) NOT NULL,
  `cedula` varchar(20) NOT NULL,
  `direccion_cliente` varchar(255) NOT NULL,
  `telefono_cliente` varchar(20) NOT NULL,
  `email_cliente` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Cliente`
--

INSERT INTO `Cliente` (`id_cliente`, `nombre_cliente`, `cedula`, `direccion_cliente`, `telefono_cliente`, `email_cliente`) VALUES
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
(45, 'Zoeeee Guadalupe', '129012345', 'Diagonal 78', '3222323232', 'andw@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Detalle_Venta`
--

CREATE TABLE `Detalle_Venta` (
  `id_detalle` int(11) NOT NULL,
  `id_venta` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Garantia_Producto`
--

CREATE TABLE `Garantia_Producto` (
  `id_garantia` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `origen_garantia` enum('compra_proveedor','venta_cliente') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Garantia_Servicio`
--

CREATE TABLE `Garantia_Servicio` (
  `id_garantia` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Producto`
--

CREATE TABLE `Producto` (
  `id_producto` int(11) NOT NULL,
  `nombre_producto` varchar(100) NOT NULL,
  `marca` varchar(50) NOT NULL,
  `modelo` varchar(50) NOT NULL,
  `descripcion` text NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `id_proveedor` int(11) NOT NULL,
  `fecha_inicio_garantia` date DEFAULT NULL,
  `fecha_expiracion_garantia` date DEFAULT NULL,
  `fecha_compra` date NOT NULL,
  `precio_venta` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Producto`
--

INSERT INTO `Producto` (`id_producto`, `nombre_producto`, `marca`, `modelo`, `descripcion`, `precio`, `stock`, `id_proveedor`, `fecha_inicio_garantia`, `fecha_expiracion_garantia`, `fecha_compra`, `precio_venta`) VALUES
(1, 'Laptop Gamer', 'Asus', 'ROG Strix', 'Laptop de alto rendimiento para gaming', 4500000.00, 10, 1, NULL, NULL, '2024-01-01', 40000.00),
(2, 'Laptop Gamer', 'Asus', 'ROG Strix', 'Laptop de alto rendimiento para gaming', 4400000.00, 5, 2, '2024-02-01', '2026-02-01', '2024-02-01', 50000.00),
(4, 'USBB ', 'kingston', 'b876', '32gb', 5000.00, 32, 2, '2025-04-04', '2025-04-12', '2025-04-11', 10000.00),
(5, 'Tecladinho', 'Redragon', 'K552', 'White', 100000.00, 32, 7, '2025-04-03', '2025-04-19', '2025-04-04', 180000.00),
(8, 'Computador', 'hp', 'paser76', 'Amd, 16gb ram', 1000000.00, 3, 1, '2025-04-01', '2025-04-25', '2025-04-07', 1400000.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Proveedor`
--

CREATE TABLE `Proveedor` (
  `id_proveedor` int(11) NOT NULL,
  `nit` varchar(20) NOT NULL,
  `nombre_proveedor` varchar(100) NOT NULL,
  `representante_ventas` varchar(100) NOT NULL,
  `telefono_representante_ventas` varchar(20) NOT NULL,
  `direccion_proveedor` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Proveedor`
--

INSERT INTO `Proveedor` (`id_proveedor`, `nit`, `nombre_proveedor`, `representante_ventas`, `telefono_representante_ventas`, `direccion_proveedor`) VALUES
(1, '900123456', 'Proveedor Tech', 'Carlos López', '3112345678', 'Calle 123 #45-67, Ciudad'),
(2, '900654321', 'Electro S.A.', 'Ana Gómez', '3223456789', 'Avenida 78 #12-34, Ciudad'),
(7, '9001234561', 'Impresoras D', 'Carlos Quintero', '3223244343', 'cra 9789'),
(10, '7321879361', 'Memorias USb', 'Joseeee', '4223244434', 'cra 98-98');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Servicio_Tecnico`
--

CREATE TABLE `Servicio_Tecnico` (
  `id_servicio` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `tipo_equipo` varchar(50) NOT NULL,
  `marca_equipo` varchar(50) NOT NULL,
  `modelo_equipo` varchar(50) NOT NULL,
  `descripcion_problema` text NOT NULL,
  `fecha_recepcion` date NOT NULL,
  `fecha_entrega_estimada` date NOT NULL,
  `estado_servicio` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Servicio_Tecnico`
--

INSERT INTO `Servicio_Tecnico` (`id_servicio`, `id_cliente`, `id_usuario`, `tipo_equipo`, `marca_equipo`, `modelo_equipo`, `descripcion_problema`, `fecha_recepcion`, `fecha_entrega_estimada`, `estado_servicio`) VALUES
(10, 18, 1, 'sdasda', 'dasdas', 'dasdas', 'dsadasd', '2025-04-01', '2025-04-17', 'Finalizado'),
(11, 45, 1, 'Portatil', 'Asus', 'rog76', 'No prende', '2025-04-01', '2025-04-17', 'En Progreso'),
(13, 45, 1, 'sdsads', 'dsadsa', 'dsadsa', 'dsadas', '2025-04-01', '2025-04-17', 'En Progreso'),
(14, 16, 1, 'Computador', 'asus', 'rog89', 'le falla la ram', '2025-04-07', '2025-04-10', 'Finalizado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Usuario`
--

CREATE TABLE `Usuario` (
  `id_usuario` int(11) NOT NULL,
  `nombre_usuario` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `clave` varchar(255) NOT NULL,
  `rol` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `Usuario`
--

INSERT INTO `Usuario` (`id_usuario`, `nombre_usuario`, `correo`, `clave`, `rol`) VALUES
(1, 'Administrador', 'admin@tienda.com', '$2b$12$JzamhaLIewvcMWRU3qq6r.lngMaMp7BhaacgLBRJoktjDfftpaJle', 'Administrador'),
(6, 'Test', 'test-hh08p33yo@srv1.mail-tester.com', '$2b$12$r6Jl3YLSy2Y09Zb6O9c0jehbVrzcNnh170hzktc4NNs5EbrFgl066', 'Administrador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Venta`
--

CREATE TABLE `Venta` (
  `id_venta` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `fecha_venta` date NOT NULL,
  `total_venta` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `Cliente`
--
ALTER TABLE `Cliente`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `cedula` (`cedula`),
  ADD UNIQUE KEY `email_cliente` (`email_cliente`);

--
-- Indices de la tabla `Detalle_Venta`
--
ALTER TABLE `Detalle_Venta`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_venta` (`id_venta`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `Garantia_Producto`
--
ALTER TABLE `Garantia_Producto`
  ADD PRIMARY KEY (`id_garantia`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `Garantia_Servicio`
--
ALTER TABLE `Garantia_Servicio`
  ADD PRIMARY KEY (`id_garantia`),
  ADD KEY `id_servicio` (`id_servicio`);

--
-- Indices de la tabla `Producto`
--
ALTER TABLE `Producto`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `id_proveedor` (`id_proveedor`);

--
-- Indices de la tabla `Proveedor`
--
ALTER TABLE `Proveedor`
  ADD PRIMARY KEY (`id_proveedor`),
  ADD UNIQUE KEY `nit` (`nit`);

--
-- Indices de la tabla `Servicio_Tecnico`
--
ALTER TABLE `Servicio_Tecnico`
  ADD PRIMARY KEY (`id_servicio`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `Usuario`
--
ALTER TABLE `Usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `Venta`
--
ALTER TABLE `Venta`
  ADD PRIMARY KEY (`id_venta`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `Cliente`
--
ALTER TABLE `Cliente`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT de la tabla `Detalle_Venta`
--
ALTER TABLE `Detalle_Venta`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `Garantia_Producto`
--
ALTER TABLE `Garantia_Producto`
  MODIFY `id_garantia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `Garantia_Servicio`
--
ALTER TABLE `Garantia_Servicio`
  MODIFY `id_garantia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `Producto`
--
ALTER TABLE `Producto`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `Proveedor`
--
ALTER TABLE `Proveedor`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `Servicio_Tecnico`
--
ALTER TABLE `Servicio_Tecnico`
  MODIFY `id_servicio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `Usuario`
--
ALTER TABLE `Usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `Venta`
--
ALTER TABLE `Venta`
  MODIFY `id_venta` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `Detalle_Venta`
--
ALTER TABLE `Detalle_Venta`
  ADD CONSTRAINT `Detalle_Venta_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `Venta` (`id_venta`),
  ADD CONSTRAINT `Detalle_Venta_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `Producto` (`id_producto`);

--
-- Filtros para la tabla `Garantia_Producto`
--
ALTER TABLE `Garantia_Producto`
  ADD CONSTRAINT `Garantia_Producto_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `Producto` (`id_producto`);

--
-- Filtros para la tabla `Garantia_Servicio`
--
ALTER TABLE `Garantia_Servicio`
  ADD CONSTRAINT `Garantia_Servicio_ibfk_1` FOREIGN KEY (`id_servicio`) REFERENCES `Servicio_Tecnico` (`id_servicio`);

--
-- Filtros para la tabla `Producto`
--
ALTER TABLE `Producto`
  ADD CONSTRAINT `Producto_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `Proveedor` (`id_proveedor`);

--
-- Filtros para la tabla `Servicio_Tecnico`
--
ALTER TABLE `Servicio_Tecnico`
  ADD CONSTRAINT `Servicio_Tecnico_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `Cliente` (`id_cliente`),
  ADD CONSTRAINT `Servicio_Tecnico_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id_usuario`);

--
-- Filtros para la tabla `Venta`
--
ALTER TABLE `Venta`
  ADD CONSTRAINT `Venta_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `Cliente` (`id_cliente`),
  ADD CONSTRAINT `Venta_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id_usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
