CREATE TABLE
     turnos (
          id int,
          paciente_id int,
          empresa_id int,
          fecha datetime,
          tipo_examen varchar(50),
          file_token varchar(50),
          created_at datetime,
          last_modification datetime,
          confirmado BOOLEAN,
          deleted BOOLEAN
     );