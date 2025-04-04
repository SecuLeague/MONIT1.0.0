from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
        time.sleep(5)

    # Localiser et cliquer sur l'élément "Users" en utilisant XPath relatif
    try:
        users_element = driver.find_element(By.XPATH, "//a[@class='zi-users']")
        users_element.click()
        print("Clic sur 'Users' effectué avec succès.")
        time.sleep(5)
    except Exception as e:
        print(f"Erreur lors du clic sur 'Users': {e}")
        raise

    # Localiser et cliquer sur l'élément "User roles" en utilisant XPath relatif
    try:
        users_role_element = driver.find_element(By.XPATH, "(//a[normalize-space()='User roles'])[1]")
        users_role_element.click()
        print("Clic sur 'User roles' effectué avec succès.")
        time.sleep(5)

        # Capture d'écran après le clic sur "User roles"
        screenshot_path = r"C:\Users\walid\Desktop\user_roles_page.png"
        driver.save_screenshot(screenshot_path)
        print(f"Capture d'écran enregistrée à : {screenshot_path}")
        
        # Vérifier que nous sommes bien sur la page "User roles"
        expected_text = "User roles"
        # Vérifie si le texte "User roles" est présent dans le titre de la page ou dans un élément d'en-tête
        page_header = driver.find_element(By.TAG_NAME, "h1").text
        
        if expected_text in page_header:
            test_passed = True
            print("Navigation vers la page 'User roles' vérifiée.")
        else:
            print(f"Erreur: Le texte attendu '{expected_text}' n'est pas trouvé dans l'en-tête '{page_header}'")

    except Exception as e:
        print(f"Erreur lors du clic sur 'User roles': {e}")
        raise

except Exception as e:
    print(f"Erreur critique pendant l'exécution du test: {e}")

finally:
    # Afficher le résultat du test
    if test_passed:
        print("TEST PASSED!")
    else:
        print("TEST FAILED")
    
    # Fermer le navigateur
    driver.quit()
    print("Navigateur fermé.")
