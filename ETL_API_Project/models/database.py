""" This Module will handle the table creation and mapping for the ORM and data storage layer """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    """Create a base model for abstraction of database models"""

    __abstract__ = True

    def to_dict(self):
        """for each table created, will generate a dctionary of the columns and their data types for use in generating DDL's"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Conditions(BaseModel):
    __tablename__ = "conditions_ae"
    id = db.Column(db.Integer, primary_key=True)
    impairment_category = db.Column(db.String(100))
    impairment = db.Column(db.String(100))
    feature_type = db.Column(db.String(100))
    feature = db.Column(db.String(100))
    icd_code = db.Column(db.String(100))
    report_date = db.Column(db.Date)
    clinician_specialty = db.Column(db.String(100))
    value = db.Column(db.String(100))
    person_id = db.Column(db.Integer, nullable=False)


class Labs(BaseModel):
    __tablename__ = "labs_ae"
    id = db.Column(db.Integer, primary_key=True)
    impairment_category = db.Column(db.String(100))
    impairment = db.Column(db.String(100))
    feature_type = db.Column(db.String(100))
    loinc = db.Column(db.String(100))
    feature_date = db.Column(db.Date)
    feature = db.Column(db.String(100))
    value = db.Column(db.Float)
    normal_range_of_value = db.Column(db.String(100))
    result_evaluation_or_flag = db.Column(db.String(100))
    person_id = db.Column(db.Integer, nullable=False)

    def get_latest_hgb_level(self):
        """This function will query the Labs table looking for the most recent HgB readings and return those levels"""
        latest_record = (
            Labs.query.filter_by(feature="Hemoglobin (HGB)", person_id=self.person_id)
            .order_by(Labs.feature_date.desc())
            .first()
        )
        return latest_record.value if latest_record else None


class Lifestyle(BaseModel):
    __tablename__ = "lifestyle_ae"
    id = db.Column(db.Integer, primary_key=True)
    impairment_category = db.Column(db.String(100))
    impairment = db.Column(db.String(100))
    lifestyle_category = db.Column(db.String(100))
    feature_type = db.Column(db.String(100))
    feature = db.Column(db.String(100))
    report_date = db.Column(db.Date)
    clinician_specialty = db.Column(db.String(100))
    value = db.Column(db.String(100))
    secondary_value = db.Column(db.String(100), default="Null")
    person_id = db.Column(db.Integer, nullable=False)


class Rx(BaseModel):
    __tablename__ = "rx_ae"
    id = db.Column(db.Integer, primary_key=True)
    impairment_category = db.Column(db.String(100))
    impairment = db.Column(db.String(100))
    din = db.Column(db.Float)
    rx_name = db.Column(db.String(100))
    rx_type = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    rx_date = db.Column(db.Date)
    rx_norm = db.Column(db.Float)
    person_id = db.Column(db.Integer, nullable=False)

    def is_prescribed_alpha_blockers(self):
        """This function will identify if a person has been prescribed Alpha Blockers and return a boolean value"""
        alpha_blockers = (
            self.query.filter_by(rx_type="Alpha Blockers", person_id=self.person_id)
            .where(not Rx.end_date)
            .order_by(Rx.start_date.desc())
        ) is not None
        return alpha_blockers


class Tests(BaseModel):
    __tablename__ = "tests_ae"
    id = db.Column(db.Integer, primary_key=True)
    impairment_category = db.Column(db.String(100))
    impairment = db.Column(db.String(100))
    feature_type = db.Column(db.String(100))
    feature = db.Column(db.String(100))
    icd_code = db.Column(db.String(100))
    report_date = db.Column(db.Date)
    value = db.Column(db.String(100))
    person_id = db.Column(db.Integer, nullable=False)
