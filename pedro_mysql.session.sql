CREATE DATABASE IF NOT EXISTS escola;

USE escola;

CREATE TABLE IF NOT EXISTS alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    idade INT,
    curso VARCHAR(100)
);

INSERT INTO alunos (nome, idade, curso)
VALUES ('Pedro', 20, 'ADS');


SELECT * FROM alunos;
