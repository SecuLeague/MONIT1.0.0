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
# Variables pour suivre l'état du test
test_passed = False
login_success = False
navigation_to_monitoring = False
navigation_to_latest_data = False
screenshot_success = False

try:
    # Accéder au site
    #url = "https://192.168.150.15/"
    url = "https://monit-02-prj.seculeague.link/zabbix"
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
        
        # Vérifier la connexion en cherchant un élément qui n'apparaît qu'après connexion
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".zi-monitoring"))
            )
            login_success = True
            print("Connexion réussie.")
        except Exception as e:
            print(f"Échec de la connexion : {e}")

    # CSS Selector pour Monitoring
    try:
        monitoring_element_css = driver.find_element(By.CSS_SELECTOR, ".zi-monitoring")
        monitoring_element_css.click()
        print("Clic sur 'Monitoring' effectué avec CSS Selector.")
        time.sleep(2)
        navigation_to_monitoring = True
    except Exception as e:
        print(f"Erreur lors du clic sur 'Monitoring' avec CSS Selector : {e}")

    # 1. Localiser et cliquer sur l'élément 'Latest data'
    try:
        latest_data_element_css = driver.find_element(By.CSS_SELECTOR, "a[href='zabbix.php?action=latest.view']")
        latest_data_element_css.click()
        print("Clic sur 'Latest data' effectué avec CSS Selector.")
        time.sleep(2)
        
        # Vérifier que nous sommes sur la page "Latest data"
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Latest data') or contains(@class, 'latest-data-title')]"))
            )
            navigation_to_latest_data = True
            print("Navigation vers 'Latest data' confirmée.")
            
            # Prendre une capture d'écran après avoir accédé à "Latest data"
            screenshot_path = r"C:\Users\walid\Desktop\latest_data.png"
            result = driver.save_screenshot(screenshot_path)
            
            if result and os.path.exists(screenshot_path):
                screenshot_success = True
                print(f"Capture d'écran effectuée et enregistrée à : {screenshot_path}")
            else:
                print(f"Échec de la capture d'écran.")
            
        except Exception as e:
            print(f"Impossible de confirmer la navigation vers 'Latest data' : {e}")
            
    except Exception as e:
        print(f"Erreur lors du clic sur 'Latest data' avec CSS Selector : {e}")

    # Déterminer si le test est réussi
    test_passed = login_success and navigation_to_monitoring and navigation_to_latest_data and screenshot_success

except Exception as e:
    print(f"Erreur critique lors de l'exécution du test : {e}")

finally:
    # Afficher le résultat du test
    if test_passed:
        print("\n=== TEST PASSED! ===")
        print("✅ Connexion : Réussie")
        print("✅ Navigation vers Monitoring : Réussie")
        print("✅ Navigation vers Latest data : Réussie")
        print("✅ Capture d'écran : Réussie")
    else:
        print("\n=== TEST FAILED! ===")
        print(f"❌ Connexion : {'Réussie' if login_success else 'Échouée'}")
        print(f"❌ Navigation vers Monitoring : {'Réussie' if navigation_to_monitoring else 'Échouée'}")
        print(f"❌ Navigation vers Latest data : {'Réussie' if navigation_to_latest_data else 'Échouée'}")
        print(f"❌ Capture d'écran : {'Réussie' if screenshot_success else 'Échouée'}")
    
    # Fermer le navigateur
    driver.quit()
    print("Navigateur fermé.")
