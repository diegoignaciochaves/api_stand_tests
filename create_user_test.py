import sender_stand_request
import data

def get_user_body(first_name):
    # el diccionario que contiene el cuerpo de solicitud se copia del archivo "data" (datos) para conservar los datos del diccionario de origen
    current_body = data.user_body.copy()
    # Se cambia el valor del parámetro firstName
    current_body["firstName"] = first_name #firstName es mi "x" de la funcion
    # Se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body

# def test_create_user_2_letter_in_first_name_get_success_response():
#     # La versión actualizada del cuerpo de solicitud con el nombre "Aa" se guarda en la variable "user_body"
#     user_body = get_user_body("Aa") #esto es user_body="f(x)"
#     # El resultado de la solicitud relevante se guarda en la variable "user_response"
#     user_response = sender_stand_request.post_new_user(user_body)
#
#     # Comprueba si el código de estado es 201
#     assert user_response.status_code == 201
#     # Comprueba que el campo authToken está en la respuesta y contiene un valor
#     assert user_response.json()["authToken"] != ""
#     # El resultado de la solicitud de recepción de datos de la tabla "user_model" se guarda en la variable "users_table_response"
#     users_table_response = sender_stand_request.get_users_table()
#     # El string que debe estar en el cuerpo de la respuesta para recibir datos de la tabla "users" se ve así
#     str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
#                + user_body["address"] + ",,," + user_response.json()["authToken"]
#
#     # Comprueba si el usuario o usuaria existe y es único/a
#     assert users_table_response.text.count(str_user) == 1

def positive_assert(first_name): #first_name es el firstName modificado de la copia
    user_body = get_user_body(first_name)
    user_response =  sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] !=""
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
    + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa#")

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "Has introducido un nombre de usuario no válido. " \
                                         "El nombre solo puede contener letras del alfabeto latino, " \
                                         "la longitud debe ser de 2 a 15 caracteres."


def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")


def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

def test_create_user_has_space_in_first_name_get_error_response():
     negative_assert_symbol("A Aaa")


def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("//A")


def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")


def negative_assert_no_firstname(user_body): 
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

def test_create_user_no_first_name_get_error_response():
   user_body = data.user_body.copy()
   user_body.pop("firstName")
   negative_assert_no_firstname(user_body)

def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
