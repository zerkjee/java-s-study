CREATE DATABASE teste;

USE teste;

CREATE TABLE exemplo (
  id INT IDENTITY(1,1) PRIMARY KEY,
  nome VARCHAR(100)
);

INSERT INTO exemplo (nome) VALUES ('Teste 1');

SELECT * FROM exemplo;
