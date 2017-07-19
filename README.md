# DJANGO-ESIA-AUTH

## Краткое описание
Приложение содержит функционал по внедрению интеграции с ЕСИА
в механизм аутентификации и авторизации Django, а именно:

* Абстрактную модель **ESIACompatibleUser**;
* Совместиные с абстрактной моделью менеджер **EsiaCompatibleUserManager** и queryset **ESIACompatibleUserQuerySet**;
* Класс для аутентицикации **EsiaAuthBackend**;
* Базовый функционал для прохождения аутентицикации через ЕСИА **(url+view)**


## Зависимости приложения
* Приложения зависит от пакета **esia-connector** (https://github.com/sysols/esia-connector)\
  На данном этапе **esia-connector** требуется установить в разрабатываемый проект как git-подмодуль.\
  Далее, необходимо установить все зависимости **esia-connector**.\
  В будущем **esia-connector** будет оформлен как полноценный пакет с автоматически устанавливаемыми зависимостями.


## Пример использования
Пример использования представлен в проекте **sample-project** репозитория.

#### Основные моменты

##### Требуемые настройки проекта
```python
INSTALLED_APPS = [                                  # Добавить 'esia_auth' в INSTALLED_APPS
    # ...
    'esia_auth',
    # ...
]


AUTH_USER_MODEL = 'app.CustomUser'                  # CustomUser отнаследован от ESIACompatibleUser
AUTHENTICATION_BACKENDS = [
    'esia_auth.gears.EsiaAuthBackend',              # Можете отнаслодовать от EsiaAuthBackend свой бэкенд
    'django.contrib.auth.backends.ModelBackend',
]

ESIA_SETTINGS = {
    'CLIENT_ID': '',
    'REDIRECT_URL': 'http://localhost:8000/esia-auth/login',
    'CERTIFICATE': '/path/to/crt',
    'PRIVATE_KEY': '/path/to/key',
    'TOKEN_CHECK_KEY': '/path/to/pub_key',
    'SERVICE_URL': 'https://esia.gosuslugi.ru',
    'SCOPE': 'openid http://esia.gosuslugi.ru/usr_inf',
}

``` 

##### URLs
В url-схему проекта добавлена ветка
```python
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # ...
    url(r'^esia-auth/', include('esia_auth.urls', namespace='esia_auth')),  # Необходимо для работы django-esia-auth
    # ...
]
```

Теперь вы можете добавлять ссылки на авторизацию через ЕСИА. Например:
```html
{% extends "admin/login.html" %}
{% load i18n %}


{% block usertools %}
    <a href="{% url 'esia_auth:link' %}">{% trans 'Login with ESIA' %}</a>
{% endblock %}

```