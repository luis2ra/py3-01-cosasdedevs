# Fuente: https://cosasdedevs.com/posts/como-crear-un-crud-en-python-parte-1-estructura-y-clase/

import os
import time
from classes.validations import Validations
from classes.contact import Contact
from classes.db_contacts import DBContacts
from prettytable import PrettyTable

# Cargamos en una variable las validaciones definidas en la clase Validations
validator = Validations()
db = DBContacts()

'''
Definición de los checks que son utilizados en los campos de la clase Contact
'''
def check_name():
    print('Inserta el nombre:')
    name = input()
    try:
        validator.validateName(name)
        return name
    except ValueError as err:
        print(err)
        check_name()


def check_surname():
    print('Inserta los apellidos:')
    surname = input()
    try:
        validator.validateSurname(surname)
        return surname
    except ValueError as err:
        print(err)
        check_surname()


def check_email():
    print('Inserta el email:')
    email = input()
    try:
        validator.validateEmail(email)
        return email
    except ValueError as err:
        print(err)
        check_email()


def check_phone():
    print('Inserta el teléfono (11 cifras sin guiones ni puntos):')
    phone = input()
    try:
        validator.validatePhone(phone)
        return phone
    except ValueError as err:
        print(err)
        check_phone()


def check_birthday():
    print('Inserta la fecha de nacimiento (DD-MM-YYYY):')
    birthday = input()
    try:
        validator.validateBirthday(birthday)
        return birthday
    except ValueError as err:
        print(err)
        check_birthday()


'''
Función que optimiza toda los checks definidos anteriormente
'''
# def check_contact_data(message, data_name):
#     print(message)
#     input_data = input()
#     try:
#         getattr(validator, f'validate{data_name.capitalize()}')(input_data)
#         return input_data
#     except ValueError as err:
#         print(err)
#         check_contact_data(message, data_name)


'''
Función que crea una instancia de la clase Contact
'''
def create_contact():
    print('CREACIÓN DE CONTACTO')
    print('*' * 50)
    name = check_name()
    surname = check_surname()
    email = check_email()
    phone = check_phone()
    birthday = check_birthday()

    contact = Contact(None, name, surname, email, phone, birthday)
    if db.save_contact(contact):
        print('Contacto insertado con éxito')
    else:
        print('Error al guardar el contacto')


''' 
Otra alternativa más óptima cuando se comprenda 
'''
# def create_contact():
#     print('CREACIÓN DE CONTACTO')
#     print('*' * 50)
#     name = check_contact_data('Inserta el nombre:', 'name')
#     surname = check_contact_data('Inserta los apellidos:', 'surname')
#     email = check_contact_data('Inserta el email:', 'email')
#     phone = check_contact_data('Inserta el teléfono (9 cifras sin guiones ni puntos):', 'phone')
#     birthday = check_contact_data('Inserta la fecha de nacimiento (YYYY-MM-DD):', 'birthday')


'''
Función que lista los contactos
'''
def list_contacts():
    list_contacts = db.list_contacts()

    if not list_contacts:
        return print('Todavía no hay contactos guardados')

    table = PrettyTable(db.get_schema().keys())
    for contact in list_contacts:
        table.add_row([
            contact.id_contact,
            contact.name,
            contact.surname,
            contact.email,
            contact.phone,
            contact.birthday
        ])

    print(table)
    print('Pulsa intro para salir')
    command = input()


'''
Menú Principal del Sistema.
'''
def print_options():
    print('AGENDA DE CONTACTOS')
    print('*' * 50)
    print('Selecciona una opción:')
    print('[C]rear contacto')
    print('[L]istado de contactos')
    print('[M]odificar contacto')
    print('[E]liminar contacto')
    print('[B]uscar contacto')
    print('[S]ALIR')


def run():
    print_options()

    command = input()
    #print(command)
    command = command.upper()

    if command == 'C':
        create_contact()
    elif command == 'L':
        list_contacts()
    elif command == 'M':
        pass
    elif command == 'E':
        pass
    elif command == 'B':
        pass
    elif command == 'S':
        os._exit(1)
    else:
        print('Comando inválido!!!')
        
    time.sleep(1)
    run()

if __name__ == "__main__":
    run()