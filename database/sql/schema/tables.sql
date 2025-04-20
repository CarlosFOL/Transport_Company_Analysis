/*-----------------------------------------------------------------------------------------------------------------*/
/*POINT*/
/*USE THE NOMATIM OSM API TO GET THE COORDINATES OF A POINT*/
CREATE TABLE point(
	num SERIAL,
	name VARCHAR(13) NOT NULL,
	street VARCHAR(100) NOT NULL,
	number NUMERIC(10) NOT NULL,
	council VARCHAR(100) NOT NULL,
	postal_code VARCHAR(10) NOT NULL,
	country VARCHAR(9) NOT NULL,
	lat NUMERIC(3, 6) NOT NULL,
	cod NUMERIC(3, 6) NOT NULL, 

	CONSTRAINT pk_point PRIMARY KEY (num)
)

/*ROUTE*/
CREATE TABLE route(
	cod SERIAL,
	distance NUMERIC(6, 3) NOT NULL, /*km*/
	origin NUMERIC NOT NULL,
	destinantion NUMERIC NOT NULL,

	CONSTRAINT pk_route PRIMARY KEY (cod),
	CONSTRAINT fk_origin FOREIGN KEY (origin) REFERENCES point(num),
	CONSTRAINT fk_dest FOREIGN KEY (destination) REFERENCES point(num)
)

/*-----------------------------------------------------------------------------------------------------------------*/
/*CUSTOMER*/
CREATE TABLE customer(
	tin VARCHAR(11),
	name_cust VARCHAR (20) NOT NULL,

	CONSTRAINT pk_customer PRIMARY KEY (tin)
)

/*-----------------------------------------------------------------------------------------------------------------*/
/*TRIPS*/

CREATE TABLE type_purp(
	cod SERIAL,
	name VARCHAR(100) NOT NULL,
)

CREATE TABLE purpose(
	cod VARCHAR(9),
	name VARCHAR(100) NOT NULL,
	descr VARCHAR(255),
	cod_type NUMERIC NOT NULL,

	CONSTRAINT pk_cod PRIMARY KEY (cod),
	CONSTRAINT fk_type FOREIGN KEY (cod_type) REFERENCES type_purp(cod)
)

CREATE TABLE trip(
	cod VARCHAR(9),
	rem_guide VARCHAR(10) NOT NULL, /*It has to be inserted manually*/
	status VARCHAR(14) DEFAULT "PROGRAMMED", /*Default status when a trip is recorded*/
	start_date TIMESTAMP NOT NULL,
	end_date TIMESTAMP NOT NULL,
	cod_purp VARCHAR(9) NOT NULL,
	cod_route NUMERIC NOT NULL,
	customer VARCHAR(11) NOT NULL,

	CONSTRAINT pk_trip PRIMARY KEY (cod),
	CONSTRAINT fk_purp FOREIGN KEY (cod_purp) REFERENCES purpose(cod),
	CONSTRAINT fk_route FOREIGN KEY (cod_route) REFERENCES route(cod),
	CONSTRAINT fk_cust FOREIGN KEY (customer) REFERENCES customer(tin)
)

/*-----------------------------------------------------------------------------------------------------------------*/
/*VEHICLE*/
CREATE TABLE vehicle(
	chassis VARCHAR(17),
	is_new BOOLEAN NOT NULL,
	color VARCHAR(10) NOT NULL,
	family VARCHAR(10) NOT NULL,
	brand VARCHAR(20) NOT NULL,
	model VARCHAR(20) NOT NULL,
	owner VARCHAR(11) DEFAULT "TC", /*TC -> Vehicles from transport company*/ 
	
	CONSTRAINT valid_fam CHECK ( family_veh in ("TRUCK", "AUTOMOBILE", "VAN", "BUS") ),
	CONSTRAINT pk_vehicle PRIMARY KEY (chassis),
	CONSTRAINT owner_vehicle FOREIGN KEY (owner) REFERENCES customer(tin)
)

/*TECH. INSPECTION*/
CREATE TABLE tech_insp(
	cod VARCHAR(9)
	issue_date TIMESTAMP NOT NULL,
	exp_date TIMESTAMP NOT NULL,
	chassis VARCHAR(17) NOT NULL,
	
	CONSTRAINT pk_tech_insp PRIMARY KEY (cod),
	CONSTRAINT fk_vehicle FOREIGN KEY (chassis) REFERENCES vehicle(chassis)
)

/*-----------------------------------------------------------------------------------------------------------------*/
/*DRIVER*/
CREATE TABLE driver(
	id VARCHAR(9) NOT NULL,
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
	id VARCHAR(9) NOT NULL,

	CONSTRAINT valid_lic_type CHECK ( type_lic IN ("A1", "A", "B", "C1", "C", "D1", 
													"D", "BE", "C1E", "CE", "D1E", "DE") ),
	CONSTRAINT pk_license PRIMARY KEY (id_lic),
	CONSTRAINT fk_driver FOREIGN KEY (id) REFERENCES driver(id)
)

/*CONTROL*/
CREATE TABLE control(
	id_driver VARCHAR(9),
	arr_date TIMESTAMP,
	dept_date TIMESTAMP NOT NULL,
	chassis VARCHAR(17) NOT NULL,
	codtrip VARCHAR(9) NOT NULL,

	CONSTRAINT pk_control PRIMARY KEY (id_driver, arr_date),
	CONSTRAINT fk_driver_ctl FOREIGN KEY (id_driver) REFERENCES driver(id),
	CONSTRAINT fk_veh_ctl FOREIGN KEY (chassis) REFERENCES vehicle(chassis)
	CONSTRAINT fk_trip_ctl FOREIGN KEY (codtrip) REFERENCES trip(cod)
)

/*-----------------------------------------------------------------------------------------------------------------*/
/*PARTICIPATES*/
CREATE TABLE participate(
	id_driver VARCHAR(9),
	codtrip VARCHAR(9),

	CONSTRAINT pk_part PRIMARY KEY (id_driver, codtrip),
	CONSTRAINT fk_id_part FOREIGN KEY (id_driver) REFERENCES driver(id),
	CONSTRAINT fk_codtrip_part FOREIGN KEY (codtrip) REFERENCES trip(cod)
)

/*-----------------------------------------------------------------------------------------------------------------*/
/*COSTS*/
CREATE TABLE type_cost(
	cod VARCHAR(9),
	name VARCHAR(100) NOT NULL,

	CONSTRAINT pk_tcost PRIMARY KEY (cod)
)

CREATE TABLE extra_cost(
	cod_tcost VARCHAR(9),
	num NUMERIC,
	name VARCHAR(100) NOT NULL,
	descr VARCHAR(255),

	CONSTRAINT pk_ex_cost PRIMARY KEY (cod_tcost, num),
	CONSTRAINT fk_tcost FOREIGN KEY (cod_tcost) REFERENCES type_cost(cod)
)

/*-----------------------------------------------------------------------------------------------------------------*/
/*Cost Attribution*/

CREATE TABLE cost_attribution(
	cod_tcost VARCHAR(9),
	cod_trip VARCHAR(9),
	id_driver VARCHAR(9),
	price NUMERIC,

	CONSTRAINT pk_cost_attr PRIMARY KEY (cod_tcost, cod_trip, id_driver),
	CONSTRAINT fk_extra_cost FOREIGN KEY (cod_tcost) REFERENCES extra_cost(cod_tcost),
	CONSTRAINT fk_trip_cost FOREIGN KEY (cod_trip) REFERENCES trip(cod),
	CONSTRAINT fk_driver_cost FOREIGN KEY (id_driver) REFERENCES driver(id)
)