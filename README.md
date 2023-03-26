<img src="https://user-images.githubusercontent.com/28496268/227754157-d83c4ae5-de82-43bd-9103-0751b3c268ec.svg" alt="Rooster logo" align="right" width="120" />

# Rooster

[![Discord][discord-badge]][discord-url]

[discord-badge]: https://img.shields.io/discord/880413392916054098?label=Beanstalk
[discord-url]: https://discord.gg/beanstalk

**Rooster URL: [rooster.bean.money](https://rooster.bean.money)**

## Environment
Make sure there is a .env file in server directory
```
OPENAI_API_KEY=xyz
```

## Running server locally
```
cd server
pip3 install -r requirements.txt
export OPENAI_API_KEY=xyz
waitress-serve --host=0.0.0.0 --port=5001 --call index:create_app
```


# Running client locally
```
cd client
npm start
```
