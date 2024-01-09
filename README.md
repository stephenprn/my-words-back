# my-words-back

## Deploy

### Set up docker

1. Create local volume to persist db data:
```
docker volume create pgdata
```
2. Create `.env` and `.env.compose` from templates
3. Build and run docker containers:
```
docker build -f Dockerfile -t my_words_app_container .
docker-compose --env-file .env -f docker-compose.yml up --force-recreate -d db app
```


## Django

### Add an app

```
python manage.py startapp my_app
```

## Authentication

Authentication in this project is managed with (djoser)[https://djoser.readthedocs.io/en/latest/getting_started.html]
- Create a user: `POST` request on `/auth/users/`
- Create a token: `/auth/jwt/create/` and then add received token in header `Authorization` `JWT {token}`
- Check you are connected: `/auth/users/me/`
