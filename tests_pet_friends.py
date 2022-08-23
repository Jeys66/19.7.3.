from api import PetFrends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFrends()

def test_add_new_pets_without_photo(name='Геннадий', animal_type='крокодил', age='5'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_photo_of_pet(pet_id='', pet_photo='images/123.jpg'):
    """ Проверяем что можно добавить фото питомца по ID"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Геннадий", "ящерка", "100")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    # Добавляем фото питомца
    status, result = pf.add_photo_of_pet(auth_key, pet_id,  pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] != ""



def test_get_api_key_for_invalid_user(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа c неправильным паролем  возвращает статус 403 """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result



def test_unsuccessful_delete_self_pet():
    """Проверяем возможность удаления несуществующего питомца возвращает статус 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = "f3043661-b5a7-41b2-be7c-39e1e3141290"
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 400

def test_successful_update_self_not_pet_info(name='Нога', animal_type='голень', age=5):
    '''Тест на обновление данных несуществующего питомца возвращает статус 403'''

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

   #Если список не пустой, то пробуем обновить  имя, тип и возраст первого питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

   #проверяем что обновление данных прриводит к ошибке
    assert status == 403


def test_add_new_invalid_photo(name="Нога", animal_type="голень", age=2,pet_photo="images/000.jpg"):
    '''Тест на добавление питомца с несуществующим фото'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pet_not_animal_type(name="Бумби", animal_type="", age=1):
    """Тест на добавление питомца с пустым полем тип животного"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    assert status == 400

def test_successful_update_self_not_pet_info(name='Бемби', animal_type='олень', age=1):
    '''Тест на обновление данных несуществующего питомца возвращает статус 403'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    #проверяем что обновление данных прриводит к ошибке
    assert status == 403


def test_add_new_pet_not_photo_invalid_age(name='ХОРН', animal_type='олень', age=-12):
    '''Тест на добавление питомца с отрицательными цифрами возраста возвращает статус 400'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Запрашиваем ключ api и сохраняем в переменную auth_key
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    assert age == -12

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """ Проверяем что запрос api ключа c неправильным паролем  возвращает статус 403 """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result
