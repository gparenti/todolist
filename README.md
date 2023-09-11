# todolist
Das ist die finale Version.

##API
Es gibt 4 API-Abfragen

Für bestimmte User:
GET /api/users/<ID>

Für alle User:
GET /api/users/

Einzelne ToDo-Items:
GET /api/getTodoItemById/<ID>

Alle ToDos:
GET /api/getAllTodos

Es gibt eine API-POST Anweisung
POST /api/users username=benutzer1 password=benutzerpasswort email=benutzer@outlook.com "about_me=Hallo, ich bin der erste Benutzer"
