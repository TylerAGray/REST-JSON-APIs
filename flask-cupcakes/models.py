from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Default image URL for cupcakes that don't have an image provided
DEFAULT_IMAGE = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    """Cupcake model representing cupcakes in the database."""

    __tablename__ = "cupcakes"  # Name of the table in the database

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier for each cupcake
    flavor = db.Column(db.Text, nullable=False)  # Flavor of the cupcake
    size = db.Column(db.Text, nullable=False)  # Size of the cupcake
    rating = db.Column(db.Float, nullable=False)  # Rating of the cupcake (e.g., out of 5 stars)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE)  # URL of the cupcake's image

    def to_dict(self):
        """Serialize cupcake to a dictionary of cupcake information."""
        return {
            "id": self.id,
            "flavor": self.flavor,
            "rating": self.rating,
            "size": self.size,
            "image": self.image,
        }

def connect_db(app):
    """Connect the Flask app to the database."""
    db.app = app
    db.init_app(app)
