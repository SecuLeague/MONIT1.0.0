from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Définir le chemin du chromedriver (à ajuster en fonction de l'emplacement sur votre machine)
chrome_driver_path = r"C:\Users\walid\Desktop\chromedriver-win64\chromedriver.exe"
# Options pour le navigateur (par exemple, ignorer les erreurs SSL si nécessaire)
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')

# Créer le service pour ChromeDriver
service = Service(chrome_driver_path)

# Initialiser le WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL de l'interface Web de Zabbix
url = "https://192.168.150.15/"
# Accéder à l'interface Zabbix
driver.get(url)
# Vérifier que la page de connexion de Zabbix est visible
try:
    # Attendre que le titre de la page de connexion soit présent
    WebDriverWait(driver, 10).until(EC.title_contains("Zabbix"))
    print("Page de connexion de Zabbix est accessible.")
    
    # Capture d'écran de la page de connexion
    screenshot_path = r"C:\Users\walid\Desktop\zabbix_login.png"  # Chemin où la capture sera enregistrée
    driver.save_screenshot(screenshot_path)
    print(f"Capture d'écran de la page de connexion enregistrée à {screenshot_path}.")
    
except Exception as e:
    print(f"Erreur d'accès à la page de connexion Zabbix : {e}")

# Essayer de se connecter en utilisant des identifiants de test (si nécessaire)
try:
    # Localiser les champs de connexion pour "Nom d'utilisateur" et "Mot de passe"
    username_input = driver.find_element(By.ID, "name")
    password_input = driver.find_element(By.ID, "password")
    
    # Entrer les identifiants (par exemple : Admin/zabbix)
    username_input.send_keys("Admin")
    password_input.send_keys("zabbix")
    password_input.send_keys(Keys.RETURN)  # Soumettre le formulaire
    
    # Attendre la page d'accueil du tableau de bord
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard-element")))
    print("Connexion réussie et tableau de bord affiché.")
    
    # Capture d'écran de la page d'accueil du tableau de bord
    screenshot_path_dashboard = "/path/to/screenshot_zabbix_dashboard.png"  # Modifiez ce chemin
    driver.save_screenshot(screenshot_path_dashboard)
    print(f"Capture d'écran du tableau de bord enregistrée à {screenshot_path_dashboard}.")
    
except Exception as e:
    print(f"Erreur lors de la connexion à Zabbix ou affichage du tableau de bord : {e}")

# Fermer le navigateur après l'exécution
driver.quit()
