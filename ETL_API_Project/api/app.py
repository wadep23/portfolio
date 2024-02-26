"""

This is the Server layer of the application and contains the API endpoints and logic.
In the future I would like to extract out the business logic and routes into seperate modules 
for scalability and readability.

"""

import os

from datetime import datetime, timedelta
from sqlalchemy import func
from flask import Flask, jsonify

from models.database import db, Conditions, Labs, Lifestyle, Rx, Tests

database_dir = os.path.join(os.getcwd(), "data/database")
DATABASE_FILE = "ae.db"
database_path = os.path.join(database_dir, DATABASE_FILE)

if not os.path.isdir(database_dir):
    os.makedirs(database_dir)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
db.init_app(app)


@app.route("/conditions", methods=["GET"])
def get_conditions():
    try:
        conditions_query = Conditions.query.all()
        conditions_list = [item.to_dict() for item in conditions_query]
        return jsonify(conditions_list), 200
    except Exception as e:
        app.logger.error(f"Error retrieving conditions: {e}")
        return jsonify({"error": "Error retrieving conditions data"}), 500


@app.route("/labs", methods=["GET"])
def get_labs():
    try:
        labs_query = Labs.query.all()
        labs_list = [item.to_dict() for item in labs_query]
        return jsonify(labs_list), 200
    except Exception as e:
        app.logger.error(f"Error retrieving labs: {e}")
        return jsonify({"error": "Error retrieving labs data"}), 500


@app.route("/lifestyle", methods=["GET"])
def get_lifestyle():
    try:
        lifestyle_query = Lifestyle.query.all()
        lifestyle_list = [item.to_dict() for item in lifestyle_query]
        return jsonify(lifestyle_list), 200
    except Exception as e:
        app.logger.error(f"Error retrieving lifestyle data: {e}")
        return jsonify({"error": "Error retrieving lifestyle data"}), 500


@app.route("/rx", methods=["GET"])
def get_rx():
    try:
        rx_query = Rx.query.all()
        rx_list = [item.to_dict() for item in rx_query]
        return jsonify(rx_list), 200
    except Exception as e:
        app.logger.error(f"Error retrieving prescriptions: {e}")
        return jsonify({"error": "Error retrieving prescriptions data"}), 500


@app.route("/rx/<int:person_id>", methods=["GET"])
def get_rx_by_id(person_id):
    try:
        rx_query = Rx.query.filter_by(person_id=person_id).all()

        rx_list = [
            {
                "id": rx.id,
                "rx_name": rx.rx_name,
                "rx_type": rx.rx_type,
                "alpha_blocker": rx.alpha_blocker,
            }
            for rx in rx_query
        ]

        return jsonify(rx_list), 200
    except Exception as e:
        app.logger.error(f"Error retrieving prescriptions: {e}")
        return jsonify({"error": "Error retrieving prescriptions data"}), 500


@app.route("/tests", methods=["GET"])
def get_tests():
    try:
        tests_query = Tests.query.all()
        tests_list = [item.to_dict() for item in tests_query]
        return jsonify(tests_list), 200
    except Exception as e:
        app.logger.error(f"Error retrieving tests data: {e}")
        return jsonify({"error": "Error retrieving tests data"}), 500


@app.route("/person/<int:person_id>", methods=["GET"])
def get_person_data(person_id):
    try:
        conditions = Conditions.query.filter_by(person_id=person_id).all()
        conditions_list = [item.to_dict() for item in conditions]

        labs = Labs.query.filter_by(person_id=person_id).all()
        labs_list = [item.to_dict() for item in labs]

        lifestyle = Lifestyle.query.filter_by(person_id=person_id).all()
        lifestyle_list = [item.to_dict() for item in lifestyle]

        prescriptions = Rx.query.filter_by(person_id=person_id).all()
        prescriptions_list = [item.to_dict() for item in prescriptions]

        tests = Tests.query.filter_by(person_id=person_id).all()
        tests_list = [item.to_dict() for item in tests]

        person_data = {
            "person_id": person_id,
            "data": {
                "conditions": conditions_list,
                "labs": labs_list,
                "lifestyle": lifestyle_list,
                "prescriptions": prescriptions_list,
                "tests": tests_list,
            },
        }

        return jsonify(person_data), 200

    except Exception as e:
        app.logger.error(f"Error retrieving data for person ID {person_id}: {e}")
        return (
            jsonify({"error": f"Error retrieving data for person ID {person_id}"}),
            500,
        )


@app.route("/person/<int:person_id>/details", methods=["GET"])
def get_person_details(person_id):
    try:
        rx_query = Rx.query.filter_by(person_id=person_id).first()
        if rx_query:
            is_prescribed = rx_query.is_prescribed_alpha_blockers()

        labs_query = Labs.query.filter_by(person_id=person_id).first()
        if labs_query:
            recent_labs = labs_query.get_latest_hgb_level()

        six_months_ago = datetime.today() - timedelta(days=182.5)

        conditions_count = (
            db.session.query(func.count(Conditions.id))
            .filter(
                Conditions.person_id == person_id,
                Conditions.report_date >= six_months_ago,
            )
            .scalar()
        )

        labs_count = (
            db.session.query(func.count(Labs.id))
            .filter(Labs.person_id == person_id, Labs.feature_date >= six_months_ago)
            .scalar()
        )

        lifestyle_count = (
            db.session.query(func.count(Lifestyle.id))
            .filter(
                Lifestyle.person_id == person_id,
                Lifestyle.report_date >= six_months_ago,
            )
            .scalar()
        )

        rx_count = (
            db.session.query(func.count(Rx.id))
            .filter(Rx.person_id == person_id, Rx.rx_date >= six_months_ago)
            .scalar()
        )

        tests_count = (
            db.session.query(func.count(Tests.id))
            .filter(Tests.person_id == person_id, Tests.report_date >= six_months_ago)
            .scalar()
        )

        number_of_visits = sum(
            [conditions_count, labs_count, lifestyle_count, rx_count, tests_count]
        )

        person_data = {
            "person_id": person_id,
            "data": {
                "Alpha_Blockers": is_prescribed,
                "HgB_Levels": recent_labs,
                "Number_of_Visits": number_of_visits,
            },
        }

        return jsonify(person_data), 200

    except Exception as e:
        app.logger.error(f"Error retrieving data for person ID {person_id}: {e}")
        return (
            jsonify({"error": f"Error retrieving data for person ID {person_id}"}),
            500,
        )


if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()
        app.run(debug=True)
    except Exception as e:
        app.logger.error(f"Failed to start the Flask application: {e}")
