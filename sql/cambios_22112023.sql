use rehabilitar_testing;

create table informe_estudio(
	id int primary key auto_increment,
    id_estudio int not null,
    id_area int not null,
    id_turno int not null,
    id_fact_informe int not null,
    observaciones varchar(200) default null
);
create table fact_informe_area(
	id int primary key auto_increment,
    id_informe int not null,
    token_archivo varchar(150) not null
);
create table archivos(
	id int primary key auto_increment,
    id_usuario_creador int not null,
    original_filename varchar(100) not null,
    token_archivo varchar(150) not null,
    created_at datetime default current_timestamp,
	deleted_at datetime default null
);
create table fact_asistencia_estaciones(
	id int primary key auto_increment,
    id_turno int not null,
    id_area_atendida int not null,
    created_at datetime default current_timestamp
);