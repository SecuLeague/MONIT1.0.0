from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

try:
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

    # Remplir le champ "password"
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
        time.sleep(5)  # Attendre quelques secondes pour que la page se charge complètement

    # Localiser l'élément .wrapper et effectuer un défilement jusqu'au bas de cet élément
    try:
        wrapper_element = wait_for_element(By.CSS_SELECTOR, ".wrapper", timeout=30)
        if wrapper_element:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", wrapper_element)
            print("Défilement jusqu'au bas de l'élément '.wrapper' effectué avec succès.")
            time.sleep(2)  # Attendre pour observer le défilement

            # Capture d'écran après le défilement
            screenshot_path = r"C:\Users\walid\Desktop\wrapper_scroll_bottom.png"
            driver.save_screenshot(screenshot_path)
            print(f"Capture d'écran enregistrée à : {screenshot_path}")
        else:
            print("Élément '.wrapper' introuvable.")
    
    except Exception as e:
        print(f"Erreur lors du défilement : {e}")

finally:
    # Fermer le navigateur
    driver.quit()
    print("Navigateur fermé.")
