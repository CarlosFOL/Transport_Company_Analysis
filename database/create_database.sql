
/*TRIPS*/
CREATE TABLE trip(
	cod VARCHAR(9),
	rem_guide VARCHAR(10) NOT NULL, /*It has to be inserted manually*/
	status VARCHAR(14) NOT NULL DEFAULT "PROGRAMMED", /*Default status when a trip is recorded*/
	start_date TIMESTAMP NOT NULL,
	end_date TIMESTAMP NOT NULL,

	CONSTRAINT pk_trip PRIMARY KEY (cod);
)
/*Set the trigger to update the surrogate key when a new record is inserting*/
CREATE SEQUENCE prefix_cod START WITH 1; /*Sequence generator*/

CREATE FUNCTION gen_trip_cod()
	RETURNS TRIGGER AS $$
		BEGIN /*Set function body*/
			NEW.trip_cod := "TRIP" || LPAD( NEXTVAL("prefix_cod")::TEXT, 4, '0'); /*LPAD -> Left padding*/
			RETURN NEW;
		END;
	$$ LANGUAGE plpgsql;

CREATE TRIGGER trip_cod
	BEFORE INSERT ON trip /*When inserting a new record on TRIPS table*/
	FOR EACH ROW /*Call this trigger for each modified row*/
		WHEN (NEW.cod is NULL)
EXECUTE FUNCTION gen_trip_cod();

/*-----------------------------------------------------------------------------------------------------------------*/
/*DRIVER*/
CREATE TABLE driver(
	dni VARCHAR(9) NOT NULL,
	first_name VARCHAR(20) NOT NULL,
	surname1 VARCHAR(20) NOT NULL,
	surname2 VARCHAR(20) NOT NULL,
	CONSTRAINT pk_driver PRIMARY KEY (driver)
)	


/*LICENSE*/
CREATE TABLE license(
	id_lic VARCHAR(8),
	issue_date TIMESTAMP NOT NULL,
	exp_date TIMESTAMP NOT NULL,
	type_lic VARCHAR NOT NULL,

	CONSTRAINT valid_lic_type CHECK ( type_lic IN ("A1", "A", "B", "C1", "C", "D1", 
													"D", "BE", "C1E", "CE", "D1E", "DE") ),
	CONSTRAINT pk_license PRIMARY KEY (id_lic)
)

/*-----------------------------------------------------------------------------------------------------------------*/
/*VEHICLE*/
CREATE TABLE vehicle(
	chassis VARCHAR(17),
	is_new BOOLEAN NOT NULL,
	color VARCHAR(10) NOT NULL,
	family_veh VARCHAR(10) NOT NULL,
	brand VARCHAR(20) NOT NULL,
	model VARCHAR(20) NOT NULL,
	
	CONSTRAINT valid_fam CHECK ( family_veh in ("TRUCK", "AUTOMOBILE", "VAN", "BUS") ),
	CONSTRAINT pk_vehicle PRIMARY KEY (chassis)
)

/*TECH. INSPECTION*/
CREATE TABLE tech_insp(
	cod VARCHAR(9)
	issue_date TIMESTAMP NOT NULL,
	exp_date TIMESTAMP NOT NULL,
	chassis VARCHAR(17) NOT NULL,
	
	CONSTRAINT pk_tech_insp PRIMARY KEY (cod)
	CONSTRAINT fk_vehicle FOREIGN KEY (chassis) REFERENCES vehicle(chassis)
)

CREATE SEQUENCE tech_cod START WITH 1;

CREATE FUNCTION gen_tech_cod()
	RETURNS TRIGGER AS $$
		BEGIN
			NEW.cod := SUBSTRING(NEW.chassis from 1 to 3) || LPAD(NEXTVAL("tech_cod")::TEXT, 4, 0)
			RETURN NEW;
		END;
	$$ LANGUAGE plpgsql;

CREATE TRIGGER tech_cod
	BEFORE INSERT ON tech_insp
	FOR EACH ROW 
		WHEN NEW.cod is NULL
EXECUTE FUNCTION;

