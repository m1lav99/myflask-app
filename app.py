from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

# Параметры подключения берем из переменных окружения (это стандарт DevOps)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'strongpassword')

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT title FROM tasks;')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([t[0] for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO tasks (title) VALUES (%s)', (data['title'],))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "ok"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
