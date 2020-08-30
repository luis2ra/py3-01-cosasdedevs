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
Esta función optimiza todos los checks definidos anteriormente
'''
def check_contact_data(message, data_name, force = True):
    print(message)
    input_data = input()
    if not force and not input_data:
        return
    try:
        getattr(validator, f'validate{data_name.capitalize()}')(input_data)
        return input_data
    except ValueError as err:
        print(err)
        check_contact_data(message, data_name)


''' 
Función que crea una instancia de la clase Contact, usando la función "check_contact_data"
'''
def create_contact():
    print('CREACIÓN DE CONTACTO')
    print('*' * 50)
    name = check_contact_data('Inserta el nombre:', 'name')
    surname = check_contact_data('Inserta los apellidos:', 'surname')
    email = check_contact_data('Inserta el email:', 'email')
    phone = check_contact_data('Inserta el teléfono (9 cifras sin guiones ni puntos):', 'phone')
    birthday = check_contact_data('Inserta la fecha de nacimiento (DD-MM-YYYY):', 'birthday')

    contact = Contact(None, name, surname, email, phone, birthday)
    if db.save_contact(contact):
        print('Contacto insertado con éxito')
    else:
        print('Error al guardar el contacto')


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
Función que busca los contactos
'''
def search_contact():

    filters = {}
    print('Introduce un nombre (vacío para usar otro filtro):')
    nombre = input()
    if nombre:
        filters['NAME'] = nombre
    print('Introduce un apellido (vacío para usar otro filtro):')
    apellidos = input()
    if apellidos:
        filters['SURNAME'] = apellidos
    print('Introduce un email (vacío para usar otro filtro):')
    email = input()
    if email:
        filters['EMAIL'] = email

    try:
        list_contacts = db.search_contacts(filters)
        if not list_contacts:
            return print('No hay ningún contacto con esos criterios de búsqueda')

        _print_table_contacts(list_contacts)
    except ValueError as err:
        print(err)
        time.sleep(1)
        search_contact()


'''
Función interna que es llamada desde la opción de busqueda de contactos
'''
def _print_table_contacts(list_contacts):
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
    print('Pulsa cualquier letra para continuar')
    command = input()


'''
Función que actualiza los contactos
'''
def update_contact():

    list_contacts()

    print('Introduce el id del contacto que quieres actualizar:')
    id_object = input()

    data = {}
    nombre = check_contact_data('Introduce un nombre (vacío para mantener el nombre actual):', 'name', False)
    if nombre:
        data['NAME'] = nombre
    apellidos = check_contact_data('Introduce un apellido (vacío para mantener los apellidos actuales):', 'surname', False)
    if apellidos:
        data['SURNAME'] = apellidos
    email = check_contact_data('Introduce un email (vacío para mantener el email actual):', 'email', False)
    if email:
        data['EMAIL'] = email
    phone = check_contact_data('Introduce un teléfono (vacío para mantener el teléfono actual):', 'phone', False)
    if phone:
        data['PHONE'] = phone
    birthday = check_contact_data('Introduce una fecha de nacimiento DD-MM-YYYY (vacío para mantener la fecha actual):', 'birthday', False)
    if birthday:
        data['BIRTHDAY'] = birthday
    
    try:
        res = db.update(id_object, data)
        if res:
            print('Contacto actualizado con éxito')
    except Exception as err:
        print(err)
        time.sleep(1)
        update_contact()


'''
Función que elimina los contactos
'''
def delete_contact():
    list_contacts()

    print('Introduce el id del contacto que quieres eliminar:')
    id_object = input()
    try:
        res = db.delete(id_object)
        if res:
            print('Contacto eliminado con éxito')
    except Exception as err:
        print(err)
        time.sleep(1)
        delete_contact()


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
        update_contact()
    elif command == 'E':
        delete_contact()
    elif command == 'B':
        search_contact()
    elif command == 'S':
        os._exit(1)
    else:
        print('Comando inválido!!!')
        
    time.sleep(1)
    run()

if __name__ == "__main__":
    run()