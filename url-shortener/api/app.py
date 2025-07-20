from flask import Flask,request,jsonify,redirect,render_template
from flask_cors import CORS
import mysql.connector
import hashlib
import base64

app=Flask(__name__)#initialing flask app
CORS(app)
#db configuration to connect to mysql database
db_config={
    'host':'localhost',
    'user':'root',
    'password':'sanjay',
    'database':'url_shortening_project'
}


def connect_db():
    try:
        mysql_connection = mysql.connector.connect(**db_config)
        return mysql_connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
#url shortening function
def generate_short_url(long_url):
    hash_obj=hashlib.sha256(long_url.encode())
    short_hash=base64.urlsafe_b64encode(hash_obj.digest())[:5].decode()
    # print(hash_obj.digest())
    # print(short_hash)
    return short_hash

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    Long_Url = data.get('url')
    
    if not Long_Url:
        return jsonify({'error': 'Invalid URL'}), 400
    
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    
    # Check if URL exists
    cursor.execute("SELECT Short_Url FROM url_mapping WHERE Long_Url = %s", (Long_Url,))
    existing_entry = cursor.fetchone()
    
    if existing_entry:
        conn.close()
        return jsonify({
            'Short_Url': f"{request.host_url}{existing_entry['Short_Url']}",
            'already_exists': True
        })
    
    Short_Url = generate_short_url(Long_Url)
    cursor.execute("INSERT INTO url_mapping (Long_Url, Short_Url) VALUES (%s, %s)", 
                    (Long_Url, Short_Url))
    conn.commit()
    conn.close()
    
    return jsonify({
        'Short_Url': f"{request.host_url}{Short_Url}",
        'already_exists': False
    })
