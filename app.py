from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "items.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify(status="ok", database="connected"), 200
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

# API endpoint for items
@app.route("/api/items", methods=["GET", "POST"])
def items_api():
    if request.method == "POST":
        try:
            data = request.get_json(force=True)
            
            # Validate required fields
            if not data.get('name', '').strip():
                return jsonify(error="Name is required"), 400
            
            # Create new item
            new_item = Item(
                name=data.get('name', '').strip(),
                description=data.get('description', '').strip() or None
            )
            
            # Save to database
            db.session.add(new_item)
            db.session.commit()
            
            return jsonify(
                message="Item created successfully", 
                item=new_item.to_dict()
            ), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify(error=f"Database error: {str(e)}"), 500
    
    # GET request - return all items
    try:
        items = Item.query.order_by(Item.created_at.desc()).all()
        return jsonify(items=[item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify(error=f"Database error: {str(e)}"), 500

# Get statistics
@app.route("/api/stats", methods=["GET"])
def get_stats():
    try:
        total_items = Item.query.count()
        today_items = Item.query.filter(
            Item.created_at >= datetime.utcnow().date()
        ).count()
        
        return jsonify(
            total_items=total_items,
            items_today=today_items,
            database_status="connected"
        ), 200
    except Exception as e:
        return jsonify(error=f"Stats error: {str(e)}"), 500

# Frontend route
@app.route("/")
def home():
    return render_template('index.html')

# Initialize database using modern approach
def init_db():
    with app.app_context():
        db.create_all()
        print(" Database initialized successfully!")

if __name__ == "__main__":
    init_db()  # Create tables before running
    app.run(debug=True)
