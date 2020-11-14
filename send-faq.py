# Este codigo nos sirve para poder colocar nuevos datos a FaunaDB
# Hay estas opciones:
#   - Consultar datos
#   - Agregar datos
#   - Eliminar datos (pendiente)
#   - Modificar datos (pendiente)
# Por ahora es version consola, estaria copado utilizar una GUI

#///---- Imports ----///
import re
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import os
from dotenv import load_dotenv

#///---- dot Env ----///
def env_request():
    '''
    Descripción: Cargo archivo .env y obtengo la clave.
    Precondición: Tener archivo .env en la misma carpeta que este código
    Postcondición: Retorno con la clave en DB_value y variable client del tipo FaunaClient
    '''
    load_dotenv()
    DB_value = os.getenv("FAUNADB_SECKEY")
    client = FaunaClient(secret = DB_value)
    return client


#///---- Add data ----///
def add_data(client):
    '''
    Descripción: Agrego nuevos datos a FaunaDB
    Precondición: Dar pregunta y respuesta
    Postcondición: Agrega datos nuevos a la base de datos.
    '''
    print('Ingrese categoría: ', end='')
    valueCategory = input()
    print('Ingrese pregunta: ', end='')
    valueQuestion = input()
    print('Ingrese respuesta: ', end='')
    valueAnswer = input()
    dataDict = {"Category": valueCategory, "Question": valueQuestion, "Answer": valueAnswer}
    client.query(
        q.create(
            q.collection("faqs"),
            {"data": dataDict}
        )
    )


#///---- Check data ----///
def check_data(client):
    '''
    Descripción: Imprime por consola los datos de Fauna
    Precondición: Solo debe dar la opción :D
    Poscondición: Se ven datos en consola
    '''
    # Indezacion de datos
    allfaqs = client.query(
        q.paginate(
            q.match(q.index('allfaqs'))
        )
    )
    allfaqslist = [allfaqs['data']]
    refID = re.findall('\\d+', str(allfaqslist))
    for i in range(0, len(refID), 1):
        faqDetails = client.query(q.get(q.ref(q.collection('faqs'), refID[i])))
        detailsList = [faqDetails['data']]
        print(f'\n{i})\tPregunta: {detailsList[0].get("Question")}',
                '\n\tRespuesta:', detailsList[0].get("Answer"),
                '\n\tID FaunaDB:', refID[i])

#///---- Menu ----///
def menu(client):
    opc = '1'
    while opc != '0':
        # Menu que imprime hasta dar un valor = 0
        print('\n\nMenú\n',
              '--------------------------\n',
              '1) Agregar datos\n',
              '2) Consultar datos\n',
              '3) Editar datos\n',
              '4) Eliminar datos\n',
              '0) Salir\n')
        # Input del menu
        print('\nIngrese opcion: ', end='')
        opc = input()
        # Condicionales (switch case cavernicola)
        if opc == '1':
            add_data(client)
        elif opc == '2':
            check_data(client)
        elif opc == '3':
            # edit_data()
            print('Dummy print')
        elif opc == '4':
            # remove_data()
            print('Dummy print')
        elif opc == '0':
            print('Saliendo del programa!')
        else:
            print('Opción inválida!')


#///---- Main ----///
menu(env_request())
