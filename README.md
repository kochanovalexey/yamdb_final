# yamdb_final
![status yamdb_workflow.yml](https://github.com/kochanovalexey/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?event=push)
## Описание проекта
api_yamdb - проект, в котором пользователи могут делиться отзывами о художественных произведениях при помощи API. Сами произведения на сервисе не хранятся. Фукнции сервиса:

1. Создание нового пользователя и получения токена для авторизации
2. Создание отзывов и их просмотр
3. Выставление оценок произведению
4. Создание комментариев к произведением и их редактирование
5. Данный проект выполнен с использованием версии python 3.7.9.

Проект содержит три контейнера:
* db - содержит базу данных
* web - содержит файлы проекта api_yamdb
* nginx - содержит nginx

## Команды для запуска проекта:
Обновить <b>pip</b>:
```
python -m pip install --upgrade pip
```
В директории api_yamdb установить зависимости из файла <b>requirements.txt</b>:
```
pip install -r requirements.txt
```
В директории infra создайте файл <b>.env</b>:
```
nano .env
```
В текстовом редакторе ```nano``` необходимо заполнить файл <b>.env</b> по шаблону.

В директории ```infra``` выполните сборку контейнеров:
```
docker-compose up -d
```
## Шаблон наполнения env-файла:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql  
DB_NAME=postgres # имя базы данных  
POSTGRES_USER=postgres # логин для подключения к базе данных    
POSTGRES_PASSWORD=Password1! # пароль для подключения к БД (установите свой)    
DB_HOST=db # название сервиса (контейнера)  
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs
```

## Команды для заполнения базы данных приложения в контейнерах:
Выполните команды:
```
docker-compose exec web python manage.py migrate # выполнить миграции
docker-compose exec web python manage.py createsuperuser # создать суперпользователя
docker-compose exec web python manage.py collectstatic --no-input # сборка файлов со статикой
docker-compose exec web python manage.py loaddata fixtures.json # заполнение базы данных из фикстур  
```

## Примеры запросов

Неавторизованные пользователи могут просматривать описания произведений, читать отзывы и комментарии, но изменить или внести никакую информацию они не могут.

```
GET api/v1/categories/ - получить список всех публикаций.
GET api/v1/genres/ - получить список всех жанров
GET api/v1/titles/ - получить список всех произведений
GET api/v1/titles/{titles_id}/ - получить информацию о произведении
GET api/v1/titles/{titles_id}/reviews/ - получить все отзывы о произведении
GET api/v1/titles/{titles_id}/reviews/{reviews_id}/ - получить конкретный отзыв по его id к конкретному произведению номеру id (titles_id)
GET api/v1/titles/{title_id}/reviews/{review_id}/comments/ - получить все комментарии к отзыву
GET api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ - получить конкретный комментарий к отзыву по его id (comment_id)
```

---

Для того, чтобы стать авторизованным пользователям необходимо зарегистрироваться и получить токен. Сделать это можно двумя способами:

1) По адресу http://<ipсервера>/admin/ администратор сайта создает нового пользователя, а затем передает ему имя пользователя и пароль.

2) Пользователь регистрируется самостоятельно. Для этого необходимо сделать следующее:

1. Отправить POST запрос для регистрации пользователя и в теле запроса передать имя пользователя и email

```
POST api/v1/auth/signup/ 
{
  "email": "newuser@mail.ru",
  "username": "Danil"
}
```

2. Далее не указанную пользователем почту придет код подтверждения. Затем необходимо отправить еще один POST запрос с параметрами username и confirmation_code, чтобы получить token.

```
POST api/v1/auth/token/ 
{
  "username": "Danil",
  "confirmation_code": "fghkjdbcku3691"
}
```

в ответ получим следующий токен:

```
{
"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyMDk0MTQ3NywianRpIjoiODUzYzE5MTg5NzMwNDQwNTk1ZjI3ZTBmOTAzZDcxZDEiLCJ1c2VyX2lkIjoxfQ.0vJBPIUZG4MjeU_Q-mhr5Gqjx7sFlO6AShlfeINK8nA"
} 
```

В случае утраты токена или истечения его срока годности необходимо отправить повторный POST запрос на адрес api/v1/auth/token/, указав username и confirmation_code


3. В программе Postman перейти в раздел Headers и в поле "KEY" указать "Authorization", а в поле "Value" указать "Bearer <token>". Это позволит вам использовать API в качестве авторизованного пользователя.

---

Авторизованные пользователи могут оставлять свои отзывы о произведениях и комментировать отзывы других пользователей

Примеры запросов:

1. Для создания отзыва в теле запроса указывается текст отзыва и оценка пользователя (в диапазоне от 1 до 10):


```
POST /api/v1/titles/{title_id}/reviews/ 
{
  "text": "new review",
  "score": "5"
}
```
в ответ получим:
  
```
[{
  "id": 0,
  "text": "new review",
  "author": "Danil",
  "score": 5,
  "pub_date": "2019-08-24T14:15:22Z"
}
{
  "id": 1,
  "text": "new review 2",
  "author": "Danil",
  "score": 6,
  "pub_date": "2019-08-24T14:15:25Z"
}]
```

2. Для внесения изменение или удаления отзыва в адресе запроса указыввается id отзыва и, если вы обладаете соответствующим уровнем доступа, то сможете внести изменения или удалить отзыв):
  
```
GET(PATCH,DELETE) /api/v1/titles/{title_id}/reviews/{review_id}/
```
Для обновления отзыва обязательно должно в теле запроса указать параметры "text" и "score"

В ответ на GET запрос получим:
 
```
{
  "id": 0,
  "text": "new review",
  "author": "Danil",
  "score": 5,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
  


3. Для создания комментария к отзыву в теле запроса указыввается текст комментария:
  
```
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
{
  "text": "new comment"
}
```

В ответ получим:
  
```
  {
  "id": 0,
  "text": "new comment,
  "author": "Danil",
  "pub_date": "2019-08-24T14:15:22Z"
  }
```
  
4. Для обновления и удаления комментария необходимо в адресной строке указать id комментария и, если у вас есть соответствующие права, то вы сможете изменить или удалить комментарий. Для внесения изменений в теле запроса необходимо указать поле "text"
  
```
GET(PATCH,DELETE) /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

В ответ на GET запрос получим:
  
```
{
  "id": 0,
  "text": "new comment",
  "author": "Danil",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


Также пользователь может получить данные о своей учетной записи и изменить их путем отправки GET или PATCH запроса по адресу /api/v1/users/me/


Все дальнейшие операции вы сможете выполнять только обладая правами Администратора и вышею


5. Для получения списка всех пользователей необходимо отправить GET запрос по адресу /api/v1/users/.
  
  
6. Для добавления нового пользователя необходимо отправить POST запрос по адресу. В качестве роли (role) можно выбрать 1 из 3 предустановленных значений: user, moderator, admin. Без указания данного параметра пользователю будет присовена роль user. В данном случае обязательными параметрами являются username и email.
  
```
POST /api/v1/api/v1/users/
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

7. Для получения конкретного пользователя по его username необходимо отправить GET запрос с указнием username пользователя.
  
  
```
GET /api/v1/api/v1/users/new_user/
{
  "username": "new_user",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

8. Изменение и удаление данных о пользователя осуществляется путем отправки PATCH или DELETE запроса по адресу /api/v1/api/v1/users/{username}/


9. Для добавления новой категории необходимо отправить POST запрос по адресу /api/v1/categories/
 

```
POST /api/v1/categories/
{
  "name": "new_category",
  "slug": "new_slug",
}
```

10. Для удаления категории необходимо отправить DELETE запрос
 

```
DELETE /api/v1/categories/{slug}/
```
  
11. Для добавления жанра необходимо отправить POST запрос
  
 
```
POST /api/v1/genres/
 
{
  "name": "new_genre",
  "slug": "new_slug_genre",
}
```
  
12. Для удаления жанра необходимо отправить DELETE запрос
  

```
DELETE /api/v1/genres/{slug}/
```

  
13. Для добавления нового произведения необходимо отправить POST запрос. Обязательными полями в данном случае являются name, year, genre и category
  

```
POST /api/v1/titles/

{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
  "string"
  ],
  "category": "string"
}
```

В ответ получи:
  
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {}
  ],
  "category": {
    "name": "string",
    "slug": "string"
    }
  }
```
  

14. Для частичного обновления или удаления информации о произведении необходимо отправить PATCH или DELETE запрос по адресу /api/v1/titles/{titles_id}/. Для PATCH запроса в теле передается информации о произведении, которую мы хотим изменить.


Более подробную информацию о запросах и их ответах вы сможете найти по адресу http://<ipсервера>/redoc/
  
---