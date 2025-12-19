#!/usr/bin/env python3
"""
Campus IT Helpdesk Ticket Microservice
Student ID: 25RP19452-NIYONKURU
Simple REST API for submitting and tracking IT support tickets
"""

from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import os
import logging
from functools import wraps

# Initialize Flask application
app = Flask(__name__)

# Configuration
app.config['JSON_SORT_KEYS'] = False
DATABASE = '/data/tickets.db'
LOG_FILE = '/var/log/helpdesk/app.log'

# Setup logging
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize database
def init_db():
    """Initialize SQLite database with schema"""
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  description TEXT NOT NULL,
                  category TEXT NOT NULL,
                  priority TEXT NOT NULL,
                  submitter_email TEXT NOT NULL,
                  submitter_name TEXT NOT NULL,
                  status TEXT DEFAULT 'open',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  assigned_to TEXT,
                  resolution_notes TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS metrics
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  metric_type TEXT NOT NULL,
                  metric_value INTEGER NOT NULL,
                  recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

# Decorator for error handling
def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({'error': str(e)}), 500
    return decorated_function

# Routes
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Campus IT Helpdesk - 25RP19452-NIYONKURU'
    }), 200

@app.route('/api/v1/tickets', methods=['POST'])
@handle_errors
def create_ticket():
    """Create a new support ticket"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'category', 'priority', 'submitter_email', 'submitter_name']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate category and priority
    valid_categories = ['network', 'login', 'lab_computers', 'software', 'hardware', 'other']
    valid_priorities = ['low', 'medium', 'high', 'critical']
    
    if data['category'] not in valid_categories:
        return jsonify({'error': f'Invalid category. Must be one of {valid_categories}'}), 400
    
    if data['priority'] not in valid_priorities:
        return jsonify({'error': f'Invalid priority. Must be one of {valid_priorities}'}), 400
    
    # Insert ticket into database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''INSERT INTO tickets 
                 (title, description, category, priority, submitter_email, submitter_name)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (data['title'], data['description'], data['category'], 
               data['priority'], data['submitter_email'], data['submitter_name']))
    
    ticket_id = c.lastrowid
    conn.commit()
    conn.close()
    
    logger.info(f"Ticket created: ID={ticket_id}, Category={data['category']}, Priority={data['priority']}")
    
    return jsonify({
        'message': 'Ticket created successfully',
        'ticket_id': ticket_id
    }), 201

@app.route('/api/v1/tickets', methods=['GET'])
@handle_errors
def get_tickets():
    """Retrieve all tickets with optional filtering"""
    status = request.args.get('status')
    category = request.args.get('category')
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    query = 'SELECT * FROM tickets WHERE 1=1'
    params = []
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    query += ' ORDER BY created_at DESC'
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    
    tickets = [dict(row) for row in rows]
    
    logger.info(f"Retrieved {len(tickets)} tickets with filters: status={status}, category={category}")
    
    return jsonify({
        'count': len(tickets),
        'tickets': tickets
    }), 200

@app.route('/api/v1/tickets/<int:ticket_id>', methods=['GET'])
@handle_errors
def get_ticket(ticket_id):
    """Retrieve a specific ticket by ID"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('SELECT * FROM tickets WHERE id = ?', (ticket_id,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        return jsonify({'error': 'Ticket not found'}), 404
    
    logger.info(f"Retrieved ticket: ID={ticket_id}")
    return jsonify(dict(row)), 200

@app.route('/api/v1/tickets/<int:ticket_id>', methods=['PUT'])
@handle_errors
def update_ticket(ticket_id):
    """Update a ticket"""
    data = request.get_json()
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Check if ticket exists
    c.execute('SELECT id FROM tickets WHERE id = ?', (ticket_id,))
    if not c.fetchone():
        conn.close()
        return jsonify({'error': 'Ticket not found'}), 404
    
    # Update allowed fields
    allowed_updates = ['status', 'assigned_to', 'resolution_notes', 'priority']
    updates = {k: v for k, v in data.items() if k in allowed_updates}
    
    if updates:
        updates['updated_at'] = datetime.utcnow().isoformat()
        set_clause = ', '.join([f'{k} = ?' for k in updates.keys()])
        values = list(updates.values()) + [ticket_id]
        
        c.execute(f'UPDATE tickets SET {set_clause} WHERE id = ?', values)
        conn.commit()
        logger.info(f"Ticket updated: ID={ticket_id}, Updates={updates}")
    
    conn.close()
    return jsonify({'message': 'Ticket updated successfully'}), 200

@app.route('/api/v1/metrics', methods=['GET'])
@handle_errors
def get_metrics():
    """Get system metrics for administrators"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Total tickets
    c.execute('SELECT COUNT(*) as count FROM tickets')
    total_tickets = c.fetchone()[0]
    
    # Open tickets
    c.execute('SELECT COUNT(*) as count FROM tickets WHERE status = "open"')
    open_tickets = c.fetchone()[0]
    
    # Tickets by category
    c.execute('''SELECT category, COUNT(*) as count 
                 FROM tickets GROUP BY category''')
    tickets_by_category = {row[0]: row[1] for row in c.fetchall()}
    
    # Tickets by priority
    c.execute('''SELECT priority, COUNT(*) as count 
                 FROM tickets GROUP BY priority''')
    tickets_by_priority = {row[0]: row[1] for row in c.fetchall()}
    
    conn.close()
    
    logger.info("Metrics retrieved for dashboard")
    
    return jsonify({
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'tickets_by_category': tickets_by_category,
        'tickets_by_priority': tickets_by_priority,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/v1/health', methods=['GET'])
def api_health():
    """API health endpoint with detailed status"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.execute('SELECT 1')
        conn.close()
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'operational',
        'database': db_status,
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    init_db()
    logger.info("Starting Campus IT Helpdesk Ticket Microservice")
    app.run(host='0.0.0.0', port=5000, debug=False)
