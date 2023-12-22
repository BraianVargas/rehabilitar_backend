use rehabilitar_testing;

delete from campos where 1;


SET foreign_key_checks = 0;
drop table campos;
drop table campos_informacion; 

create table campos(
	id int auto_increment,
    id_area int,
    name varchar(1000),
    label varchar(1000),
    type varchar(100),
    clase varchar(200),
    options varchar(1000),
    default_value varchar(1000),
    form_orden int,
    categoria varchar(1000),
    
    primary key (id)
);

create table campos_informacion(
	id int auto_increment,
    id_campo int,
    id_turno int,
    value varchar(1000),
    id_adjunto int,
    
    primary key (id),
    foreign key (id_turno) references turnos(id),
    foreign key (id_campo) references campos(id)
);


select * from campos;

