from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains  # Import nécessaire pour les actions
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

# Variables pour suivre l'état du test
test_passed = False
login_success = False
dashboard_click_success = False
event_click_success = False
action_button_click_success = False
screenshot_success = False

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
        time.sleep(5)

        # Vérifier si la connexion a réussi en cherchant un élément spécifique du tableau de bord
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".zi-dashboards"))
            )
            login_success = True
            print("Connexion réussie.")
        except Exception as e:
            print(f"Erreur lors de la vérification de connexion : {e}")

    # Localiser et cliquer sur l'élément "Dashboards"
    try:
        dashboards_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.zi-dashboards"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", dashboards_element)
        ActionChains(driver).move_to_element(dashboards_element).click().perform()
        print("Clic sur 'Dashboards' effectué avec succès via CSS Selector.")
        dashboard_click_success = True
    except Exception as e:
        print(f"Erreur lors du clic sur 'Dashboards' : {e}")

    # Localiser et cliquer sur l'élément spécifique avec CSS Selector
    try:
        event_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='tr_events.php?triggerid=24851&eventid=2186799']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", event_element)
        ActionChains(driver).move_to_element(event_element).click().perform()
        print("Clic sur l'élément '2025-01-13 02:45:06 AM' effectué avec succès.")
        event_click_success = True
    except Exception as e:
        print(f"Erreur lors du clic sur l'élément '2025-01-13 02:45:06 AM' : {e}")

    # Localiser et cliquer sur le bouton "1 action"
    try:
        action_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-icon.zi-bullet-right-with-content[data-content='1'][data-hintbox-preload='{\"type\":\"eventactions\",\"data\":{\"eventid\":\"2186799\"}}']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", action_button)
        ActionChains(driver).move_to_element(action_button).click().perform()
        print("Clic sur le bouton '1 action' effectué avec succès.")
        action_button_click_success = True
    except Exception as e:
        print(f"Erreur lors du clic sur le bouton '1 action' : {e}")

    # Capture d'écran après le clic sur "1 action"
    try:
        screenshot_path = "/home/walid/Desktop/screenshot_after_action_click.png"
        driver.save_screenshot(screenshot_path)
        
        if os.path.exists(screenshot_path):
            screenshot_success = True
            print(f"Capture d'écran sauvegardée à : {screenshot_path}")
        else:
            print(f"Échec de la sauvegarde de la capture d'écran.")
        
    except Exception as e:
        print(f"Erreur lors de la capture d'écran : {e}")

finally:
    # Déterminer si le test est globalement réussi
    test_passed = all([
        login_success,
        dashboard_click_success,
        event_click_success,
        action_button_click_success,
        screenshot_success,
    ])

    # Afficher les résultats du test final
    print("\n=== RAPPORT FINAL ===")
    print(f"Connexion réussie : {'✅' if login_success else '❌'}")
    print(f"Clic sur Dashboards : {'✅' if dashboard_click_success else '❌'}")
    print(f"Clic sur événement spécifique : {'✅' if event_click_success else '❌'}")
    print(f"Clic sur bouton '1 action' : {'✅' if action_button_click_success else '❌'}")
    print(f"Capture d'écran : {'✅' if screenshot_success else '❌'}")
    
    print("\nTest global : ", "SUCCÈS ✅" if test_passed else "ÉCHEC ❌")

    # Fermer le navigateur après toutes les étapes du test.
    driver.quit()
