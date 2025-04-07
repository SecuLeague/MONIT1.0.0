from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains

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
print("Fen fenêtre redimensionnée et déplacée.")

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

# Localiser et cliquer sur l'élément "Dashboards"
try:
    # Attendre que l'élément "Dashboards" soit visible et cliquable
    dashboards_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.zi-dashboards"))
    )

    # Faire défiler jusqu'à l'élément si nécessaire
    driver.execute_script("arguments[0].scrollIntoView(true);", dashboards_element)

    # Utilisation d'ActionChains pour s'assurer que l'élément est cliqué même s'il est recouvert par un autre élément
    ActionChains(driver).move_to_element(dashboards_element).click().perform()

    print("Clic sur 'Dashboards' effectué avec succès via CSS Selector.")
except Exception as e:
    print(f"Erreur lors du clic sur 'Dashboards' avec CSS Selector : {e}")

# Attendre quelques secondes pour vérifier l'action
time.sleep(2)

# Localiser et cliquer sur l'élément avec le CSS Selector spécifique
try:
    # Attendre que l'élément avec le sélecteur spécifique soit visible et cliquable
    event_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='tr_events.php?triggerid=24851&eventid=2186799']"))
    )

    # Faire défiler jusqu'à l'élément si nécessaire
    driver.execute_script("arguments[0].scrollIntoView(true);", event_element)

    # Utilisation d'ActionChains pour s'assurer que l'élément est cliqué
    ActionChains(driver).move_to_element(event_element).click().perform()

    print("Clic sur l'élément '2025-01-13 02:45:06 AM' effectué avec succès via CSS Selector.")
except Exception as e:
    print(f"Erreur lors du clic sur l'élément '2025-01-13 02:45:06 AM' avec CSS Selector : {e}")

# Attendre quelques secondes pour vérifier l'action
time.sleep(2)

# Localiser et cliquer sur le bouton "1 action" via le CSS Selector
try:
    # Attendre que l'élément avec le sélecteur spécifique soit visible et cliquable
    action_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-icon.zi-bullet-right-with-content[data-content='1'][data-hintbox-preload='{\"type\":\"eventactions\",\"data\":{\"eventid\":\"2186799\"}}']"))
    )

    # Faire défiler jusqu'à l'élément si nécessaire
    driver.execute_script("arguments[0].scrollIntoView(true);", action_button)

    # Utilisation d'ActionChains pour s'assurer que l'élément est cliqué
    ActionChains(driver).move_to_element(action_button).click().perform()

    print("Clic sur le bouton '1 action' effectué avec succès via CSS Selector.")
except Exception as e:
    print(f"Erreur lors du clic sur le bouton '1 action' avec CSS Selector : {e}")

# Attendre 3 secondes pour vérifier l'action avant de prendre la capture d'écran
time.sleep(3)

# Prendre une capture d'écran après le clic
screenshot_path = r"C:\Users\walid\Desktop\screenshot_after_action_click.png"
driver.get_screenshot_as_file(screenshot_path)
print(f"Capture d'écran sauvegardée à l'emplacement: {screenshot_path}")

# Attendre quelques secondes pour vérifier l'action
time.sleep(2)

# Fermer le navigateur
driver.quit()
