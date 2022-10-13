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



@pytest.mark.parametrize("filter", ['', 'my_pets'], ids= ['empty string', 'only my pets'])
def test_get_all_pets_with_valid_key(filter):
   #""" Проверяем, что запрос всех питомцев возвращает не пустой список.
   # Для этого сначала получаем api-ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
   # запрашиваем список всех питомцев и проверяем, что список не пустой.
   # Доступное значение параметра filter - 'my_pets' либо '' """

   pytest.status, result = pf.get_list_of_pets(pytest.key, filter)

   assert len(result['pets']) > 0

def generate_string(n):
   return "x" * n

def russian_chars():
   return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

# Здесь мы взяли 20 популярных китайских иероглифов
def chinese_chars():
   return '的一是不了人我在有他这为之大来以个中上们'

def special_chars():
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

# @pytest.fixture(autouse=True)
# def get_api_key():
#     # """ Проверяем, что запрос api-ключа возвращает статус 200 и в результате содержится слово key"""
#
#     # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
#     status, pytest.key = pf.get_api_key(valid_email, valid_password)
#
#     # Сверяем полученные данные с нашими ожиданиями
#     assert status == 200
#     assert 'key' in pytest.key
#
#     yield

@pytest.mark.parametrize("filter",
                         [
                             generate_string(255)
                             , generate_string(1001)
                             , russian_chars()
                             , russian_chars().upper()
                             , chinese_chars()
                             , special_chars()
                             , 123
                         ],
                         ids=
                         [
                             '255 symbols'
                             , 'more than 1000 symbols'
                             , 'russian'
                             , 'RUSSIAN'
                             , 'chinese'
                             , 'specials'
                             , 'digit'
                         ])
def test_get_all_pets_with_negative_filter(filter):
    pytest.status, result = pf.get_list_of_pets(pytest.key, filter)

    # Проверяем статус ответа
    assert pytest.status == 500

@pytest.mark.parametrize("filter",
                         ['', 'my_pets'],
                         ids=['empty string', 'only my pets'])
def test_get_all_pets_with_valid_key(filter):
    pytest.status, result = pf.get_list_of_pets(pytest.key, filter)

    # Проверяем статус ответа
    assert pytest.status == 200
    assert len(result['pets']) > 0