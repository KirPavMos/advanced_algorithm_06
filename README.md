# advanced_algorithm_06

Для работы с базой данных используется SQLAlchemy ORM.

Для валидации данных используются Pydantic модели.

Реализованы все три требуемых метода:

GET /sellers - получение всех продавцов

PUT /sellers/{id}/update - обновление продавца

GET /sellers/{id} - получение продавца по ID

Для тестирования API вы можете использовать следующие команды (после запуска сервера):

http://localhost:8000/sellers

http://localhost:8000/sellers/1

Для запуска сервера сохраните код в файл main.py и выполните:

uvicorn main:app --reload