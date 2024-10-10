from flask import Flask, request, jsonify
from openai import OpenAI
import mysql.connector
from dotenv import dotenv_values

app = Flask(__name__)
config = dotenv_values(".env")

client = OpenAI(
    api_key=config['OPENAI_API_KEY']
)

"""Initializes OpenAI model with rules and context."""
rules = (
    "this is a pre-knowledge for you ... "
    "RULES: "
    " 'cars' table stores car details (including car_id, make, model, year, price, and created_at) "
    "while the 'invoice' table records invoice information (including invoice_id, car_id, invoice_date, total_amount, and created_at), "
    "with a foreign key relationship linking car_id in invoice to car_id in cars, enabling cascading deletes. "
    "remember these table names and columns, please keep progress about that. "
    "This is initializing and after that, all responses MUST be just SQL queries and "
    "even if the user wants to DELETE or INSERT, NEVER return INSERT or DELETE queries!"
)


def create_db_connection():
    connection = mysql.connector.connect(
        host=config['MYSQL_HOST'],
        user=config['MYSQL_USER'],
        password=config['MYSQL_PASSWORD'],
        database=config['MYSQL_DATABASE'],
    )
    return connection


def query_res(query):
    db = create_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute(query) 
    results = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(results)

@app.route("/")
def index():
    return "Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        if request.content_type != 'application/json':
            return "Content-Type must be application/json", 415       
        

        data = request.get_json()
        if not data:
            return "Invalid JSON", 400
        
        user_req = data.get("input", "")

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": rules
                },
                {
                    "role": "user",
                    "content": f"create just sql query for {user_req}, nothing more info just query",
                }
            ],
            model="gpt-3.5-turbo",
        )
        sql_query = chat_completion.choices[0].message.content or ""

        return query_res(sql_query)
    
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1907)
