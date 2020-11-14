
#///---- Imports ----///
import re
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import os
from dotenv import load_dotenv

detailslist = []

load_dotenv()
DB_KEY = os.getenv("FAUNADB_SECKEY")
client = FaunaClient(secret = DB_KEY)

# Agrego datos a la BD
client.query(
    q.create(
        q.collection("faqs"), # La coleccion que se crea en la BD
        {"data": {"Category": "FEC", "Question": "Alberto","Answer": "1111"}} # Se agregan los valores de la key data
    ))

# Indezacion de datos
allfaqs = client.query(
    q.paginate(
        q.match(q.index('allfaqs'))
    )
)
allfaqslist = [allfaqs['data']]
# print(allfaqslist) # Muestra los Ref de cada dato en 'data'
result = re.findall('\\d+', str(allfaqslist))
# print(result) # Muestra los resultados de allfaqslist en strings (una cosa fea)

for i in range(0, len(result), 1):
    # print(result[i]) # Muestra los Ref de cada dato
    faqdetails = client.query(q.get(q.ref(q.collection('faqs'), result[i])))
    detailslist += [faqdetails['data']]
    # print(detailslist) # Muestro lista de diccionario con datos5
    # print('Nombre de usuario:', detailslist[0].get('Answer'),
    #         '\tContrasenia: ', detailslist[0].get('Question'))
    # dictFAQ = {'Category': detailslist[0].get('Category'),
    #                    'Question': detailslist[0].get('Question'),
    #                    'Answer': detailslist[0].get('Answer')}
    
print(detailslist)