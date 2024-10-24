from flask import Flask, request, render_template, jsonify # type: ignore
import pymysql # type: ignore

app = Flask(__name__)

# PyMySQL connection setup
db = pymysql.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    passwd="root",  # Replace with your MySQL password
    database="lead_scoring"  # Replace with your MySQL database name
)
cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id VARCHAR(255),
    name VARCHAR(255),
    company VARCHAR(255),
    title VARCHAR(255),
    gender VARCHAR(50),
    country VARCHAR(255),
    score INT DEFAULT 0
)
""")
db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    print("Form Data Received:", request.form)

    name = request.form['name']
    company = request.form['company']
    title = request.form['title']
    gender = request.form['gender']
    country = request.form['country']
    client_id = request.form['client_id']
    
    # Default score for form submission
    score = 50
    
    try:
        # Insert into database
        cursor.execute("""
            INSERT INTO leads (client_id, name, company, title, gender, country, score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (client_id, name, company, title, gender, country, score))
        db.commit()
    
        return jsonify({'message': 'Lead submitted successfully!', 'score': score})
    except Exception as e:
        print("Error inserting data:", e)
        return jsonify({'error': 'Failed to insert data.'}), 500
# Endpoint for updating score based on interactions (page views, scroll depth)
@app.route('/update_score', methods=['POST'])
def update_score():
    client_id = request.form['client_id']
    score_increment = int(request.form['score_increment'])
    
    # Update score in the database
    cursor.execute("""
        UPDATE leads SET score = score + %s WHERE client_id = %s
    """, (score_increment, client_id))
    db.commit()
    
    return jsonify({'message': 'Score updated successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
