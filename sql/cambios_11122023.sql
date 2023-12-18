use rehabilitar_testing;

delete from campos where 1;


SET foreign_key_checks = 0;
drop table campos;

create table campos(
	id int auto_increment,
    id_area int not null,
    name varchar(100),
    label varchar(100),
    type varchar(100),
    options varchar(100),
    default_value varchar(100),
    form_orden int,
    
    primary key (id)
);

drop table campos_informacion;
create table campos_informacion(
	id int auto_increment,
    id_campo int,
    id_turno int,
    value varchar(150),
    id_adjunto int,
    
    primary key (id),
    foreign key (id_turno) references turnos(id),
    foreign key (id_campo) references campos(id)
);


INSERT INTO campos (id_area, name, label, type) VALUES (2, 'EXAMEN CLINICO', '', 'titulo');

select * from campos;

