from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Définir le chemin complet vers GeckoDriver (Firefox)
gecko_driver_path = "/usr/local/bin/geckodriver"  # Chemin valide pour Fedora

# Vérifier que GeckoDriver existe
if not os.path.exists(gecko_driver_path):
    raise FileNotFoundError(f"GeckoDriver introuvable à : {gecko_driver_path}")

# Options pour Firefox (ajout des options nécessaires)
firefox_options = Options()
firefox_options.add_argument('--headless')  # Exécuter Firefox en mode headless (sans interface graphique)

# Créer le service pour GeckoDriver
service = Service(gecko_driver_path)

# Initialiser le WebDriver (ici Firefox)
try:
    driver = webdriver.Firefox(service=service, options=firefox_options)
except Exception as e:
    print(f"Erreur d'initialisation de GeckoDriver : {e}")
    exit()


# Variable pour suivre si le test est réussi
test_passed = False

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

    # Localiser et cliquer sur l'élément "Help" via le CSS Selector
    try:
        help_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'zi-help-circled') or text()='Help']"))
        )
        help_button.click()
        print("Clic sur l'élément 'Help' effectué avec succès.")
        
        # Ajouter un délai d'attente après le clic
        time.sleep(3)
        
        # Prendre une capture d'écran
        screenshot_path = r"C:\Users\walid\Desktop\screenshot_help_interface.png"
        screenshot_success = driver.save_screenshot(screenshot_path)
        
        # Vérifier si la capture d'écran a été effectuée avec succès
        if screenshot_success and os.path.exists(screenshot_path):
            test_passed = True
            print(f"Capture d'écran sauvegardée avec succès à {screenshot_path}")
        else:
            print(f"Erreur : La capture d'écran n'a pas pu être enregistrée à {screenshot_path}")

    except Exception as e:
        print(f"Erreur lors du clic sur l'élément 'Help' ou de la capture d'écran : {e}")

except Exception as e:
    print(f"Erreur critique pendant l'exécution du test : {e}")

finally:
    # Afficher le résultat du test
    if test_passed:
        print("TEST PASSED!")
    else:
        print("TEST FAILED")
    
    # Fermer le navigateur après toutes les étapes
    driver.quit()
    print("Navigateur fermé.")
