from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Définir le chemin complet vers chromedriver.exe
chrome_driver_path = r"C:\Users\walid\Desktop\chromedriver-win64\chromedriver.exe"

# Options pour Chrome (ignorer les erreurs SSL si nécessaire)
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')

# Créer le service pour ChromeDriver
service = Service(chrome_driver_path)

# Initialiser le WebDriver (ici Chrome)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Variable pour suivre si le test est réussi
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
        time.sleep(5)  # Attendre quelques secondes pour que la page se charge complètement

    # Localiser et cliquer sur l'élément "Users" en utilisant XPath relatif
    try:
        users_element = driver.find_element(By.XPATH, "//a[@class='zi-users']")
        users_element.click()
        print("Clic sur 'Users' effectué avec succès.")
        time.sleep(5)
    except Exception as e:
        print(f"Erreur lors du clic sur 'Users': {e}")

    # CSS Selector pour Monitoring
    try:
        monitoring_element_css = driver.find_element(By.CSS_SELECTOR, ".zi-monitoring")
        monitoring_element_css.click()
        print("Clic sur 'Monitoring' effectué avec CSS Selector.")
        time.sleep(2)
    except Exception as e:
        print(f"Erreur lors du clic sur 'Monitoring' avec CSS Selector : {e}")
        raise  # Arrêter le test si l'étape essentielle échoue

    # 1. Localiser et cliquer sur l'élément 'Latest data'
    latest_data_clicked = False
    try:
        latest_data_element_css = driver.find_element(By.CSS_SELECTOR, "a[href='zabbix.php?action=latest.view']")
        latest_data_element_css.click()
        print("Clic sur 'Latest data' effectué avec CSS Selector.")
        time.sleep(2)  # Attendre le chargement de la page après le clic
        latest_data_clicked = True
    except Exception as e:
        print(f"Erreur lors du clic sur 'Latest data' avec CSS Selector : {e}")
        raise  # Arrêter le test si l'étape essentielle échoue

    # 2. Glissade vers le bas (scroll down)
    scroll_performed = False
    try:
        driver.execute_script("window.scrollBy(0, 300);")
        print("Page déplacée vers le bas de 300 pixels.")
        time.sleep(2)
        scroll_performed = True
    except Exception as e:
        print(f"Erreur lors du défilement vers le bas : {e}")

    # 3. Prendre une capture d'écran après la glissade
    screenshot_taken = False
    try:
        screenshot_path = r"C:\Users\walid\Desktop\screenshot_latest_data.png" 
        screenshot_success = driver.save_screenshot(screenshot_path)
        
        if screenshot_success and os.path.exists(screenshot_path):
            print(f"Capture d'écran effectuée et sauvegardée sous {screenshot_path}")
            screenshot_taken = True
        else:
            print(f"Échec de la capture d'écran : le fichier n'existe pas ou n'a pas été créé correctement.")
    except Exception as e:
        print(f"Erreur lors de la capture d'écran : {e}")
    
    # Vérifier que nous sommes bien sur la page "Latest data"
    page_verification = False
    try:
        # Vérifier la présence d'un élément spécifique à la page "Latest data"
        latest_data_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Latest data')]"))
        )
        print("Page 'Latest data' vérifiée avec succès.")
        page_verification = True
    except Exception as e:
        print(f"Erreur lors de la vérification de la page 'Latest data' : {e}")
    
    # Déterminer si le test est réussi (toutes les étapes importantes sont réussies)
    test_passed = latest_data_clicked and scroll_performed and screenshot_taken and page_verification

except Exception as e:
    print(f"Erreur critique pendant l'exécution du test : {e}")

finally:
    # Afficher le résultat du test
    if test_passed:
        print("TEST PASSED!")
    else:
        print("TEST FAILED")
    
    # Fermer le navigateur
    driver.quit()
    print("Navigateur fermé.")
