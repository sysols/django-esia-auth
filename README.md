# DJANGO-ESIA-AUTH

## Краткое описание
Приложение содержит функционал по внедрению интеграции с ЕСИА
 в механизм аутентификации и авторизации Django, а именно:
 * Абстрактную модель **ESIACompatibleUser**;
 * Совместиные с абстрактной моделью менеджер **EsiaCompatibleUserManager** и queryset **ESIACompatibleUserQuerySet**;
 * Абстрактный класс для аутентицикации **AbstractEsiaAuthBackend**;
 * Базовый функционал для прохождения аутентицикации через ЕСИА **(url+view)**