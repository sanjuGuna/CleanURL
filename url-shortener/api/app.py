from flask import Flask, request, jsonify,redirect
from flask_cors import CORS
import mysql.connector
import hashlib
import base64
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sanjay',
    'database': 'url_shortening_project'
}

def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        print("Database connection successful")
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def generate_short_url(long_url):
    """Generate a 5-character base64-encoded hash of the URL"""
    hash_obj = hashlib.sha256(long_url.encode())
    return base64.urlsafe_b64encode(hash_obj.digest())[:5].decode()

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """Endpoint to shorten a URL"""
    try:
        # Log raw request data for debugging
        print(f"\n[{datetime.now()}] Incoming request data: {request.data}")
        
        # Parse JSON data
        data = request.get_json(force=True, silent=True)
        if data is None:
            print("JSON parsing failed")
            return jsonify({'error': 'Invalid JSON format'}), 400
            
        print(f"Parsed JSON: {data}")
        
        # Validate URL
        long_url = data.get('url', '').strip()
        if not long_url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Connect to database
        conn = connect_db()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Check if URL already exists
            cursor.execute(
                "SELECT Short_Url FROM url_mapping WHERE Long_Url = %s",
                (long_url,)
            )
            
            if existing := cursor.fetchone():
                print(f"Found existing URL: {existing}")
                return jsonify({
                    'short_url': f"{request.host_url}{existing['Short_Url']}",
                    'exists': True
                })
            
            # Generate new short URL
            short_url = generate_short_url(long_url)
            print(f"Generated short URL: {short_url}")
            
            # Insert into database
            cursor.execute(
                "INSERT INTO url_mapping (Long_Url, Short_Url) VALUES (%s, %s)",
                (long_url, short_url)
            )
            conn.commit()
            
            return jsonify({
                'short_url': f"{request.host_url}{short_url}",
                'exists': False
            })
            
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return jsonify({'error': 'Database operation failed'}), 500
        finally:
            if conn.is_connected():
                conn.close()
                
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/<short_url>')
def redirect_short_url(short_url):
    """Redirect from short URL to original"""
    conn = connect_db()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT Long_Url FROM url_mapping WHERE Short_Url = %s",
            (short_url,)
        )
        
        if result := cursor.fetchone():
            # Update click count
            cursor.execute(
                "UPDATE url_mapping SET clicks = clicks + 1 WHERE Short_Url = %s",
                (short_url,)
            )
            conn.commit()
            return redirect(result['Long_Url'])
            
        return jsonify({'error': 'Short URL not found'}), 404
        
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database operation failed'}), 500
    finally:
        if conn.is_connected():
            conn.close()

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/test_db')
def test_db_connection():
    """Test database connection"""
    conn = connect_db()
    if conn:
        conn.close()
        return jsonify({'status': 'Database connection successful'})
    return jsonify({'error': 'Database connection failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)