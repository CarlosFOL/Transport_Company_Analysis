/*SURROGATE KEYS*/

/*1) SURROGATE KEY FOR TABLE TRIPS*/
CREATE TRIGGER trip_cod
	BEFORE INSERT ON trip /*When inserting a new record on TRIPS table*/
	FOR EACH ROW /*Call this trigger for each modified row*/
		WHEN (NEW.cod is NULL)
EXECUTE FUNCTION gen_trip_cod();

/*2) SURROGATE KEY FOR TECHNICAL INSPECTION*/
CREATE TRIGGER tech_cod
	BEFORE INSERT ON tech_insp
	FOR EACH ROW 
		WHEN NEW.cod is NULL
EXECUTE FUNCTION gen_tech_cod();

/*3) SURROGATE KEY FOR PURPOSE*/
CREATE TRIGGER purp_cod
	BEFORE INSERT ON purpose
	FOR EACH ROW
		WHEN NEW.cod is NULL
EXECUTE FUNCTION gen_purp_code();

/*----------------------------------------------------------------------------------------*/
