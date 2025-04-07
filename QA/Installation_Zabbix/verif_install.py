from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

# Configuration Firefox
gecko_driver_path = "/usr/local/bin/geckodriver"
screenshot_dir = "/home/walid/Desktop/zabbix_screenshots"

# Créer le dossier de captures si inexistant
os.makedirs(screenshot_dir, exist_ok=True)

# Vérifier GeckoDriver
if not os.path.exists(gecko_driver_path):
    raise FileNotFoundError(f"❌ GeckoDriver introuvable : {gecko_driver_path}")

# Options Firefox
firefox_options = Options()
firefox_options.add_argument('--headless')
firefox_options.add_argument('--no-sandbox')
firefox_options.add_argument('--disable-dev-shm-usage')

# Service Firefox
service = Service(gecko_driver_path)

# Variables de suivi
test_passed = False
page_access_success = False
login_success = False
dashboard_success = False

try:
    # Initialiser Firefox
    driver = webdriver.Firefox(service=service, options=firefox_options)
    
    # Accéder à Zabbix
    url = "https://192.168.150.15/"
    driver.get(url)
    print("Accès à l'interface Zabbix...")

    # Attente générique
    driver.implicitly_wait(10)

    # Vérification page login
    try:
        WebDriverWait(driver, 15).until(EC.title_contains("Zabbix"))
        print("✅ Page de connexion détectée")
        page_access_success = True
        
        # Capture login
        screenshot_login = os.path.join(screenshot_dir, "zabbix_login.png")
        driver.save_screenshot(screenshot_login)
        print(f"Capture login : {screenshot_login}")

    except Exception as e:
        print(f"❌ Erreur page login : {str(e)}")

    # Connexion
    try:
        driver.find_element(By.ID, "name").send_keys("Admin")
        driver.find_element(By.ID, "password").send_keys("zabbix" + Keys.RETURN)
        
        # Attendre le dashboard
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dashboard-grid"))
        )
        login_success = True
        print("✅ Connexion réussie")
        
        # Capture dashboard
        screenshot_dashboard = os.path.join(screenshot_dir, "zabbix_dashboard.png")
        driver.save_screenshot(screenshot_dashboard)
        print(f"Capture dashboard : {screenshot_dashboard}")

    except Exception as e:
        print(f"❌ Erreur connexion : {str(e)}")

    # Résultat final
    test_passed = all([page_access_success, login_success])

finally:
    # Rapport
    print("\n=== RAPPORT ===")
    print(f"Accès login : {'✅' if page_access_success else '❌'}")
    print(f"Connexion : {'✅' if login_success else '❌'}")
    print(f"Résultat global : {'SUCCÈS ✅' if test_passed else 'ÉCHEC ❌'}")

    # Fermeture
    driver.quit()
