# Modulo FAQ para bot MateBot de FrontEndCafé

## Lista de implementaciones:
- Consultas a FaunaDB (ver datos y agregar)
- FAQ completo y por categorías
- Detección de comando y subcomando en Discord
- Respuesta del Bot en el servidor en algún canal o por DM

## Información utilizada para desarrollo de FAQ
- [FaunaDB + Python](https://www.youtube.com/watch?v=mKPBJsoxOpU)
- [Real Python - How to Maked a Discord Bot in Python](https://realpython.com/how-to-make-a-discord-bot-python/)
- Stackoverflow

## Encargados de este módulo:
- Javier Rodriguez (Javo.py#7797)

## Estructura de BotJavo
Este bot contiene los siguientes archivos importantes para su funcionamiento:
- `BotJavo.py`: Código principal del bot. Obtiene funcionalidades a partir de `bot.add_cog(modules.FAQ(bot))`. 
- `Modules`: Carpeta en donde contiene `faq.py` y `__init__.py`
    - `faq.py` es el módulo en el que realizaremos las operaciones necesarias para obtener información del servidor.
    - `__init__.py` es un archivo que inicializa las importaciones necesarias.
- `send-faq.py`: Código para poder manipular las distintas acciones disponibles en FaunaDB.

## Funcionamiento de BotJavo
Para el módulo FAQ, estan disponibles los siguientes comandos
- !faq all: Por DM recibís el FAQ completo
- !faq general: Preguntas generales sobre el uso de Discord y el servidor
- !faq english: Preguntas relacionadas a los eventos sobre Inglés
- !faq mentoring: Dudas sobre el sistema de mentorías
- !faq coworking: Sobre Coworking en FEC
- !faq roles: Que són y como se obtienen los roles
- !faq projects: Consulta sobre los proyectos activos