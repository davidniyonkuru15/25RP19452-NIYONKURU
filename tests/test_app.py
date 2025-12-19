"""
Unit tests for Campus IT Helpdesk Ticket Microservice
Student ID: 25RP19452-NIYONKURU
"""

import unittest
import json
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import tempfile
import app as app_module

# Use temp file database for testing (in-memory won't persist across connections)
temp_db = os.path.join(tempfile.gettempdir(), 'test_tickets.db')
try:
    os.remove(temp_db)
except OSError:
    pass
app_module.DATABASE = temp_db
from app import app, init_db

class HelpdeskTestCase(unittest.TestCase):
    """Test cases for the helpdesk API"""
    
    def setUp(self):
        """Set up test client and database"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Initialize database for testing
        with self.app.app_context():
            init_db()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_api_health(self):
        """Test API health endpoint"""
        response = self.client.get('/api/v1/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'operational')
    
    def test_create_ticket_success(self):
        """Test successful ticket creation"""
        ticket_data = {
            'title': 'Network connectivity issue',
            'description': 'Cannot access university network',
            'category': 'network',
            'priority': 'high',
            'submitter_email': 'student@university.edu',
            'submitter_name': 'John Doe'
        }
        response = self.client.post('/api/v1/tickets',
                                   data=json.dumps(ticket_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('ticket_id', data)
    
    def test_create_ticket_missing_fields(self):
        """Test ticket creation with missing fields"""
        ticket_data = {
            'title': 'Network issue',
            'category': 'network'
        }
        response = self.client.post('/api/v1/tickets',
                                   data=json.dumps(ticket_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_create_ticket_invalid_category(self):
        """Test ticket creation with invalid category"""
        ticket_data = {
            'title': 'Test issue',
            'description': 'Test description',
            'category': 'invalid_category',
            'priority': 'high',
            'submitter_email': 'test@uni.edu',
            'submitter_name': 'Test User'
        }
        response = self.client.post('/api/v1/tickets',
                                   data=json.dumps(ticket_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_tickets(self):
        """Test retrieving all tickets"""
        response = self.client.get('/api/v1/tickets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('count', data)
        self.assertIn('tickets', data)
    
    def test_get_ticket_by_id(self):
        """Test retrieving a specific ticket"""
        # First create a ticket
        ticket_data = {
            'title': 'Test ticket',
            'description': 'Test description',
            'category': 'software',
            'priority': 'medium',
            'submitter_email': 'test@uni.edu',
            'submitter_name': 'Test User'
        }
        create_response = self.client.post('/api/v1/tickets',
                                          data=json.dumps(ticket_data),
                                          content_type='application/json')
        ticket_id = json.loads(create_response.data)['ticket_id']
        
        # Then retrieve it
        response = self.client.get(f'/api/v1/tickets/{ticket_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Test ticket')
    
    def test_get_nonexistent_ticket(self):
        """Test retrieving a non-existent ticket"""
        response = self.client.get('/api/v1/tickets/99999')
        self.assertEqual(response.status_code, 404)
    
    def test_update_ticket(self):
        """Test updating a ticket"""
        # Create a ticket first
        ticket_data = {
            'title': 'Test ticket',
            'description': 'Test description',
            'category': 'hardware',
            'priority': 'low',
            'submitter_email': 'test@uni.edu',
            'submitter_name': 'Test User'
        }
        create_response = self.client.post('/api/v1/tickets',
                                          data=json.dumps(ticket_data),
                                          content_type='application/json')
        ticket_id = json.loads(create_response.data)['ticket_id']
        
        # Update it
        update_data = {
            'status': 'resolved',
            'assigned_to': 'Admin User',
            'resolution_notes': 'Issue fixed'
        }
        response = self.client.put(f'/api/v1/tickets/{ticket_id}',
                                  data=json.dumps(update_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_get_metrics(self):
        """Test metrics endpoint"""
        response = self.client.get('/api/v1/metrics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('total_tickets', data)
        self.assertIn('open_tickets', data)
        self.assertIn('tickets_by_category', data)
        self.assertIn('tickets_by_priority', data)
    
    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get('/invalid/endpoint')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
