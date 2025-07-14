-- Stored Procedure: A function to add a new image record by name, not ID.
CREATE OR REPLACE PROCEDURE add_new_image(
    p_filename VARCHAR,
    p_image_path VARCHAR,
    p_plant_name VARCHAR,
    p_disease_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_plant_id INT;
    v_disease_id INT;
BEGIN
    -- Find the ID for the given plant name, or create it if it doesn't exist
    INSERT INTO plants (plant_name) VALUES (p_plant_name)
    ON CONFLICT (plant_name) DO NOTHING;
    SELECT plant_id INTO v_plant_id FROM plants WHERE plant_name = p_plant_name;

    -- Find the ID for the given disease name, or create it if it doesn't exist
    INSERT INTO diseases (disease_name) VALUES (p_disease_name)
    ON CONFLICT (disease_name) DO NOTHING;
    SELECT disease_id INTO v_disease_id FROM diseases WHERE disease_name = p_disease_name;

    -- Insert the new record into the metadata table using the IDs
    INSERT INTO image_metadata (filename, image_path, plant_id, disease_id)
    VALUES (p_filename, p_image_path, v_plant_id, v_disease_id);
END;
$$;


-- Trigger Function: This function logs a deleted record to the audit table.
CREATE OR REPLACE FUNCTION log_deleted_image()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert the data from the deleted row (OLD) into the audit table
    INSERT INTO image_metadata_audit (image_id, filename, image_path)
    VALUES (OLD.image_id, OLD.filename, OLD.image_path);
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger: This attaches the function to the image_metadata table.
-- It will fire AFTER any row is deleted.
CREATE TRIGGER after_image_delete_log
AFTER DELETE ON image_metadata
FOR EACH ROW
EXECUTE FUNCTION log_deleted_image();