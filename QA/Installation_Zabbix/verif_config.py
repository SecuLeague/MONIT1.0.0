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
login_success = False
users_menu_success = False
user_list_success = False
screenshot_success = False
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
        
        # Vérifier la connexion réussie en cherchant un élément du menu principal
        try:
            dashboards_element = wait_for_element(By.XPATH, "//a[contains(text(), 'Dashboards')]", timeout=10)
            if dashboards_element:
                login_success = True
                print("Connexion réussie - Menu principal détecté.")
        except Exception as e:
            print(f"Échec de la vérification de connexion: {e}")

    # Localiser et cliquer sur l'élément "Users" en utilisant XPath relatif
    try:
        users_element = wait_for_element(By.XPATH, "//a[@class='zi-users']", timeout=10)
        if users_element:
            users_element.click()
            print("Clic sur 'Users' effectué avec succès.")
            time.sleep(5)
            users_menu_success = True
        else:
            print("Élément 'Users' non trouvé.")
    except Exception as e:
        print(f"Erreur lors du clic sur 'Users': {e}")

    # Localiser et cliquer sur l'élément "Users List" en utilisant XPath relatif
    try:
        user_list_link = wait_for_element(By.XPATH, "//a[@href='zabbix.php?action=user.list']", timeout=10)
        if user_list_link:
            user_list_link.click()
            print("Clic sur 'User List' effectué avec succès.")
            time.sleep(5)
            
            # Vérifier qu'on est bien sur la page User List
            page_header = wait_for_element(By.TAG_NAME, "h1", timeout=10)
            if page_header and "Users" in page_header.text:
                user_list_success = True
                print("Navigation vers 'User List' confirmée.")
            else:
                print("Navigation vers 'User List' non confirmée.")
        else:
            print("Élément 'User List' non trouvé.")
    except Exception as e:
        print(f"Erreur lors du clic sur 'User List': {e}")

    # Prendre une capture d'écran de l'interface après le clic
    try:
        screenshot_path = r"C:\Users\walid\Desktop\users_list_interface.png"
        result = driver.save_screenshot(screenshot_path)
        
        if result and os.path.exists(screenshot_path):
            screenshot_success = True
            print(f"Capture d'écran enregistrée avec succès à {screenshot_path}.")
        else:
            print(f"Échec de l'enregistrement de la capture d'écran.")
    except Exception as e:
        print(f"Erreur lors de la capture d'écran : {e}")

    # Déterminer si le test est réussi dans l'ensemble
    test_passed = login_success and users_menu_success and user_list_success and screenshot_success

except Exception as e:
    print(f"Erreur critique lors de l'exécution du test : {e}")

finally:
    # Afficher le résultat du test
    if test_passed:
        print("\n=== TEST PASSED! ===")
        print("✅ Connexion : Réussie")
        print("✅ Navigation vers menu Users : Réussie")
        print("✅ Navigation vers User List : Réussie")
        print("✅ Capture d'écran : Réussie")
    else:
        print("\n=== TEST FAILED! ===")
        print(f"❌ Connexion : {'Réussie' if login_success else 'Échouée'}")
        print(f"❌ Navigation vers menu Users : {'Réussie' if users_menu_success else 'Échouée'}")
        print(f"❌ Navigation vers User List : {'Réussie' if user_list_success else 'Échouée'}")
        print(f"❌ Capture d'écran : {'Réussie' if screenshot_success else 'Échouée'}")
    
    # Fermer le navigateur
    driver.quit()
    print("Navigateur fermé.")
