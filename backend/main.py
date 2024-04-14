from flask import request, jsonify
from config import app, db
from models import Contact, PhoneNumber  # Imported PhoneNumber model


@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = [contact.to_json() for contact in contacts]
    return jsonify({"contacts": json_contacts})


@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return jsonify({"message": "You must include a first name, last name and email"}), 400

    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    db.session.add(new_contact)
    db.session.commit()

    return jsonify({"message": "Contact created!", "contact_id": new_contact.id}), 201


@app.route("/update_contact/<int:contact_id>", methods=["PATCH"])
def update_contact(contact_id):
    contact = Contact.query.get(contact_id)

    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "Contact updated."}), 200


@app.route("/delete_contact/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)

    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "Contact deleted!"}), 200


@app.route("/add_phone_number/<int:contact_id>", methods=["POST"])
def add_phone_number(contact_id):
    contact = Contact.query.get(contact_id)

    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    number = request.json.get("number")
    if not number:
        return jsonify({"message": "You must include a phone number"}), 400

    new_phone_number = PhoneNumber(number=number, contact_id=contact_id)  # Creating a new PhoneNumber instance
    db.session.add(new_phone_number)  # Adding the new phone number to the session
    db.session.commit()  # Committing the changes to the database

    return jsonify({"message": "Phone number added to contact!", "phone_number_id": new_phone_number.id}), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5002)
