from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

# Définir le chemin complet vers GeckoDriver
gecko_driver_path = "/usr/local/bin/geckodriver"

# Vérifier l'existence de GeckoDriver
if not os.path.exists(gecko_driver_path):
    raise FileNotFoundError(f"GeckoDriver introuvable à : {gecko_driver_path}")

# Options pour Firefox
firefox_options = Options()
firefox_options.add_argument('--headless')
firefox_options.add_argument('--no-sandbox')
firefox_options.add_argument('--disable-dev-shm-usage')

# Créer le service pour Firefox
service = Service(executable_path=gecko_driver_path)

# Variables de suivi du test
test_passed = False
page_access_success = False
login_success = False
dashboard_success = False
screenshot_login_success = False
screenshot_dashboard_success = False

try:
    # Initialiser le navigateur Firefox
    driver = webdriver.Firefox(service=service, options=firefox_options)
    
    # Accéder à l'interface Zabbix
    url = "https://192.168.150.15/"
    driver.get(url)
    
    # Vérification de la page de connexion
    try:
        WebDriverWait(driver, 10).until(EC.title_contains("Zabbix"))
        print("Page de connexion accessible.")
        page_access_success = True
        
        # Capture d'écran de la page de connexion
        screenshot_path = "/home/walid/Desktop/zabbix_login.png"
        driver.save_screenshot(screenshot_path)
        screenshot_login_success = os.path.exists(screenshot_path)
        
    except Exception as e:
        print(f"Erreur page de connexion : {str(e)}")

    # Connexion
    try:
        driver.find_element(By.ID, "name").send_keys("Admin")
        driver.find_element(By.ID, "password").send_keys("zabbix" + Keys.RETURN)
        
        # Vérification connexion réussie
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard-grid"))
        )
        login_success = True
        
        # Capture d'écran du dashboard
        screenshot_path = "/home/walid/Desktop/zabbix_dashboard.png"
        driver.save_screenshot(screenshot_path)
        screenshot_dashboard_success = os.path.exists(screenshot_path)
        
    except Exception as e:
        print(f"Erreur de connexion : {str(e)}")

    # Déterminer le succès global
    test_passed = all([
        page_access_success,
        login_success,
        screenshot_login_success,
        screenshot_dashboard_success
    ])

finally:
    # Générer le rapport
    print("\n=== RAPPORT FINAL ===")
    print(f"Accès page login : {'✅' if page_access_success else '❌'}")
    print(f"Connexion réussie : {'✅' if login_success else '❌'}")
    print(f"Capture login : {'✅' if screenshot_login_success else '❌'}")
    print(f"Capture dashboard : {'✅' if screenshot_dashboard_success else '❌'}")
    print(f"\nRésultat global : {'SUCCÈS ✅' if test_passed else 'ÉCHEC ❌'}")

    # Fermeture du navigateur
    driver.quit()
