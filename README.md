# sql_chatbot


docker-compose up --build

## Endpoints 

GET localhost:1907/  -> heathcheck

POST localhost:1907/chat  -> for sql results

Header 
"Content-Type": "application/json"

Request-Body 
{
  "input": "Give me invoice data of toyota cars"
}

