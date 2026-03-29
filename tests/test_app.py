"""
Test suite for ACEest Fitness & Gym API
Comprehensive unit tests for all core functionality
"""

import pytest
import json
import os
import sqlite3
from datetime import datetime
import tempfile

# Import the Flask application
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, init_db, calculate_calories, get_week_identifier, PROGRAMS


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def client():
    """Create a test client with a temporary database."""
    # Use temporary database for tests
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    os.environ['DATABASE_PATH'] = db_path
    
    # Reinitialize app to use test database
    with app.app_context():
        init_db()
    
    test_client = app.test_client()
    
    yield test_client
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
    if 'DATABASE_PATH' in os.environ:
        del os.environ['DATABASE_PATH']


@pytest.fixture
def sample_client_data():
    """Sample client data for testing."""
    return {
        'name': 'John Doe',
        'age': 30,
        'weight': 80.5,
        'program': 'Fat Loss (FL)'
    }


# ============================================================================
# TESTS - HEALTH & INITIALIZATION
# ============================================================================

class TestHealthAndInit:
    """Tests for health check and initialization endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'service' in data
    
    def test_database_initialization(self, client):
        """Test database initialization endpoint."""
        response = client.post('/initialize')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'


# ============================================================================
# TESTS - PROGRAMS
# ============================================================================

class TestPrograms:
    """Tests for fitness programs endpoints."""
    
    def test_get_all_programs(self, client):
        """Test retrieving all available programs."""
        response = client.get('/programs')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']) == 3
        assert 'Fat Loss (FL)' in data['data']
        assert 'Muscle Gain (MG)' in data['data']
        assert 'Beginner (BG)' in data['data']
    
    def test_program_structure(self, client):
        """Test that programs have required structure."""
        response = client.get('/programs')
        data = json.loads(response.data)
        
        for program_name, program_data in data['data'].items():
            assert 'factor' in program_data
            assert 'description' in program_data
            assert isinstance(program_data['factor'], (int, float))


# ============================================================================
# TESTS - CLIENTS CRUD
# ============================================================================

class TestClientsCRUD:
    """Tests for client CRUD operations."""
    
    def test_list_clients_empty(self, client):
        """Test listing clients when none exist."""
        response = client.get('/clients')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['count'] == 0
        assert data['data'] == []
    
    def test_create_client_success(self, client, sample_client_data):
        """Test successful client creation."""
        response = client.post('/clients',
                              data=json.dumps(sample_client_data),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['name'] == 'John Doe'
        assert data['data']['calories'] == 1771  # 80.5 * 22
    
    def test_create_client_missing_fields(self, client):
        """Test client creation with missing required fields."""
        incomplete_data = {'name': 'Jane Doe', 'age': 25}
        response = client.post('/clients',
                              data=json.dumps(incomplete_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_create_client_invalid_program(self, client):
        """Test client creation with invalid program."""
        bad_data = {
            'name': 'Test User',
            'age': 25,
            'weight': 70,
            'program': 'Invalid Program'
        }
        response = client.post('/clients',
                              data=json.dumps(bad_data),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_create_duplicate_client(self, client, sample_client_data):
        """Test creating duplicate client names."""
        # Create first client
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        # Attempt to create duplicate
        response = client.post('/clients',
                              data=json.dumps(sample_client_data),
                              content_type='application/json')
        assert response.status_code == 409
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_get_client_success(self, client, sample_client_data):
        """Test retrieving a specific client."""
        # Create client
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        # Retrieve client
        response = client.get(f"/clients/{sample_client_data['name']}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['name'] == 'John Doe'
    
    def test_get_client_not_found(self, client):
        """Test retrieving non-existent client."""
        response = client.get('/clients/NonExistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_update_client_success(self, client, sample_client_data):
        """Test updating client details."""
        # Create client
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        # Update client
        update_data = {'age': 31, 'weight': 85.0}
        response = client.put(f"/clients/{sample_client_data['name']}",
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
    
    def test_update_client_not_found(self, client):
        """Test updating non-existent client."""
        update_data = {'age': 31}
        response = client.put('/clients/NonExistent',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 404
    
    def test_delete_client_success(self, client, sample_client_data):
        """Test deleting a client."""
        # Create client
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        # Delete client
        response = client.delete(f"/clients/{sample_client_data['name']}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        
        # Verify deletion
        get_response = client.get(f"/clients/{sample_client_data['name']}")
        assert get_response.status_code == 404
    
    def test_delete_client_not_found(self, client):
        """Test deleting non-existent client."""
        response = client.delete('/clients/NonExistent')
        assert response.status_code == 404


# ============================================================================
# TESTS - PROGRESS TRACKING
# ============================================================================

class TestProgress:
    """Tests for progress tracking functionality."""
    
    def test_get_progress_empty(self, client, sample_client_data):
        """Test getting progress for client with no records."""
        # Create client
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        response = client.get(f"/clients/{sample_client_data['name']}/progress")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 0
    
    def test_record_progress_success(self, client, sample_client_data):
        """Test recording weekly progress."""
        # Create client
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        progress_data = {'adherence': 85}
        response = client.post(f"/clients/{sample_client_data['name']}/progress",
                              data=json.dumps(progress_data),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['adherence'] == 85
    
    def test_record_progress_invalid_adherence(self, client, sample_client_data):
        """Test recording progress with invalid adherence."""
        # Create client
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        bad_data = {'adherence': 150}  # Over 100
        response = client.post(f"/clients/{sample_client_data['name']}/progress",
                              data=json.dumps(bad_data),
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_record_progress_non_existent_client(self, client):
        """Test recording progress for non-existent client."""
        progress_data = {'adherence': 85}
        response = client.post('/clients/NonExistent/progress',
                              data=json.dumps(progress_data),
                              content_type='application/json')
        assert response.status_code == 404


# ============================================================================
# TESTS - WORKOUTS
# ============================================================================

class TestWorkouts:
    """Tests for workout logging functionality."""
    
    def test_get_workouts_empty(self, client, sample_client_data):
        """Test getting workouts for client with no records."""
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        response = client.get(f"/clients/{sample_client_data['name']}/workouts")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 0
    
    def test_log_workout_success(self, client, sample_client_data):
        """Test logging a workout."""
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        workout_data = {
            'workout_type': 'Back Squat 5x5 + Core',
            'date': '2024-03-10',
            'duration_min': 60,
            'notes': 'Great session!'
        }
        response = client.post(f"/clients/{sample_client_data['name']}/workouts",
                              data=json.dumps(workout_data),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
    
    def test_log_workout_missing_fields(self, client, sample_client_data):
        """Test logging workout with missing required fields."""
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        bad_data = {'workout_type': 'Squat'}  # Missing date
        response = client.post(f"/clients/{sample_client_data['name']}/workouts",
                              data=json.dumps(bad_data),
                              content_type='application/json')
        assert response.status_code == 400


# ============================================================================
# TESTS - METRICS
# ============================================================================

class TestMetrics:
    """Tests for body metrics tracking."""
    
    def test_get_metrics_empty(self, client, sample_client_data):
        """Test getting metrics for client with no records."""
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        response = client.get(f"/clients/{sample_client_data['name']}/metrics")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] == 0
    
    def test_record_metrics_success(self, client, sample_client_data):
        """Test recording body metrics."""
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        metrics_data = {
            'date': '2024-03-10',
            'weight': 79.5,
            'waist': 85.0,
            'bodyfat': 18.5
        }
        response = client.post(f"/clients/{sample_client_data['name']}/metrics",
                              data=json.dumps(metrics_data),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
    
    def test_record_metrics_missing_date(self, client, sample_client_data):
        """Test recording metrics without date."""
        client.post('/clients',
                   data=json.dumps(sample_client_data),
                   content_type='application/json')
        
        bad_data = {'weight': 79.5}  # Missing date
        response = client.post(f"/clients/{sample_client_data['name']}/metrics",
                              data=json.dumps(bad_data),
                              content_type='application/json')
        assert response.status_code == 400


# ============================================================================
# TESTS - BUSINESS LOGIC
# ============================================================================

class TestBusinessLogic:
    """Tests for core business logic functions."""
    
    def test_calculate_calories_fat_loss(self):
        """Test calorie calculation for Fat Loss program."""
        calories = calculate_calories(80, 'Fat Loss (FL)')
        assert calories == 1760  # 80 * 22
    
    def test_calculate_calories_muscle_gain(self):
        """Test calorie calculation for Muscle Gain program."""
        calories = calculate_calories(80, 'Muscle Gain (MG)')
        assert calories == 2800  # 80 * 35
    
    def test_calculate_calories_beginner(self):
        """Test calorie calculation for Beginner program."""
        calories = calculate_calories(70, 'Beginner (BG)')
        assert calories == 1820  # 70 * 26
    
    def test_calculate_calories_invalid_program(self):
        """Test calorie calculation with invalid program."""
        with pytest.raises(ValueError):
            calculate_calories(80, 'Invalid Program')
    
    def test_get_week_identifier(self):
        """Test week identifier generation."""
        week = get_week_identifier()
        assert 'Week' in week
        assert str(datetime.now().year) in week


# ============================================================================
# TESTS - ERROR HANDLING
# ============================================================================

class TestErrorHandling:
    """Tests for error handling and edge cases."""
    
    def test_404_not_found(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_invalid_json(self, client):
        """Test handling of invalid JSON."""
        response = client.post('/clients',
                              data='invalid json',
                              content_type='application/json')
        assert response.status_code in [400, 500]


# ============================================================================
# TESTS - INTEGRATION
# ============================================================================

class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_complete_client_lifecycle(self, client, sample_client_data):
        """Test complete client lifecycle: create, update, log progress, delete."""
        # Create client
        create_response = client.post('/clients',
                                     data=json.dumps(sample_client_data),
                                     content_type='application/json')
        assert create_response.status_code == 201
        
        # Update client
        update_data = {'weight': 79.0}
        update_response = client.put(f"/clients/{sample_client_data['name']}",
                                    data=json.dumps(update_data),
                                    content_type='application/json')
        assert update_response.status_code == 200
        
        # Record progress
        progress_data = {'adherence': 90}
        progress_response = client.post(f"/clients/{sample_client_data['name']}/progress",
                                       data=json.dumps(progress_data),
                                       content_type='application/json')
        assert progress_response.status_code == 201
        
        # Log workout
        workout_data = {
            'workout_type': 'Cardio',
            'date': '2024-03-10',
            'duration_min': 30
        }
        workout_response = client.post(f"/clients/{sample_client_data['name']}/workouts",
                                      data=json.dumps(workout_data),
                                      content_type='application/json')
        assert workout_response.status_code == 201
        
        # Delete client
        delete_response = client.delete(f"/clients/{sample_client_data['name']}")
        assert delete_response.status_code == 200
    
    def test_multiple_clients_management(self, client):
        """Test managing multiple clients."""
        clients_data = [
            {'name': 'Client 1', 'age': 25, 'weight': 70, 'program': 'Fat Loss (FL)'},
            {'name': 'Client 2', 'age': 30, 'weight': 80, 'program': 'Muscle Gain (MG)'},
            {'name': 'Client 3', 'age': 35, 'weight': 75, 'program': 'Beginner (BG)'}
        ]
        
        # Create all clients
        for client_data in clients_data:
            response = client.post('/clients',
                                  data=json.dumps(client_data),
                                  content_type='application/json')
            assert response.status_code == 201
        
        # List all clients
        list_response = client.get('/clients')
        data = json.loads(list_response.data)
        assert data['count'] == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=app', '--cov-report=html'])
