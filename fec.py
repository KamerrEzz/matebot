from PIL import Image
from io import BytesIO
from selenium import webdriver
from time import sleep

# Función que busca en la página de FEC en la sección de eventos el último evento cargado

def capturar_imagen():
    exec_path = r"E:\Descargas\Programas\geckodriver-v0.27.0-win64\geckodriver.exe"
    URL = "https://frontend.cafe/eventos"

    driver = webdriver.Firefox(executable_path=exec_path) # Abre el navegador Firefox con el driver especificado en la ruta de arriba
    driver.get(URL)

    element = driver.find_element_by_xpath("/html/body/div/div/section/div/div/div[1]/div/img") # Busca el evento pasado por parámetro

    location = element.location # Obtengo la ubicación
    size = element.size # Obtengo las dimensiones

    sleep(2)

    im = Image.open(BytesIO(driver.get_screenshot_as_png())) # Realiza la captura
    nombre = driver.find_element_by_xpath("/html/body/div/div/section/div/div/div[1]/div/div/h1") # Obtengo el nombre del evento
    name = nombre.text

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom)) # Determina los puntos de corte de la captura
    
    ruta_de_capturas = "E:\Gabriel\Python\matebot\screenshot\\"
    
    im.save(ruta_de_capturas+(name+".png"))
    
    im.show()

    driver.close()

    return ruta_de_capturas+(name+".png")
