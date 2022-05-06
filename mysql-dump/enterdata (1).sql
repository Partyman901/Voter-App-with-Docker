CREATE DATABASE IF NOT EXISTS enterdata;
USE enterdata;
CREATE TABLE IF NOT EXISTS enterdata (
	id int auto_increment not null,
    mac int not null,
    windows int not null,
	constraint pk_enterdata primary key (id)
);
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Passw0rd!';