from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pdfkit
import time

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Configura el controlador de Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Ejecutar en modo headless para no abrir una ventana de navegador

# Configura el servicio de ChromeDriver usando webdriver-manager
service = ChromeService(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)

# Abre la web
driver.get('https://docs.messangi.com/docs/getting-started-dep')

# Espera a que la página cargue completamente
time.sleep(5)

articulos = []

try:
    # Encuentra el primer <section> con la clase especificada
    section = driver.find_element(By.CSS_SELECTOR, 'section.Sidebar-listWrapper6Q9_yUrG906C.rm-Sidebar-section')

    # Encuentra todos los elementos con la clase especificada dentro de este <section>
    elementos = section.find_elements(By.CSS_SELECTOR, '.Sidebar-link-expandIcon2yVH6SarI6NW.icon-chevron-rightward')
    
    # Verifica que haya al menos dos elementos
    if len(elementos) > 1:
        # Itera sobre cada elemento a partir del segundo (índice 1)
        for elemento in elementos[1:]:
            try:
                elemento.click()
                time.sleep(2)  # Espera para asegurarse de que el clic tenga efecto y la nueva vista cargue
            except Exception as e:
                print(f"Error al hacer clic en el elemento: {e}")
    else:
        print("No hay suficientes elementos para hacer clic (se requieren al menos dos).")

except Exception as e:
    print(f"Error general: {e}")

try:
    # Encuentra el <ul> después de hacer clic en los elementos y extrae los enlaces
    ul_element = driver.find_element(By.CSS_SELECTOR, 'ul.Sidebar-list3cZWQLaBf9k8.rm-Sidebar-list')
    links = ul_element.find_elements(By.TAG_NAME, 'a')
    array_links = []
    # Recorre los enlaces e imprime el href
    for link in links:
        print(link.get_attribute('href'))
        ##guarda cada link.get_attribute('href') en array_links
        array_links.append(link.get_attribute('href'))

    ## Recorre array_links 
    for link in array_links:
        driver.get(link)
        time.sleep(2)  # Espera para asegurarse de que la nueva página cargue
        
        try:
            article = driver.find_element(By.CSS_SELECTOR, 'article.rm-Article')
            articulos.append(article.get_attribute('outerHTML'))
        except Exception as e:
            print(f"Error al extraer el artículo en {link}: {e}")

except Exception as e:
    print(f"Error al extraer enlaces: {e}")

# Definir estilos CSS para las imágenes
styles = """
<style>
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin-left: auto;
    margin-right: auto;
}
</style>
"""

# Incluir los estilos en el contenido HTML
html_content = styles + '<meta charset="UTF-8">' + ''.join(articulos)

options = {
    'encoding': 'UTF-8'
}

# Crear el PDF usando la configuración
if articulos:
    pdfkit.from_string(html_content, 'articulos.pdf', configuration=config, options=options)

# Mantén el navegador abierto para inspección
input("Presiona Enter para cerrar el navegador...")
driver.quit()