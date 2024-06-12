create database CollectionStep;

use CollectionStep;


create table usuarios(
	id_user int primary key auto_increment not null,
    name_user varchar(50) not null,
    mail varchar(50) not null,
    passW  varchar(20) not null
);

CREATE TABLE produtos (
    rastreio_pedido varchar(50),
    id_produto int PRIMARY KEY auto_increment not null,
    datareceb_prod varchar(20),
    tipo_prod varchar(50),
    desc_prod varchar(255)
);

INSERT INTO usuarios (name_user, mail, passW) VALUES
('Caio', 'caiomirandab@gmail.com', 'cmb110205');

