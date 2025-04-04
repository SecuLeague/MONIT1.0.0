from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Définir le chemin complet vers chromedriver.exe
chrome_driver_path = r"C:\Users\walid\Desktop\chromedriver-win64\chromedriver.exe"

# Options pour Chrome (ignorer les erreurs SSL si nécessaire)
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')

# Créer le service pour ChromeDriver
service = Service(chrome_driver_path)

# Initialiser le WebDriver (ici Chrome)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Accéder au site
url = "https://192.168.150.15/"
driver.get(url)

# Redimensionner la fenêtre du navigateur
driver.set_window_size(1024, 768)
driver.set_window_position(0, 0)
print("Fenêtre redimensionnée et déplacée.")

# Fonction d'attente explicite pour un élément
def wait_for_element(selector_type, selector_value, timeout=30):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((selector_type, selector_value))
        )
        return element
    except Exception as e:
        print(f"Erreur lors de l'attente de l'élément {selector_value}: {e}")
        return None

# Remplir le champ "username"
username_input = wait_for_element(By.CSS_SELECTOR, "input#name", timeout=30)
if username_input:
    username_input.send_keys("Admin")
    print("Username saisi.")
    time.sleep(2)

# Attendre que le champ "password" soit visible et remplir
password_input = wait_for_element(By.CSS_SELECTOR, "input#password", timeout=30)
if password_input:
    password_input.send_keys("zabbix")
    print("Mot de passe saisi.")
    time.sleep(2)

# Cliquer sur le bouton de login
login_button = wait_for_element(By.ID, "enter", timeout=30)
if login_button:
    login_button.click()
    print("Clic sur le bouton Login effectué.")
    time.sleep(5)

# Localiser et cliquer sur l'élément "Data collection"
try:
    data_collection_link = driver.find_element(By.LINK_TEXT, "Data collection")
    data_collection_link.click()
    print("Clic sur 'Data collection' effectué avec succès.")
except Exception as e:
    print(f"Erreur lors du clic sur 'Data collection' : {e}")

time.sleep(3)

# Localiser et cliquer sur l'élément "Hosts" en utilisant le CSS Selector
try:
    hosts_css = driver.find_element(By.CSS_SELECTOR, "a[href='zabbix.php?action=host.list']")
    hosts_css.click()
    print("Clic sur 'Hosts' effectué avec succès via CSS Selector.")
except Exception as e:
    print(f"Erreur lors du clic sur 'Hosts' avec CSS Selector : {e}")

# Attendre quelques secondes pour vérifier l'action
time.sleep(2)
# **Localiser et cliquer sur l'élément 'frhb81503ds' en utilisant le CSS Selector**
try:
    host_css_selector = driver.find_element(By.CSS_SELECTOR, "a[data-hostid='10651'][onclick='view.editHost(event, this.dataset.hostid);']")
    
    # Scrolling de l'élément dans la vue
    driver.execute_script("arguments[0].scrollIntoView(true);", host_css_selector)
    
    # Attendre que l'élément soit cliquable
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-hostid='10651'][onclick='view.editHost(event, this.dataset.hostid);']")))
    
    # Utilisation de JavaScript pour forcer le clic (si un autre élément bloque le clic)
    driver.execute_script("arguments[0].click();", host_css_selector)
    print("Clic sur 'frhb81503ds' effectué avec succès via JavaScript.")
    time.sleep(2)  # Attente pour le chargement
except Exception as e:
    print(f"Erreur lors du clic sur 'frhb81503ds' avec CSS Selector : {e}")

# **Capture d'écran après le clic**
time.sleep(3)
screenshot_path = r"C:\Users\walid\Desktop\frhb81503ds_apres_clic.png"
driver.save_screenshot(screenshot_path)
print(f"Capture d'écran enregistrée sous : {screenshot_path}")
# Fermer le navigateur
driver.quit()