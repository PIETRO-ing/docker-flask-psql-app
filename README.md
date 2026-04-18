# docker-flask-psql-app

curl -X POST http://127.0.0.1:5000/add_data_post \
     -H "Content-Type: application/json" \
     -d '{"city": "Oslo", "temperature": 19}'