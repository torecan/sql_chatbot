# sql_chatbot


docker-compose up --build

# Endpoints 

## heathcheck
localhost:1907/ 

## for sql results 
localhost:1907/chat

Header 
"Content-Type": "application/json"

-> request body 
{
  "input": "Give me data of text column and join it with another table"
}


