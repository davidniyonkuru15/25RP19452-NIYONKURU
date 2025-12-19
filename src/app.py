#!/usr/bin/env python3
"""
Campus IT Helpdesk Ticket Microservice
Student ID: 25RP19452-NIYONKURU
Simple REST API for submitting and tracking IT support tickets
"""

from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import sqlite3
import os
import logging
from functools import wraps
import tempfile

# Initialize Flask application
app = Flask(__name__)

# Configuration
app.config['JSON_SORT_KEYS'] = False
DATABASE = os.environ.get('DATABASE_PATH', '/data/tickets.db')

# Setup logging - handle permissions gracefully
try:
    log_dir = '/var/log/helpdesk'
    if os.access('/var/log', os.W_OK):
        os.makedirs(log_dir, exist_ok=True)
    else:
        log_dir = '/tmp/helpdesk-logs'
        os.makedirs(log_dir, exist_ok=True)
except Exception:
    log_dir = tempfile.gettempdir()
    os.makedirs(os.path.join(log_dir, 'helpdesk-logs'), exist_ok=True)
    log_dir = os.path.join(log_dir, 'helpdesk-logs')

LOG_FILE = os.path.join(log_dir, 'app.log')

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
    db_dir = os.path.dirname(DATABASE)
    if db_dir:
        try:
            os.makedirs(db_dir, exist_ok=True)
        except Exception:
            pass  # Use temp directory as fallback
    
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

