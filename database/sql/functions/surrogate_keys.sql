/*CREATE A SURROGATE KEY WHEN A NEW RECORD IS INSERTED*/

/*TRIP*/
CREATE SEQUENCE prefix_cod START WITH 1; 

CREATE FUNCTION gen_trip_cod()
	RETURNS TRIGGER AS $$
		BEGIN 
			NEW.trip_cod := "TRIP" || LPAD( NEXTVAL("prefix_cod")::TEXT, 4, '0');
			RETURN NEW;
		END;
	$$ LANGUAGE plpgsql;


/*TECHNICAL INSPECTION*/
CREATE SEQUENCE tech_cod START WITH 1;

CREATE FUNCTION gen_tech_cod()
	RETURNS TRIGGER AS $$
		BEGIN
			NEW.cod := SUBSTRING(NEW.chassis from 1 to 3) || LPAD(NEXTVAL("tech_cod")::TEXT, 4, 0)
			RETURN NEW;
		END;
	$$ LANGUAGE plpgsql;


/*PURPOSE*/
CREATE SEQUENCE purp_cod START WITH 1;

CREATE FUNCTION gen_purp_code()
	RETURNS TRIGGER AS $$
		BEGIN
			NEW.cod := "PURP" || LPAD( NEXTVAL("purp_cod")::TEXT, 3, 0 )
		END;
	$$ LANGUAGE plpsql;


CREATE FUNCTION gen_seq(
	num NUMERIC
	)
	RETURNS NUMERIC AS $$
		DECLARE
			len NUMERIC;
		BEGIN
			len := floor( log(num, 10) ) + 10
			RETURN 4 - len;
		END;
	$$ LANGUAGE plpgsql;
	
	




