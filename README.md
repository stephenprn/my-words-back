# my-words-back

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
