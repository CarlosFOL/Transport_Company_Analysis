/*CREATE A SURROGATE KEY WHEN A NEW RECORD IS INSERTED*/

CREATE FUNCTION gen_seq(
	num INTEGER
	)
	/*
	Calculate the length of the zero padding
	according to the number of digits of the number.
	*/
	RETURNS VARCHAR(5) AS $$
		DECLARE
			len INTEGER;
			padding VARCHAR(5);
		BEGIN
			len := floor( log(10, num) ) + 1;
			padding := LPAD(num::TEXT, 5, '0');	
			RETURN padding;
		END; 
		$$ LANGUAGE plpgsql;


/*TRIP*/
CREATE SEQUENCE prefix_cod START WITH 1; 

CREATE FUNCTION gen_trip_cod()
	RETURNS TRIGGER AS $$
		DECLARE
			num INTEGER;
		BEGIN
			num := NEXTVAL("prefix_cod");
			NEW.trip_cod := "TRIP" || gen_seq(num);
			RETURN NEW;
		END;
	$$ LANGUAGE plpgsql;


/*TECHNICAL INSPECTION*/
CREATE SEQUENCE tech_cod START WITH 1;

CREATE FUNCTION gen_tech_cod()
	RETURNS TRIGGER AS $$
		DECLARE
			num INTEGER;
		BEGIN
			num := NEXTVAL("tech_cod");
			NEW.cod := SUBSTRING(NEW.chassis from 1 to 4) || gen_trip_cod(num);
			RETURN NEW;
		END;
	$$ LANGUAGE plpgsql;


/*PURPOSE*/
CREATE SEQUENCE purp_cod START WITH 1;

CREATE FUNCTION gen_purp_code()
	RETURNS TRIGGER AS $$
		DECLARE
			num INTEGER;
		BEGIN
			NEW.cod := "PURP" || gen_seq(num)
		END;
	$$ LANGUAGE plpsql;