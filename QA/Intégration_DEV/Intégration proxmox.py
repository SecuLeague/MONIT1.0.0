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
data_collection_success = False
hosts_navigation_success = False
host_click_success = False
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
        
        # Vérifier si la connexion a réussi
        try:
            dashboard_element = wait_for_element(By.CSS_SELECTOR, ".zi-dashboards", timeout=10)
            if dashboard_element:
                login_success = True
                print("Connexion réussie - Menu principal détecté.")
        except Exception as e:
            print(f"Échec de la vérification de connexion: {e}")

    # Localiser et cliquer sur l'élément "Data collection"
    try:
        data_collection_link = wait_for_element(By.LINK_TEXT, "Data collection", timeout=10)
        if data_collection_link:
            data_collection_link.click()
            print("Clic sur 'Data collection' effectué avec succès.")
            time.sleep(3)
            data_collection_success = True
        else:
            print("Élément 'Data collection' non trouvé.")
    except Exception as e:
        print(f"Erreur lors du clic sur 'Data collection' : {e}")

    # Localiser et cliquer sur l'élément "Hosts" en utilisant le CSS Selector
    try:
        hosts_css = wait_for_element(By.CSS_SELECTOR, "a[href='zabbix.php?action=host.list']", timeout=10)
        if hosts_css:
            hosts_css.click()
            print("Clic sur 'Hosts' effectué avec succès via CSS Selector.")
            time.sleep(2)
            
            # Vérifier si la navigation vers Hosts a réussi
            hosts_header = wait_for_element(By.TAG_NAME, "h1", timeout=10)
            if hosts_header and "Hosts" in hosts_header.text:
                hosts_navigation_success = True
                print("Navigation vers 'Hosts' confirmée.")
            else:
                print("Navigation vers 'Hosts' non confirmée.")
        else:
            print("Élément 'Hosts' non trouvé.")
    except Exception as e:
        print(f"Erreur lors du clic sur 'Hosts' avec CSS Selector : {e}")

    # Localiser et cliquer sur l'élément 'frhb81503ds' en utilisant le CSS Selector
    try:
        host_css_selector = wait_for_element(By.CSS_SELECTOR, "a[data-hostid='10651'][onclick='view.editHost(event, this.dataset.hostid);']", timeout=10)
        if host_css_selector:
            # Scrolling de l'élément dans la vue
            driver.execute_script("arguments[0].scrollIntoView(true);", host_css_selector)
            time.sleep(1)
            
            # Attendre que l'élément soit cliquable
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-hostid='10651'][onclick='view.editHost(event, this.dataset.hostid);']")))
            
            # Utilisation de JavaScript pour forcer le clic
            driver.execute_script("arguments[0].click();", host_css_selector)
            print("Clic sur 'frhb81503ds' effectué avec succès via JavaScript.")
            time.sleep(2)
            
            # Vérifier si l'écran d'édition de l'hôte s'est ouvert
            edit_form = wait_for_element(By.CSS_SELECTOR, ".overlay-dialogue-body", timeout=10)
            if edit_form:
                host_click_success = True
                print("Ouverture de la page d'édition de l'hôte confirmée.")
            else:
                print("Ouverture de la page d'édition de l'hôte non confirmée.")
        else:
            print("Élément 'frhb81503ds' non trouvé.")
    except Exception as e:
        print(f"Erreur lors du clic sur 'frhb81503ds' avec CSS Selector : {e}")

    # Capture d'écran après le clic
    time.sleep(3)
    try:
        screenshot_path = r"C:\Users\walid\Desktop\frhb81503ds_apres_clic.png"
        result = driver.save_screenshot(screenshot_path)
        
        if result and os.path.exists(screenshot_path):
            screenshot_success = True
            print(f"Capture d'écran enregistrée avec succès sous : {screenshot_path}")
        else:
            print(f"Échec de l'enregistrement de la capture d'écran.")
    except Exception as e:
        print(f"Erreur lors de la capture d'écran : {e}")

    # Déterminer si le test est réussi dans l'ensemble
    test_passed = login_success and data_collection_success and hosts_navigation_success and host_click_success and screenshot_success

except Exception as e:
    print(f"Erreur critique lors de l'exécution du test : {e}")

finally:
    # Afficher le résultat du test
    if test_passed:
        print("\n=== TEST PASSED! ===")
        print("✅ Connexion : Réussie")
        print("✅ Navigation vers Data collection : Réussie")
        print("✅ Navigation vers Hosts : Réussie")
        print("✅ Clic sur l'hôte frhb81503ds : Réussi")
        print("✅ Capture d'écran : Réussie")
    else:
        print("\n=== TEST FAILED! ===")
        print(f"❌ Connexion : {'Réussie' if login_success else 'Échouée'}")
        print(f"❌ Navigation vers Data collection : {'Réussie' if data_collection_success else 'Échouée'}")
        print(f"❌ Navigation vers Hosts : {'Réussie' if hosts_navigation_success else 'Échouée'}")
        print(f"❌ Clic sur l'hôte frhb81503ds : {'Réussi' if host_click_success else 'Échoué'}")
        print(f"❌ Capture d'écran : {'Réussie' if screenshot_success else 'Échouée'}")
    
    # Fermer le navigateur
    driver.quit()
    print("Navigateur fermé.")
