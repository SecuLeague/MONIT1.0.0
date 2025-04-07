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
wrapper_found = False
scroll_success = False
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
        
        # Vérifier si la connexion a réussi en cherchant un élément qui n'apparaît qu'après connexion
        try:
            menu_element = wait_for_element(By.CSS_SELECTOR, ".zi-dashboards, .zi-monitoring", timeout=10)
            if menu_element:
                login_success = True
                print("Connexion réussie - Menu principal détecté.")
        except Exception as e:
            print(f"Échec de la vérification de connexion: {e}")

    # Localiser l'élément .wrapper et effectuer un défilement jusqu'au bas de cet élément
    try:
        wrapper_element = wait_for_element(By.CSS_SELECTOR, ".wrapper", timeout=30)
        if wrapper_element:
            wrapper_found = True
            print("Élément '.wrapper' trouvé avec succès.")
            
            # Obtenir la hauteur initiale
            initial_scroll_position = driver.execute_script("return arguments[0].scrollTop;", wrapper_element)
            
            # Effectuer le défilement
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", wrapper_element)
            print("Défilement jusqu'au bas de l'élément '.wrapper' effectué.")
            time.sleep(2)
            
            # Vérifier si le défilement a fonctionné
            final_scroll_position = driver.execute_script("return arguments[0].scrollTop;", wrapper_element)
            if final_scroll_position > initial_scroll_position:
                scroll_success = True
                print("Défilement vérifié avec succès.")
            else:
                print("Le défilement ne semble pas avoir fonctionné correctement.")

            # Capture d'écran après le défilement
            screenshot_path = r"C:\Users\walid\Desktop\wrapper_scroll_bottom.png"
            result = driver.save_screenshot(screenshot_path)
            
            if result and os.path.exists(screenshot_path):
                screenshot_success = True
                print(f"Capture d'écran enregistrée avec succès à : {screenshot_path}")
            else:
                print(f"Échec de l'enregistrement de la capture d'écran.")
        else:
            print("Élément '.wrapper' introuvable.")
    
    except Exception as e:
        print(f"Erreur lors du défilement : {e}")

    # Déterminer si le test est réussi dans l'ensemble
    test_passed = login_success and wrapper_found and scroll_success and screenshot_success

except Exception as e:
    print(f"Erreur critique lors de l'exécution du test : {e}")

finally:
    # Afficher le résultat du test
    if test_passed:
        print("\n=== TEST PASSED! ===")
        print("✅ Connexion : Réussie")
        print("✅ Élément wrapper trouvé : Réussi")
        print("✅ Défilement : Réussi")
        print("✅ Capture d'écran : Réussie")
    else:
        print("\n=== TEST FAILED! ===")
        print(f"❌ Connexion : {'Réussie' if login_success else 'Échouée'}")
        print(f"❌ Élément wrapper trouvé : {'Réussi' if wrapper_found else 'Échoué'}")
        print(f"❌ Défilement : {'Réussi' if scroll_success else 'Échoué'}")
        print(f"❌ Capture d'écran : {'Réussie' if screenshot_success else 'Échouée'}")
    
    # Fermer le navigateur
    driver.quit()
    print("Navigateur fermé.")
