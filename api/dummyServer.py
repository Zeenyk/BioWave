from flask import Flask, jsonify, request, make_response
from datetime import datetime, timedelta, timezone
import random
import csv
from io import StringIO
from functools import wraps

app = Flask(__name__)

# Dummy data storage
current_state = {
    "stirring": True,
    "rpm": 300,
    "temperature": 37.5,
    "ph": 6.8,
    "oxygen": 98
}

scheduled_operations = []
data_logs = []
users = {"admin": "password123"}  # Simple user storage
tokens = set()

# Generate some initial dummy logs
def generate_initial_logs():
    now = datetime.now(timezone.utc)
    for i in range(100):
        timestamp = now - timedelta(minutes=i*10)
        data_logs.append({
            "timestamp": timestamp.isoformat(),
            "temperature": round(37.0 + random.uniform(-0.5, 0.5), 1),
            "ph": round(6.5 + random.uniform(0, 1), 1),
            "rpm": random.randint(200, 350),
            "oxygen": random.randint(95, 100)
        })

generate_initial_logs()

# Authentication decorator (for protected routes)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer ') or token[7:] not in tokens:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/status', methods=['GET'])
def get_status():
    # Update with some random variation
    current_state["temperature"] = round(37.0 + random.uniform(-0.5, 0.5), 1)
    current_state["ph"] = round(6.5 + random.uniform(0, 1), 1)
    current_state["oxygen"] = random.randint(95, 100)
    
    response = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **current_state
    }
    return jsonify(response)

@app.route('/api/control', methods=['POST'])
@token_required
def control():
    data = request.get_json()
    command = data.get('command')
    value = data.get('value')
    
    if command == 'set_rpm':
        current_state['rpm'] = value
    elif command == 'toggle_stirring':
        current_state['stirring'] = not current_state['stirring']
    else:
        return jsonify({"error": "Invalid command"}), 400
    
    # Log this change
    data_logs.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **current_state
    })
    
    return jsonify({"status": "success"})

@app.route('/api/schedule', methods=['GET'])
@token_required
def get_schedule():
    return jsonify(scheduled_operations)

@app.route('/api/schedule', methods=['POST'])
@token_required
def add_schedule():
    data = request.get_json()
    new_id = max([op['id'] for op in scheduled_operations], default=0) + 1
    operation = {
        "id": new_id,
        "command": data['command'],
        "value": data['value'],
        "time": data['time']
    }
    scheduled_operations.append(operation)
    return jsonify({"status": "success", "id": new_id})

@app.route('/api/schedule/<int:id>', methods=['DELETE'])
@token_required
def delete_schedule(id):
    global scheduled_operations
    scheduled_operations = [op for op in scheduled_operations if op['id'] != id]
    return jsonify({"status": "success"})

@app.route('/api/logs', methods=['GET'])
@token_required
def get_logs():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    
    filtered_logs = data_logs
    
    if from_time:
        filtered_logs = [log for log in filtered_logs if log['timestamp'] >= from_time]
    if to_time:
        filtered_logs = [log for log in filtered_logs if log['timestamp'] <= to_time]
    
    return jsonify(filtered_logs)

@app.route('/api/logs/export', methods=['GET'])
@token_required
def export_logs():
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    
    filtered_logs = data_logs
    
    if from_time:
        filtered_logs = [log for log in filtered_logs if log['timestamp'] >= from_time]
    if to_time:
        filtered_logs = [log for log in filtered_logs if log['timestamp'] <= to_time]
    
    # Create CSV
    si = StringIO()
    writer = csv.DictWriter(si, fieldnames=["timestamp", "temperature", "ph", "rpm", "oxygen"])
    writer.writeheader()
    writer.writerows(filtered_logs)
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=biowave_logs.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users and users[username] == password:
        token = f"dummy_token_{random.randint(1000, 9999)}"
        tokens.add(token)
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

# In the logout endpoint, modify to:
@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout():
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token[7:]
        if token in tokens:
            tokens.remove(token)
            return jsonify({"status": "success", "message": "Token invalidated"})
    return jsonify({"error": "Invalid token"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)