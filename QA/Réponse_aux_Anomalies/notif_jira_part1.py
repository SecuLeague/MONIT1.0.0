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

# Variables de suivi des étapes du test
test_passed = False
login_success = False
alerts_success = False
media_types_success = False
jira_success = False

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
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((selector_type, selector_value))
            )
        except Exception as e:
            print(f"Erreur lors de l'attente de l'élément {selector_value}: {e}")
            return None

    # Connexion à Zabbix
    username_input = wait_for_element(By.CSS_SELECTOR, "input#name")
    if username_input:
        username_input.send_keys("Admin")
        print("Username saisi.")
        time.sleep(2)

    password_input = wait_for_element(By.CSS_SELECTOR, "input#password")
    if password_input:
        password_input.send_keys("zabbix")
        print("Mot de passe saisi.")
        time.sleep(2)

    login_button = wait_for_element(By.ID, "enter")
    if login_button:
        login_button.click()
        print("Clic sur le bouton Login effectué.")
        time.sleep(5)
        
        # Vérification connexion réussie
        if wait_for_element(By.CSS_SELECTOR, ".zi-dashboards"):
            login_success = True

    # Navigation vers Alertes
    try:
        alerts_css_selector = wait_for_element(By.CSS_SELECTOR, ".zi-alerts")
        driver.execute_script("arguments[0].click();", alerts_css_selector)
        print("Navigation vers 'Alertes' réussie.")
        alerts_success = True
        time.sleep(2)
    except Exception as e:
        print(f"Erreur lors de la navigation vers 'Alertes': {e}")

    # Navigation vers Media Types
    try:
        media_types_css_selector = wait_for_element(By.CSS_SELECTOR, "a[href='zabbix.php?action=mediatype.list']")
        driver.execute_script("arguments[0].click();", media_types_css_selector)
        print("Navigation vers 'Media Types' réussie.")
        media_types_success = True
        time.sleep(2)
    except Exception as e:
        print(f"Erreur lors de la navigation vers 'Media Types': {e}")

    # Navigation vers Jira-test-amal et captures d'écran
    try:
        jira_test_amal_xpath = wait_for_element(By.XPATH, "//a[normalize-space()='Jira-test-amal']")
        jira_test_amal_xpath.click()
        print("Navigation vers 'Jira-test-amal' réussie.")
        
        overlay_dialogue_body = wait_for_element(By.CLASS_NAME, "overlay-dialogue-body")
        
        if overlay_dialogue_body:
            screenshot_paths = [
                r"C:\Users\walid\Desktop\jira_test_amal_first_capture.png",
                r"C:\Users\walid\Desktop\jira_test_amal_second_capture.png",
                r"C:\Users\walid\Desktop\jira_test_amal_third_capture.png"
            ]
            
            driver.save_screenshot(screenshot_paths[0])
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight / 3;", overlay_dialogue_body)
            driver.save_screenshot(screenshot_paths[1])
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", overlay_dialogue_body)
            driver.save_screenshot(screenshot_paths[2])
            
            jira_success = all(os.path.exists(path) for path in screenshot_paths)
            if jira_success:
                print(f"Captures d'écran enregistrées avec succès : {', '.join(screenshot_paths)}")
        
        time.sleep(2)
    except Exception as e:
        print(f"Erreur lors de la navigation ou des captures d'écran Jira-test-amal: {e}")

except Exception as e:
    print(f"Erreur critique pendant l'exécution du test : {e}")

finally:
    # Déterminer si le test est globalement réussi (ignorer Operations)
    test_passed = all([
        login_success,
        alerts_success,
        media_types_success,
        jira_success,
    ])

    # Rapport final détaillé
    print("\n=== RAPPORT DE TEST ===")
    print(f"Connexion : {'✅' if login_success else '❌'}")
    print(f"Navigation Alertes : {'✅' if alerts_success else '❌'}")
    print(f"Navigation Media Types : {'✅' if media_types_success else '❌'}")
    print(f"Navigation Jira-test-amal : {'✅' if jira_success else '❌'}")

    print("\nTEST GLOBAL : ", "PASSÉ ✅" if test_passed else "ÉCHOUÉ ❌")

    # Fermer le navigateur après toutes les étapes du test.
    driver.quit()
