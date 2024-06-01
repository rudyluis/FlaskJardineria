DROP DATABASE IF EXISTS jardineria;
CREATE DATABASE jardineria;

CREATE TABLE oficina (
  IDOficina  SERIAL not NULL,
  codigoOficina VARCHAR(10) UNIQUE NOT NULL ,
  ciudad VARCHAR(30) NOT NULL,
  pais VARCHAR(50) NOT NULL,
  region VARCHAR(50) DEFAULT NULL,
  codigoPostal VARCHAR(10) NOT NULL,
  telefono VARCHAR(20) NOT NULL,
  lineaDireccion1 VARCHAR(50) NOT NULL,
  lineaDireccion2 VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (IDOficina)
);

CREATE TABLE empleado (
  IDEmpleado SERIAL NOT NULL ,
  codigo_empleado INTEGER UNIQUE NOT NULL,
  nombre VARCHAR(50) NOT NULL,
  apellido1 VARCHAR(50) NOT NULL,
  apellido2 VARCHAR(50) DEFAULT NULL,
  extension VARCHAR(10) NOT NULL,
  email VARCHAR(100) NOT NULL,
  IDOficina INTEGER NOT NULL,
  IDEmpleadoJefe INTEGER DEFAULT NULL,
  puesto VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (IDEmpleado),
  FOREIGN KEY (IDOficina) REFERENCES oficina (IDOficina),
  FOREIGN KEY (IDEmpleadoJefe) REFERENCES empleado (IdEmpleado)
);

CREATE TABLE gamaProducto (
  IDGamaProducto serial NOT NULL ,
  gama VARCHAR(50) NOT NULL unique,
  descripcionTexto TEXT,
  descripcionHtml TEXT,
  imagen VARCHAR(256),
  PRIMARY KEY (IDGamaProducto)
);

CREATE TABLE cliente (
  IDCliente serial NOT NULL ,
  codigoCliente INTEGER NOT NULL,
  nombreCliente VARCHAR(50) NOT NULL,
  nombreContacto VARCHAR(30) DEFAULT NULL,
  apellidoContacto VARCHAR(30) DEFAULT NULL,
  telefono VARCHAR(15) NOT NULL,
  fax VARCHAR(15) NOT NULL,
  lineaDireccion1 VARCHAR(50) NOT NULL,
  lineaDireccion2 VARCHAR(50) DEFAULT NULL,
  ciudad VARCHAR(50) NOT NULL,
  region VARCHAR(50) DEFAULT NULL,
  pais VARCHAR(50) DEFAULT NULL,
  codigoPostal VARCHAR(10) DEFAULT NULL,
  IDcodigoEmpleadoVentas INTEGER DEFAULT NULL,
  limite_credito NUMERIC(15,2) DEFAULT NULL,
  PRIMARY KEY (IDCliente),
  FOREIGN KEY (IDcodigoEmpleadoVentas) REFERENCES empleado (IDEmpleado)
);

CREATE TABLE pedido (
  IDPedido serial NOT NULL ,
  codigoPedido INTEGER NOT NULL,
  fechaPedido date NOT NULL,
  fechaEsperada date NOT NULL,
  fechaEntrega date DEFAULT NULL,
  estado VARCHAR(15) NOT NULL,
  comentarios TEXT,
  IDCliente INTEGER NOT NULL,
  PRIMARY KEY (IdPedido),
  FOREIGN KEY (IDCliente) REFERENCES cliente (IDcliente)
);

CREATE TABLE producto (
  IDProducto serial NOT NULL ,
  codigo_producto VARCHAR(15) NOT NULL,
  nombre VARCHAR(70) NOT NULL,
  IDGamaProducto INT NOT NULL,
  dimensiones VARCHAR(25) NULL,
  proveedor VARCHAR(50) DEFAULT NULL,
  descripcion text NULL,
  cantidadStock SMALLINT NOT NULL,
  precioVenta NUMERIC(15,2) NOT NULL,
  precioProveedor NUMERIC(15,2) DEFAULT NULL,
  PRIMARY KEY (IDProducto),
  FOREIGN KEY (IDGamaProducto) REFERENCES gamaProducto (IDGamaProducto)
);

CREATE TABLE detallePedido (
  IDDetallePedido serial NOT NULL ,
  IDPedido INTEGER  NOT NULL,
  IDProducto INTEGER  NOT NULL,
  cantidad INTEGER NOT NULL,
  precioUnidad NUMERIC(15,2) NOT NULL,
  numeroLinea SMALLINT NOT NULL,
  PRIMARY KEY (IDDetallePedido),
  FOREIGN KEY (IDPedido) REFERENCES pedido (IDPedido),
  FOREIGN KEY (IDProducto) REFERENCES producto (IDProducto)
);

CREATE TABLE pago (
  IDPago INTEGER serial NOT NULL ,
  IDCliente INTEGER NOT NULL,
  formaPago VARCHAR(40) NOT NULL,
  nroTransaccion VARCHAR(50) NOT NULL,
  fechaPago date NOT NULL,
  total NUMERIC(15,2) NOT NULL,
  PRIMARY KEY (IDPago),
  FOREIGN KEY (IDCliente) REFERENCES cliente (IDCliente)
);
