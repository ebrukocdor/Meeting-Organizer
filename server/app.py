from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__, static_url_path='', static_folder='../client')
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'meetings.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Meeting(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    participants = db.Column(db.String(255), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return app.send_static_file("index.html")

# Add meeting
@app.route("/meetings", methods=["POST"])
def add_meeting():
    data = request.json
    new_meeting = Meeting(
        topic=data["topic"],
        date=data["date"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        participants=data["participants"]
    )
    db.session.add(new_meeting)
    db.session.commit()
    return jsonify({'message': 'Meeting created successfully'}), 201

# List all meetings
@app.route("/meetings", methods=["GET"])
def list_meetings():
    meetings = Meeting.query.all()
    meeting_list = []
    for meeting in meetings:
        meeting_data ={
            'id': meeting.id,
            'topic': meeting.topic,
            'date': meeting.date,
            'start_time': meeting.start_time,
            'end_time': meeting.end_time,
            'participants': meeting.participants          
        }
        meeting_list.append(meeting_data) 
    return jsonify(meeting_list)

# Get a spesific meeting
@app.route("/meetings/<int:id>", methods=["GET"])
def get_meeting(id):
    meeting = Meeting.query.get(id)
    if not meeting:
        abort(404, description="Meeting not found")
    
    meeting_data = {
        'id': meeting.id,
        'topic': meeting.topic,
        'date': meeting.date,
        'start_time': meeting.start_time,
        'end_time': meeting.end_time,
        'participants': meeting.participants          
    }
    return jsonify(meeting_data)

# Update meeting
@app.route("/meetings/<int:id>", methods=["PUT"])
def modify_meeting(id):
    meeting = Meeting.query.get(id)
    if not meeting:
        abort(404, description="Meeting not found")

    data = request.json
    meeting.topic = data.get("topic", meeting.topic)
    meeting.date = data.get("date", meeting.date)
    meeting.start_time = data.get("start_time", meeting.start_time)
    meeting.end_time = data.get("end_time", meeting.end_time)
    meeting.participants = data.get("participants", meeting.participants)

    db.session.commit()
    return jsonify({'message': 'Meeting updated successfully'})

# Delete meeting
@app.route("/meetings/<int:id>", methods=["DELETE"])
def remove_meeting(id):
    meeting = Meeting.query.get(id)
    if not meeting:
        abort(404, description="Meeting not found")

    db.session.delete(meeting)
    db.session.commit()
    return jsonify({'message': 'Meeting deleted successfully'})

if __name__ == "__main__":
    app.run(debug=True)
