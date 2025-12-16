CREATE DATABASE appdb;

\c appdb;

CREATE TABLE test (
  id SERIAL PRIMARY KEY,
  message TEXT
);

INSERT INTO test (message) VALUES ('Base de datos funcionando');
