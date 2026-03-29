"""
ACEest Fitness & Gym - Flask Web Application
A comprehensive fitness management system with client profiles, programs, and progress tracking.
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import os
from contextlib import contextmanager

# Initialize Flask Application
app = Flask(__name__)
CORS(app)

# Configuration
DATABASE = os.environ.get('DATABASE_PATH', 'aceest_fitness.db')
app.config['JSON_SORT_KEYS'] = False


# ============================================================================
# DATABASE INITIALIZATION & UTILITIES
# ============================================================================

def get_db_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_db():
    """Initialize database schema."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Clients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                age INTEGER NOT NULL,
                weight REAL NOT NULL,
                program TEXT NOT NULL,
                calories INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Progress tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT NOT NULL,
                week TEXT NOT NULL,
                adherence INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_name) REFERENCES clients(name)
            )
        """)
        
        # Workouts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT NOT NULL,
                date TEXT NOT NULL,
                workout_type TEXT NOT NULL,
                duration_min INTEGER,
                notes TEXT,
                FOREIGN KEY (client_name) REFERENCES clients(name)
            )
        """)
        
        # Metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT NOT NULL,
                date TEXT NOT NULL,
                weight REAL,
                waist REAL,
                bodyfat REAL,
                FOREIGN KEY (client_name) REFERENCES clients(name)
            )
        """)


# ============================================================================
# CORE BUSINESS LOGIC
# ============================================================================

PROGRAMS = {
    "Fat Loss (FL)": {
        "factor": 22,
        "description": "High-intensity cardio with calorie deficit",
        "workout": "Mon: Back Squat 5x5 + Core, Tue: EMOM 20min Assault Bike, Wed: Bench Press + 21-15-9, Thu: Deadlift + Box Jumps, Fri: Zone 2 Cardio 30min"
    },
    "Muscle Gain (MG)": {
        "factor": 35,
        "description": "Progressive strength training with surplus",
        "workout": "Mon: Squat 5x5, Tue: Bench 5x5, Wed: Deadlift 4x6, Thu: Front Squat 4x8, Fri: Incline Press 4x10, Sat: Barbell Rows 4x10"
    },
    "Beginner (BG)": {
        "factor": 26,
        "description": "Full-body circuit focused on form mastery",
        "workout": "Full Body Circuit: Air Squats, Ring Rows, Push-ups. Focus: Technique & Consistency"
    }
}


def calculate_calories(weight: float, program: str) -> int:
    """Calculate daily calorie requirements based on weight and program."""
    if program not in PROGRAMS:
        raise ValueError(f"Program '{program}' not found")
    return int(weight * PROGRAMS[program]['factor'])


def get_week_identifier() -> str:
    """Get current week identifier (Week X - YYYY)."""
    return datetime.now().strftime("Week %U - %Y")


# ============================================================================
# ROUTES - HEALTH & INITIALIZATION
# ============================================================================
@app.route('/', methods=['GET'])
def home():
    """Root endpoint - API documentation and status."""
    return jsonify({
        'message': 'Welcome to ACEest Fitness & Gym API',
        'service': 'ACEest Fitness API',
        'version': '1.0.0',
        'status': 'running',
        'documentation': 'See README.md or API.md for full documentation',
        'quick_links': {
            'health': '/health',
            'initialize': '/init (POST)',
            'programs': '/programs',
            'clients': '/clients',
            'api_docs': 'Check API.md file'
        },
        'endpoints': {
            'GET /health': 'Health check endpoint',
            'POST /init': 'Initialize database',
            'GET /programs': 'List all programs',
            'GET /clients': 'List all clients',
            'POST /clients': 'Create new client',
            'GET /clients/{name}': 'Get client details',
            'PUT /clients/{name}': 'Update client',
            'DELETE /clients/{name}': 'Delete client'
        }
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'ACEest Fitness API',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/initialize', methods=['POST'])
def initialize():
    """Initialize database."""
    try:
        init_db()
        return jsonify({
            'status': 'success',
            'message': 'Database initialized successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============================================================================
# ROUTES - PROGRAMS
# ============================================================================

@app.route('/programs', methods=['GET'])
def get_programs():
    """Get all available fitness programs."""
    return jsonify({
        'status': 'success',
        'data': PROGRAMS
    }), 200


# ============================================================================
# ROUTES - CLIENTS
# ============================================================================

@app.route('/clients', methods=['GET'])
def list_clients():
    """Get all clients."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clients ORDER BY created_at DESC')
            clients = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({
            'status': 'success',
            'count': len(clients),
            'data': clients
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/clients', methods=['POST'])
def create_client():
    """Create a new client."""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['name', 'age', 'weight', 'program']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {required_fields}'
            }), 400
        
        if data['program'] not in PROGRAMS:
            return jsonify({
                'status': 'error',
                'message': f"Program must be one of: {list(PROGRAMS.keys())}"
            }), 400
        
        # Calculate calories
        calories = calculate_calories(data['weight'], data['program'])
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clients (name, age, weight, program, calories)
                VALUES (?, ?, ?, ?, ?)
            """, (data['name'], data['age'], data['weight'], data['program'], calories))
        
        return jsonify({
            'status': 'success',
            'message': f"Client '{data['name']}' created successfully",
            'data': {
                'name': data['name'],
                'age': data['age'],
                'weight': data['weight'],
                'program': data['program'],
                'calories': calories
            }
        }), 201
    except sqlite3.IntegrityError:
        return jsonify({
            'status': 'error',
            'message': 'Client with this name already exists'
        }), 409
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/clients/<name>', methods=['GET'])
def get_client(name):
    """Get client details."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clients WHERE name = ?', (name,))
            client = cursor.fetchone()
        
        if not client:
            return jsonify({
                'status': 'error',
                'message': f"Client '{name}' not found"
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': dict(client)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/clients/<name>', methods=['PUT'])
def update_client(name):
    """Update client details."""
    try:
        data = request.get_json()
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clients WHERE name = ?', (name,))
            if not cursor.fetchone():
                return jsonify({
                    'status': 'error',
                    'message': f"Client '{name}' not found"
                }), 404
            
            # Build dynamic update query
            updates = []
            params = []
            for field in ['age', 'weight', 'program']:
                if field in data:
                    updates.append(f"{field} = ?")
                    params.append(data[field])
            
            if not updates:
                return jsonify({
                    'status': 'error',
                    'message': 'No valid fields to update'
                }), 400
            
            # Recalculate calories if weight or program changed
            if 'weight' in data or 'program' in data:
                cursor.execute('SELECT weight, program FROM clients WHERE name = ?', (name,))
                current = cursor.fetchone()
                new_weight = data.get('weight', current['weight'])
                new_program = data.get('program', current['program'])
                new_calories = calculate_calories(new_weight, new_program)
                updates.append('calories = ?')
                params.append(new_calories)
            
            params.append(name)
            cursor.execute(f"UPDATE clients SET {', '.join(updates)} WHERE name = ?", params)
        
        return jsonify({
            'status': 'success',
            'message': f"Client '{name}' updated successfully"
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/clients/<name>', methods=['DELETE'])
def delete_client(name):
    """Delete a client."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clients WHERE name = ?', (name,))
            if not cursor.fetchone():
                return jsonify({
                    'status': 'error',
                    'message': f"Client '{name}' not found"
                }), 404
            
            cursor.execute('DELETE FROM clients WHERE name = ?', (name,))
        
        return jsonify({
            'status': 'success',
            'message': f"Client '{name}' deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============================================================================
# ROUTES - PROGRESS TRACKING
# ============================================================================

@app.route('/clients/<name>/progress', methods=['GET'])
def get_client_progress(name):
    """Get client's progress history."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM progress WHERE client_name = ? ORDER BY created_at DESC', (name,))
            progress = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({
            'status': 'success',
            'count': len(progress),
            'data': progress
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/clients/<name>/progress', methods=['POST'])
def record_progress(name):
    """Record weekly progress for a client."""
    try:
        data = request.get_json()
        
        if 'adherence' not in data or not (0 <= data['adherence'] <= 100):
            return jsonify({
                'status': 'error',
                'message': 'Adherence must be between 0 and 100'
            }), 400
        
        week = get_week_identifier()
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM clients WHERE name = ?', (name,))
            if not cursor.fetchone():
                return jsonify({
                    'status': 'error',
                    'message': f"Client '{name}' not found"
                }), 404
            
            cursor.execute("""
                INSERT INTO progress (client_name, week, adherence)
                VALUES (?, ?, ?)
            """, (name, week, data['adherence']))
        
        return jsonify({
            'status': 'success',
            'message': f"Progress recorded for {name}",
            'data': {
                'client_name': name,
                'week': week,
                'adherence': data['adherence']
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============================================================================
# ROUTES - WORKOUTS
# ============================================================================

@app.route('/clients/<name>/workouts', methods=['GET'])
def get_client_workouts(name):
    """Get client's workout history."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM workouts WHERE client_name = ? ORDER BY date DESC', (name,))
            workouts = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({
            'status': 'success',
            'count': len(workouts),
            'data': workouts
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/clients/<name>/workouts', methods=['POST'])
def log_workout(name):
    """Log a workout session for a client."""
    try:
        data = request.get_json()
        
        required_fields = ['workout_type', 'date']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {required_fields}'
            }), 400
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM clients WHERE name = ?', (name,))
            if not cursor.fetchone():
                return jsonify({
                    'status': 'error',
                    'message': f"Client '{name}' not found"
                }), 404
            
            cursor.execute("""
                INSERT INTO workouts (client_name, date, workout_type, duration_min, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (name, data['date'], data['workout_type'], 
                  data.get('duration_min'), data.get('notes')))
        
        return jsonify({
            'status': 'success',
            'message': 'Workout logged successfully',
            'data': {
                'client_name': name,
                'workout_type': data['workout_type'],
                'date': data['date']
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============================================================================
# ROUTES - METRICS
# ============================================================================

@app.route('/clients/<name>/metrics', methods=['GET'])
def get_client_metrics(name):
    """Get client's body metrics history."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM metrics WHERE client_name = ? ORDER BY date DESC', (name,))
            metrics = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({
            'status': 'success',
            'count': len(metrics),
            'data': metrics
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/clients/<name>/metrics', methods=['POST'])
def record_metrics(name):
    """Record body metrics for a client."""
    try:
        data = request.get_json()
        
        if 'date' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Date is required'
            }), 400
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM clients WHERE name = ?', (name,))
            if not cursor.fetchone():
                return jsonify({
                    'status': 'error',
                    'message': f"Client '{name}' not found"
                }), 404
            
            cursor.execute("""
                INSERT INTO metrics (client_name, date, weight, waist, bodyfat)
                VALUES (?, ?, ?, ?, ?)
            """, (name, data['date'], data.get('weight'), 
                  data.get('waist'), data.get('bodyfat')))
        
        return jsonify({
            'status': 'success',
            'message': 'Metrics recorded successfully',
            'data': {
                'client_name': name,
                'date': data['date']
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    # Run Flask application
    debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
