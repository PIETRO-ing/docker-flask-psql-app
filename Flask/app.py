from flask import Flask, request
import sqlalchemy
from sqlalchemy import create_engine, text
import logging
import pandas as pd
import os


app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/view_table')
def view_table():

    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    engine=  create_engine(
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres_container:5432/{POSTGRES_DB}',
        echo=False)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logging.info("✅ Successfully connected to PostgreSQL.")
    except Exception as e:
        logging.error("❌ Failed to connect to PostgreSQL.")
        logging.error(e)
        raise

    select_query = text("SELECT * FROM users;")

    try:
        df = pd.read_sql(select_query, engine)
        return f"View the table <br><br><br><br>{df.to_html()}"
    except Exception as e:
        logging.error("Error executing query:")
        logging.error(e)
        raise


@app.route('/insert_data')
def insert_data():

    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    engine=  create_engine(
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres_container:5432/{POSTGRES_DB}',
        echo=False)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logging.info("✅ Successfully connected to PostgreSQL.")
    except Exception as e:
        logging.error("❌ Failed to connect to PostgreSQL.")
        logging.error(e)
        raise

    # query = "INSERT INTO users (city,temperature) VALUES ('Berlin', 24)"
    insert_query = text("INSERT INTO users (city, temperature) VALUES (:city, :temp)")
    params = {"city": "Berlin", "temp": 24}
    query = text("SELECT * FROM users;")

    try:
        with engine.connect() as connection:
            connection.execute(insert_query, params)
            connection.commit()
            df = pd.read_sql(query, engine)
        return f"Data inserted successfully!<br><br><br><br>{df.to_html()}"
    except Exception as e:
        logging.error("Error executing query:")
        logging.error(e)
        return "Failed to insert data"
    
@app.route('/add_data_post', methods=['POST'])
def add_user():

    data = request.json  # Expecting JSON data
    if not data:
        return "Invalid JSON data", 400
    
    city = data.get('city')
    temperature = data.get('temperature')
    # Validate data
    if not city or not temperature:
        return "Missing data", 400
    
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')

    # Connect to the database and insert data
    try:
        engine = create_engine(
            f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres_container:5432/{POSTGRES_DB}',
            echo=False
        )
        insert_query = text("INSERT INTO users (city, temperature) VALUES (:city, :temp)")
        params = {"city": city, "temp": temperature}
        select_query = text("SELECT * FROM users;")
        with engine.connect() as connection:
            connection.execute(insert_query, params)
            connection.commit()
            df = pd.read_sql(select_query, engine)
        return f"Added {city} with temperature {temperature}<br><br><br><br>{df.to_html()}", 200
    
    except Exception as e:
        app.logger.error(e)
        return "Failed to add user", 500
    
@app.route('/add_data_url', methods=['GET'])
def add_data_url():
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    city = request.args.get('city')
    temperature = request.args.get('temperature') 

    if not city or not temperature:
        return "Missing data", 400

    try:
        temperature = int(temperature)
    except (TypeError, ValueError):
        return "Invalid temperature", 400

    # Connect to the database and insert data
    try:
        engine = create_engine(
            f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres_container:5432/{POSTGRES_DB}',
            echo=False
        )
        insert_query = text("INSERT INTO users (city, temperature) VALUES (:city, :temp)")
        params = {"city": city, "temp": temperature}
        select_query = text("SELECT * FROM users;")
        with engine.connect() as connection:
            connection.execute(insert_query, params)
            connection.commit()
            df = pd.read_sql(select_query, engine)

        return f"Added {city} with temperature {temperature}<br><br><br><br>{df.to_html()}", 200
    except Exception as e:
        app.logger.error(e)
        return "Failed to add data", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# curl -X POST http://127.0.0.1:5000/add_data_post \
     # -H "Content-Type: application/json" \
     # -d '{"city": "Oslo", "temperature": 19}'





