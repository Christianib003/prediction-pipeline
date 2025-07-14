CREATE TABLE plants (
    plant_id SERIAL PRIMARY KEY,
    plant_name VARCHAR(100) UNIQUE NOT NULL
);


CREATE TABLE diseases (
    disease_id SERIAL PRIMARY KEY,
    disease_name VARCHAR(100) UNIQUE NOT NULL
);


CREATE TABLE image_metadata (
    image_id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    image_path VARCHAR(512) NOT NULL,
    date_added TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    plant_id INT NOT NULL REFERENCES plants(plant_id),
    disease_id INT NOT NULL REFERENCES diseases(disease_id)
);


CREATE TABLE image_metadata_audit (
    audit_id SERIAL PRIMARY KEY,
    image_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    image_path VARCHAR(512) NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);