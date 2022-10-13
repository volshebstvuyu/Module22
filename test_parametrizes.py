import json

import pytest
import requests
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


@pytest.fixture(autouse=True)
def get_api_key():
    """ Проверяем, что запрос api-ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, pytest.key = pf.get_api_key(valid_email, valid_password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in pytest.key

    yield


def generate_string(n):
    return "x" * n


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


# Здесь мы взяли 20 популярных китайских иероглифов
def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


# def add_new_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
#     """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
#     запроса и результат в формате JSON с данными добавленного питомца"""
#
#     data = MultipartEncoder(
#         fields={
#             'name': name,
#             'animal_type': animal_type,
#             'age': age
#         })
#     headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
#
#     res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
#     status = res.status_code
#     result = ""
#     try:
#         result = res.json()
#     except json.decoder.JSONDecodeError:
#         result = res.text
#     print(result)
#     return status, result

#


@pytest.mark.parametrize("name"
    , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type"
    , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age"
    , ['1']
    , ids=['min'])
def test_add_new_pet_simple_positive(name, animal_type, age):
    """Проверяем, что можно добавить питомца с различными данными"""

    pytest.status, result = pf.add_new_pet_simple(pytest.key, name, animal_type, age)

    assert pytest.status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type

@pytest.mark.parametrize("name"
    , ['']
    , ids=['empty'])
@pytest.mark.parametrize("animal_type"
    , ['']
    , ids=['empty'])
@pytest.mark.parametrize("age"
    , ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
       russian_chars().upper(), chinese_chars()]
    , ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1', 'specials',
           'russian', 'RUSSIAN', 'chinese'])
def test_add_new_pet_simple_negative(name, animal_type, age):
    pytest.status, result = pf.add_new_pet_simple(pytest.key, name, animal_type, age)
    assert pytest.status == 200
