/*
-- Query: SELECT * FROM rehabilitar_test.area
LIMIT 0, 1000

-- Date: 2023-11-18 09:56
*/
CREATE TABLE `area` (
  `id` int NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `consultorio` int DEFAULT NULL,
  PRIMARY KEY (`id`)
);
INSERT INTO `area` (`id`,`Descripcion`,`Consultorio`) VALUES (0,'AREA SECRETARIAS',0);
INSERT INTO `area` (`id`,`Descripcion`,`Consultorio`) VALUES (1,'CARDIOLOGIA',1);
INSERT INTO `area` (`id`,`Descripcion`,`Consultorio`) VALUES (2,'CLINICO',2);
INSERT INTO `area` (`id`,`Descripcion`,`Consultorio`) VALUES (3,'FONOAUDIOLOGIA',3);
INSERT INTO `area` (`id`,`Descripcion`,`Consultorio`) VALUES (4,'LABORATORIO',4);
INSERT INTO `area` (`id`,`Descripcion`,`Consultorio`) VALUES (5,'NEUMONOLOGIA',5);
INSERT INTO `area` (`id`,`Descripcion`,`Consultorio`) VALUES (6,'ODONTOLOGIA',6);
INSERT INTO `area` (`id`,`Descripcion`,`Consultorio`) VALUES (7,'OFTALMOLOGIA',7);
INSERT INTO `area` (`id`,`Descripcion`,`Consultorio`) VALUES (8,'PSICOLOGIA',8);
INSERT INTO `area` (`id`,`Descripcion`,`Consultorio`) VALUES (9,'RX',9);
INSERT INTO `area` (`id`,`Descripcion`,`Consultorio`) VALUES (10,'NEUROLOGIA',10);
