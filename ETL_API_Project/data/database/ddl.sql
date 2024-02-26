
CREATE TABLE conditions_ae (
	id INTEGER NOT NULL, 
	impairment_category VARCHAR(100), 
	impairment VARCHAR(100), 
	feature_type VARCHAR(100), 
	feature VARCHAR(100), 
	icd_code VARCHAR(100), 
	report_date DATE, 
	clinician_specialty VARCHAR(100), 
	value VARCHAR(100), 
	person_id INTEGER, 
	PRIMARY KEY (id)
)

;


CREATE TABLE labs_ae (
	id INTEGER NOT NULL, 
	impairment_category VARCHAR(100), 
	impairment VARCHAR(100), 
	feature_type VARCHAR(100), 
	loinc VARCHAR(100), 
	feature_date DATE, 
	feature VARCHAR(100), 
	value FLOAT, 
	normal_range_of_value VARCHAR(100), 
	result_evaluation_or_flag VARCHAR(100), 
	person_id INTEGER, 
	PRIMARY KEY (id)
)

;


CREATE TABLE lifestyle_ae (
	id INTEGER NOT NULL, 
	impairment_category VARCHAR(100), 
	impairment VARCHAR(100), 
	lifestyle_category VARCHAR(100), 
	feature_type VARCHAR(100), 
	feature VARCHAR(100), 
	report_date DATE, 
	clinician_specialty VARCHAR(100), 
	value VARCHAR(100), 
	secondary_value VARCHAR(100), 
	person_id INTEGER, 
	PRIMARY KEY (id)
)

;


CREATE TABLE rx_ae (
	id INTEGER NOT NULL, 
	impairment_category VARCHAR(100), 
	impairment VARCHAR(100), 
	din FLOAT, 
	rx_name VARCHAR(100), 
	rx_type VARCHAR(100), 
	start_date DATE, 
	end_date DATE, 
	rx_date DATE, 
	rx_norm FLOAT, 
	person_id INTEGER, 
	PRIMARY KEY (id)
)

;


CREATE TABLE tests_ae (
	id INTEGER NOT NULL, 
	impairment_category VARCHAR(100), 
	impairment VARCHAR(100), 
	feature_type VARCHAR(100), 
	feature VARCHAR(100), 
	icd_code VARCHAR(100), 
	report_date DATE, 
	value VARCHAR(100), 
	person_id INTEGER, 
	PRIMARY KEY (id)
)

;