# HTML Frontend Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campus IT Helpdesk - 25RP19452-NIYONKURU</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header {
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        header h1 { color: #667eea; margin-bottom: 5px; }
        header p { color: #666; font-size: 14px; }
        .status-badge {
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            margin-top: 10px;
        }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }
        .card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .card h2 { color: #333; font-size: 18px; margin-bottom: 15px; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; color: #333; font-weight: 500; margin-bottom: 5px; }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            font-family: inherit;
        }
        textarea { resize: vertical; min-height: 100px; }
        button {
            background: #667eea;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: background 0.3s;
            width: 100%;
        }
        button:hover { background: #764ba2; }
        .ticket-list { max-height: 400px; overflow-y: auto; }
        .ticket-item {
            background: #f9fafb;
            padding: 12px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
            border-radius: 3px;
        }
        .ticket-item h3 { color: #333; font-size: 14px; margin-bottom: 5px; }
        .ticket-meta { font-size: 12px; color: #999; }
        .priority { font-weight: bold; }
        .priority.critical { color: #dc2626; }
        .priority.high { color: #f97316; }
        .priority.medium { color: #eab308; }
        .priority.low { color: #22c55e; }
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 15px;
        }
        .stat-box {
            background: #f0f4ff;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .stat-box .number { font-size: 24px; font-weight: bold; color: #667eea; }
        .stat-box .label { font-size: 12px; color: #666; margin-top: 5px; }
        .alert { padding: 12px; border-radius: 5px; margin-bottom: 15px; font-size: 14px; }
        .alert-success { background: #d1fae5; color: #065f46; border: 1px solid #6ee7b7; }
        .alert-error { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
        @media (max-width: 768px) { .grid { grid-template-columns: 1fr; } .stats { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎓 Campus IT Helpdesk</h1>
            <p>Project ID: <strong>25RP19452-NIYONKURU</strong></p>
            <div class="status-badge">✓ System Operational</div>
        </header>

        <div class="grid">
            <!-- Submit New Ticket -->
            <div class="card">
                <h2>📝 Submit New Ticket</h2>
                <div id="submitAlert"></div>
                <form id="ticketForm">
                    <div class="form-group">
                        <label>Your Name</label>
                        <input type="text" id="submitter_name" required placeholder="Enter your name">
                    </div>
                    <div class="form-group">
                        <label>Your Email</label>
                        <input type="email" id="submitter_email" required placeholder="your.email@university.edu">
                    </div>
                    <div class="form-group">
                        <label>Title</label>
                        <input type="text" id="title" required placeholder="Brief issue title">
                    </div>
                    <div class="form-group">
                        <label>Description</label>
                        <textarea id="description" required placeholder="Describe the issue in detail..."></textarea>
                    </div>
                    <div class="form-group">
                        <label>Category</label>
                        <select id="category" required>
                            <option value="">Select Category</option>
                            <option value="network">Network Issue</option>
                            <option value="login">Login Problem</option>
                            <option value="lab_computers">Lab Computers</option>
                            <option value="software">Software</option>
                            <option value="hardware">Hardware</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Priority</label>
                        <select id="priority" required>
                            <option value="">Select Priority</option>
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                            <option value="critical">Critical</option>
                        </select>
                    </div>
                    <button type="submit">Submit Ticket</button>
                </form>
            </div>

            <!-- Dashboard & Recent Tickets -->
            <div class="card">
                <h2>📊 Dashboard</h2>
                <div class="stats" id="stats">
                    <div class="stat-box">
                        <div class="number" id="totalTickets">0</div>
                        <div class="label">Total Tickets</div>
                    </div>
                    <div class="stat-box">
                        <div class="number" id="openTickets">0</div>
                        <div class="label">Open</div>
                    </div>
                    <div class="stat-box">
                        <div class="number" id="closedTickets">0</div>
                        <div class="label">Closed</div>
                    </div>
                </div>
                <h3 style="margin-top: 25px; margin-bottom: 15px; color: #333;">📋 Recent Tickets</h3>
                <div class="ticket-list" id="ticketList">
                    <p style="color: #999; text-align: center; padding: 20px;">Loading tickets...</p>
                </div>
            </div>
        </div>

        <div class="card" style="text-align: center; color: #999; font-size: 12px;">
            Campus IT Helpdesk Microservice | API: /api/v1 | Health: /health
        </div>
    </div>

    <script>
        const API_BASE = '/api/v1';

        // Load initial data
        function loadDashboard() {
            fetch(API_BASE + '/tickets')
                .then(r => r.json())
                .then(data => {
                    const tickets = data.tickets || [];
                    document.getElementById('totalTickets').textContent = tickets.length;
                    document.getElementById('openTickets').textContent = tickets.filter(t => t.status === 'open').length;
                    document.getElementById('closedTickets').textContent = tickets.filter(t => t.status === 'closed').length;
                    renderTickets(tickets.slice(0, 5));
                })
                .catch(err => console.error('Error loading dashboard:', err));
        }

        function renderTickets(tickets) {
            const html = tickets.length === 0
                ? '<p style="color: #999; text-align: center; padding: 20px;">No tickets yet</p>'
                : tickets.map(t => `
                    <div class="ticket-item">
                        <h3>${t.title}</h3>
                        <div class="ticket-meta">
                            <span>#${t.id}</span> | 
                            <span class="priority ${t.priority}">${t.priority.toUpperCase()}</span> | 
                            <span>${t.status}</span>
                        </div>
                    </div>
                `).join('');
            document.getElementById('ticketList').innerHTML = html;
        }

        // Submit form
        document.getElementById('ticketForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = {
                title: document.getElementById('title').value,
                description: document.getElementById('description').value,
                category: document.getElementById('category').value,
                priority: document.getElementById('priority').value,
                submitter_email: document.getElementById('submitter_email').value,
                submitter_name: document.getElementById('submitter_name').value
            };

            fetch(API_BASE + '/tickets', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            })
            .then(r => r.json())
            .then(data => {
                if (data.id) {
                    document.getElementById('submitAlert').innerHTML = '<div class="alert alert-success">✓ Ticket submitted successfully! ID: ' + data.id + '</div>';
                    document.getElementById('ticketForm').reset();
                    setTimeout(() => loadDashboard(), 500);
                } else {
                    throw new Error(data.error || 'Error submitting ticket');
                }
            })
            .catch(err => {
                document.getElementById('submitAlert').innerHTML = '<div class="alert alert-error">✗ Error: ' + err.message + '</div>';
            });
        });

        // Refresh every 10 seconds
        loadDashboard();
        setInterval(loadDashboard, 10000);
    </script>
</body>
</html>
"""

# Routes
@app.route('/', methods=['GET'])
def index():
    """Serve HTML frontend"""
    return render_template_string(HTML_TEMPLATE)

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
    app.run(debug=False, host='0.0.0.0', port=5000)
