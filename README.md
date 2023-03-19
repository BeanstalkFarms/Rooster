# beanstalk-chat-bot

## Environment
Make sure there is a .env file in server directory
```
OPENAI_API_KEY=xyz
```

## Running server locally
```
cd server
export OPENAI_API_KEY=xyz
waitress-serve --host=0.0.0.0 --port=5001 --call index:create_app
```


# Running client locally
```
cd client
npm start
```