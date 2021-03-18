# Bank System

Bank System to provide basic deposit and withdraw functionality to customer and view to manager.

#### To setup project through Docker 
<b>Note:</b> Make sure docker and docker-compose are pre-installed

- build Dockerfile

```docker-compose build```

- create and run container

```docker-compose up -d```



### To make migrations and migrate django models into db


- execute makemigration command

```docker-compose run web python manage.py makemigrations```

- execute migrate command

```docker-compose run web python manage.py migrate```


#### To populate system with permissions
- execute custom management command

    - when using docker

    ```docker-compose run web python manage.py populate_permissions```
    
    - whithout using docker
    
    ```python manage.py populate_permissions```


#### To setup project without docker
- execute makemigration command

```python manage.py makemigrations```

- execute migrate command

```python manage.py migrate```

- runserver

```python manage.py runserver```


#### To view endpoints on swagger 
- after running server e.g. locally access http://localhost:8000/docs/ on browser