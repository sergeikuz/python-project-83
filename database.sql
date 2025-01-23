DROP TABLE if exists urls CASCADE;


CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar UNIQUE NOT NULL,
    created_at date
);
