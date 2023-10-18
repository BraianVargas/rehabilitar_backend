
create table ddjj(
	id INT PRIMARY KEY AUTO_INCREMENT,
    accidente_transito BOOLEAN,
    fuma BOOLEAN,
    d_fuma INT,
    deporte BOOLEAN,
    d_deporte VARCHAR(140),
    alcohol BOOLEAN,
    d_alcohol VARCHAR(140),
    duerme BOOLEAN,
    d_duerme INT,
    vision BOOLEAN,
    audio BOOLEAN,
    dolor_cabeza BOOLEAN,
    dolor_torax BOOLEAN,
    taquicardia BOOLEAN,
    hipertension BOOLEAN,
    marcapaso BOOLEAN,
    falta_aire BOOLEAN,
    hepatitis BOOLEAN,
    alergia BOOLEAN,
    cancer BOOLEAN,
    perdida_peso BOOLEAN,
    diabetes BOOLEAN,
    diabetes_2 BOOLEAN,
    psiquiatrico BOOLEAN,
    epilepsia BOOLEAN,
    dolor_cintura BOOLEAN,
    dolor_espalda BOOLEAN,
    dolor_piernas BOOLEAN,
    fracturas BOOLEAN,
    operaciones BOOLEAN,
    apendicitis BOOLEAN,
    vesicula BOOLEAN,
    varices BOOLEAN,
    tumor BOOLEAN,
    hernias BOOLEAN,
    corazon BOOLEAN,
    rodillas BOOLEAN,
    tobillos BOOLEAN,
    hombros BOOLEAN,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);