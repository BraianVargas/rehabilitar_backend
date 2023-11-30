
create table prestador (
    id int primary key auto_increment,
    id_usuario int not null,
	codigo varchar(150) not null,
    estado tinyint not null,
    tipo_documento varchar(20) not null,
    nro_documento varchar(10) not null,
    apellido varchar(50) not null,
    nombre varchar(50) not null,
    token_firma varchar(150) not null,
    calle varchar(150) not null,
    localidad varchar(150) not null,
    provincia varchar(150) not null,
    codigo_postal varchar(10) not null,
    telefono_1 varchar(50) not null,
    telefono_2 varchar(50) default null, 
    email varchar(100) default null,
    area_id int not null,
    matricula varchar(150) not null
)