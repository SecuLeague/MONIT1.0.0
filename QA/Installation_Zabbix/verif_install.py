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
page_access_success = False
login_success = False
dashboard_success = False
screenshot_login_success = False
screenshot_dashboard_success = False

# Définir le chemin du chromedriver
chrome_driver_path = r"C:\Users\walid\Desktop\chromedriver-win64\chromedriver.exe"
# Options pour le navigateur
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')

# Créer le service pour ChromeDriver
service = Service(chrome_driver_path)

# Initialiser le WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # URL de l'interface Web de Zabbix
    url = "https://192.168.150.15/"
    # Accéder à l'interface Zabbix
    driver.get(url)
    
    # Vérifier que la page de connexion de Zabbix est visible
    try:
        # Attendre que le titre de la page de connexion soit présent
        WebDriverWait(driver, 10).until(EC.title_contains("Zabbix"))
        print("Page de connexion de Zabbix est accessible.")
        page_access_success = True
        
        # Capture d'écran de la page de connexion
        screenshot_path = r"C:\Users\walid\Desktop\zabbix_login.png"
        result = driver.save_screenshot(screenshot_path)
        
        if result and os.path.exists(screenshot_path):
            screenshot_login_success = True
            print(f"Capture d'écran de la page de connexion enregistrée à {screenshot_path}.")
        else:
            print("Échec de la capture d'écran de la page de connexion.")
        
    except Exception as e:
        print(f"Erreur d'accès à la page de connexion Zabbix : {e}")

    # Essayer de se connecter
    try:
        # Localiser les champs de connexion
        username_input = driver.find_element(By.ID, "name")
        password_input = driver.find_element(By.ID, "password")
        
        # Entrer les identifiants
        username_input.send_keys("Admin")
        password_input.send_keys("zabbix")
        password_input.send_keys(Keys.RETURN)  # Soumettre le formulaire
        
        # Attendre la page d'accueil du tableau de bord
        dashboard_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard-grid, .dashboard-element, .zi-dashboards"))
        )
        
        if dashboard_element:
            login_success = True
            dashboard_success = True
            print("Connexion réussie et tableau de bord affiché.")
            
            # Capture d'écran de la page d'accueil du tableau de bord
            screenshot_path_dashboard = r"C:\Users\walid\Desktop\screenshot_zabbix_dashboard.png"
            result_dashboard = driver.save_screenshot(screenshot_path_dashboard)
            
            if result_dashboard and os.path.exists(screenshot_path_dashboard):
                screenshot_dashboard_success = True
                print(f"Capture d'écran du tableau de bord enregistrée à {screenshot_path_dashboard}.")
            else:
                print("Échec de la capture d'écran du tableau de bord.")
        
    except Exception as e:
        print(f"Erreur lors de la connexion à Zabbix ou affichage du tableau de bord : {e}")

    # Déterminer si le test est globalement réussi
    test_passed = page_access_success and login_success and dashboard_success and (screenshot_login_success or screenshot_dashboard_success)

except Exception as e:
    print(f"Erreur critique pendant l'exécution du test : {e}")

finally:
    # Afficher le résultat du test
    if test_passed:
        print("\n=== TEST PASSED! ===")
        print("✅ Accès à la page de connexion : Réussi")
        print("✅ Connexion à Zabbix : Réussie")
        print("✅ Affichage du tableau de bord : Réussi")
        print(f"✅ Capture d'écran de la page de connexion : {'Réussie' if screenshot_login_success else 'Échouée'}")
        print(f"✅ Capture d'écran du tableau de bord : {'Réussie' if screenshot_dashboard_success else 'Échouée'}")
    else:
        print("\n=== TEST FAILED! ===")
        print(f"❌ Accès à la page de connexion : {'Réussi' if page_access_success else 'Échoué'}")
        print(f"❌ Connexion à Zabbix : {'Réussie' if login_success else 'Échouée'}")
        print(f"❌ Affichage du tableau de bord : {'Réussi' if dashboard_success else 'Échoué'}")
        print(f"❌ Capture d'écran de la page de connexion : {'Réussie' if screenshot_login_success else 'Échouée'}")
        print(f"❌ Capture d'écran du tableau de bord : {'Réussie' if screenshot_dashboard_success else 'Échouée'}")
    
    # Fermer le navigateur après l'exécution
    driver.quit()
    print("Navigateur fermé.")
