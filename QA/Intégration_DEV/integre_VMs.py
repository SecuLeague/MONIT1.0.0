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
host_click_success = {}
screenshot_success = {}
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
        
        # Vérifier si la connexion a réussi en cherchant un élément du menu principal
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

    # Liste des hôtes à cliquer et capturer les écrans
    hosts_to_click = [
        {"name": "Pfsense", "hostid": "10629"},
        {"name": "Firwl-02-prj", "hostid": "10634"},
        {"name": "frhb81503ds", "hostid": "10651"},
        {"name": "codel-04-prj", "hostid": "10653"},
        {"name": "oldap-02-prj", "hostid": "10654"},
        {"name": "nacer-01-prj", "hostid": "10655"},
        {"name": "pente-01-prj", "hostid": "10658"},
        {"name": "vulma-02-prj", "hostid": "10659"},
        {"name": "osint-01-prj", "hostid": "10660"},
        {"name": "indep-03-prj", "hostid": "10662"},
        {"name": "uclid-01-prj", "hostid": "10663"},
        {"name": "Zabbix Server", "hostid": "10671"},
        {"name": "adeco-05-prj", "hostid": "10675"},
        {"name": "packetfence", "hostid": "10677"}
    ]

    for host in hosts_to_click:
        try:
            host_css_selector = driver.find_element(By.CSS_SELECTOR, f"a[data-hostid='{host['hostid']}'][onclick='view.editHost(event, this.dataset.hostid);']")
            
            # Scrolling de l'élément dans la vue
            driver.execute_script("arguments[0].scrollIntoView(true);", host_css_selector)
            
            # Attendre que l'élément soit cliquable et effectuer le clic avec JavaScript
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[data-hostid='{host['hostid']}'][onclick='view.editHost(event, this.dataset.hostid);']")))
            driver.execute_script("arguments[0].click();", host_css_selector)
            
            print(f"Clic sur '{host['name']}' effectué avec succès via JavaScript.")
            
            # Capture d'écran après le clic
            screenshot_path = f"C:\\Users\\walid\\Desktop\\{host['name']}_apres_clic.png"
            result = driver.save_screenshot(screenshot_path)
            
            if result and os.path.exists(screenshot_path):
                screenshot_success[host["name"]] = True
                host_click_success[host["name"]] = True
                print(f"Capture d'écran enregistrée sous : {screenshot_path}")
            else:
                screenshot_success[host["name"]] = False
            
            time.sleep(2)  # Attente pour observer les changements après le clic
            
        except Exception as e:
            host_click_success[host["name"]] = False
            screenshot_success[host["name"]] = False
            print(f"Erreur lors du clic sur '{host['name']}' : {e}")

except Exception as e:
    print(f"Erreur critique lors de l'exécution du test : {e}")

finally:
    # Afficher le résultat du test globalement et par hôte
    test_passed = login_success and data_collection_success and hosts_navigation_success and all(host_click_success.values()) and all(screenshot_success.values())
    
    if test_passed:
        print("\n=== TEST PASSED! ===")
        print("✅ Connexion : Réussie")
        print("✅ Navigation vers Data collection : Réussie")
        print("✅ Navigation vers Hosts : Réussie")
        
        for host in hosts_to_click:
            name = host["name"]
            print(f"✅ Clic sur '{name}' : {'Réussi' if host_click_success[name] else 'Échoué'}")
            print(f"✅ Capture d'écran pour '{name}' : {'Réussie' if screenshot_success[name] else 'Échouée'}")
    
    else:
        print("\n=== TEST FAILED! ===")
        
        for host in hosts_to_click:
            name = host["name"]
            print(f"❌ Clic sur '{name}' : {'Réussi' if host_click_success[name] else 'Échoué'}")
            print(f"❌ Capture d'écran pour '{name}' : {'Réussie' if screenshot_success[name] else 'Échouée'}")
    
    # Fermer le navigateur après toutes les étapes
    driver.quit()
    print("Navigateur fermé.")
