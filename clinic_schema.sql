-- SQLite schema is created automatically. Example SQL for Postgres migration:

CREATE TABLE patients (
  id VARCHAR PRIMARY KEY,
  name VARCHAR,
  phone VARCHAR,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE appointments (
  id VARCHAR PRIMARY KEY,
  patient_name VARCHAR,
  patient_phone VARCHAR,
  doctor VARCHAR,
  scheduled_for TIMESTAMP,
  status VARCHAR,
  created_at TIMESTAMP DEFAULT now()
);
