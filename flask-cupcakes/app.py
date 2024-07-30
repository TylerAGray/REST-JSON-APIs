from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

# Configuration for the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications
app.config['SECRET_KEY'] = "oh-so-secret"  # Secret key for session management

# Connect the app with the database
connect_db(app)

@app.route("/")
def root():
    """Render homepage."""
    return render_template("index.html")

@app.route("/api/cupcakes")
def list_cupcakes():
    """Return all cupcakes in the system.

    This endpoint returns a JSON object containing a list of all cupcakes.
    JSON response structure:
        {cupcakes: [{id, flavor, rating, size, image}, ...]}
    """
    # Retrieve all cupcakes from the database and convert them to dictionaries
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add a new cupcake, and return data about the new cupcake.

    This endpoint accepts JSON data to create a new cupcake and returns the created cupcake's data.
    JSON request body should include:
        {flavor, rating, size, image}

    JSON response structure:
        {cupcake: {id, flavor, rating, size, image}}
    """
    # Extract data from the request JSON
    data = request.json

    # Create a new Cupcake instance with the provided data
    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None  # Use None if image is not provided
    )

    # Add and commit the new cupcake to the database
    db.session.add(cupcake)
    db.session.commit()

    # Return the created cupcake data with a 201 status code
    return jsonify(cupcake=cupcake.to_dict()), 201

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Return data on a specific cupcake.

    This endpoint returns JSON data for a specific cupcake identified by its ID.
    JSON response structure:
        {cupcake: {id, flavor, rating, size, image}}
    """
    # Retrieve the cupcake by ID or return a 404 if not found
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake with data from the request. Return updated data.

    This endpoint updates an existing cupcake's data with the provided JSON data.
    JSON request body should include:
        {flavor, rating, size, image}

    JSON response structure:
        {cupcake: {id, flavor, rating, size, image}}
    """
    # Extract data from the request JSON
    data = request.json

    # Retrieve the cupcake by ID or return a 404 if not found
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # Update the cupcake attributes with the provided data
    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    # Commit the changes to the database
    db.session.add(cupcake)
    db.session.commit()

    # Return the updated cupcake data
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete a cupcake and return a confirmation message.

    This endpoint deletes the cupcake with the specified ID and returns a confirmation message.
    JSON response structure:
        {message: "Deleted"}
    """
    # Retrieve the cupcake by ID or return a 404 if not found
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # Delete the cupcake from the database and commit the changes
    db.session.delete(cupcake)
    db.session.commit()

    # Return a confirmation message
    return jsonify(message="Deleted")
