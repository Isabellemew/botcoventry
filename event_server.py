from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
EVENTS_FILE = 'events.json'

def load_events():
    if not os.path.exists(EVENTS_FILE):
        return []
    with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_events(events):
    with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing event text'}), 400
    event = {
        'text': data['text'],
        'date': datetime.utcnow().isoformat()
    }
    events = load_events()
    events.append(event)
    save_events(events)
    return jsonify({'status': 'ok', 'event': event})

if __name__ == '__main__':
    app.run(port=8080)
