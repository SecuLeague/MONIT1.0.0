from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
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

# Accéder au site
url = "https://192.168.150.15/"
driver.get(url)

# Redimensionner la fenêtre du navigateur
driver.set_window_size(1024, 768)
driver.set_window_position(0, 0)
print("Fen fenêtre redimensionnée et déplacée.")

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

# **Localiser et cliquer sur l'élément 'Alertes' en utilisant le CSS Selector**
try:
    alerts_css_selector = driver.find_element(By.CSS_SELECTOR, ".zi-alerts")
    driver.execute_script("arguments[0].scrollIntoView(true);", alerts_css_selector)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".zi-alerts")))
    driver.execute_script("arguments[0].click();", alerts_css_selector)
    print("Clic sur 'Alertes' effectué avec succès via JavaScript.")
    time.sleep(2)  # Attente pour le chargement
except Exception as e:
    print(f"Erreur lors du clic sur 'Alertes' avec CSS Selector : {e}")

# **Localiser et cliquer sur l'élément 'Media types' en utilisant le CSS Selector**
try:
    media_types_css_selector = driver.find_element(By.CSS_SELECTOR, "a[href='zabbix.php?action=mediatype.list']")
    driver.execute_script("arguments[0].scrollIntoView(true);", media_types_css_selector)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='zabbix.php?action=mediatype.list']")))
    driver.execute_script("arguments[0].click();", media_types_css_selector)
    print("Clic sur 'Media types' effectué avec succès via JavaScript.")
    time.sleep(2)  # Attente pour le chargement
except Exception as e:
    print(f"Erreur lors du clic sur 'Media types' avec CSS Selector : {e}")

# **Localiser et cliquer sur l'élément 'Jira-test-amal' en utilisant XPath**
try:
    jira_test_amal_xpath = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Jira-test-amal']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", jira_test_amal_xpath)
    jira_test_amal_xpath.click()
    print("Clic sur 'Jira-test-amal' effectué avec succès.")
    time.sleep(2)  # Attente pour le chargement
except Exception as e:
    print(f"Erreur lors du clic sur 'Jira-test-amal' avec XPath : {e}")

# **Localiser et capturer l'écran avant le défilement**
try:
    overlay_dialogue_body = wait_for_element(By.CLASS_NAME, "overlay-dialogue-body", timeout=30)
    
    if overlay_dialogue_body:
        # 1ère capture d'écran - Avant de faire défiler
        screenshot_path_1 = r"C:\Users\walid\Desktop\jira_test_amal_first_capture.png"
        driver.save_screenshot(screenshot_path_1)
        print(f"Capture d'écran 1 enregistrée sous : {screenshot_path_1}")

        # Faire défiler vers le milieu du formulaire
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight / 3;", overlay_dialogue_body)
        time.sleep(2)  # Attente pour le défilement
        
        # 2ème capture d'écran - Après avoir fait défiler vers le milieu
        screenshot_path_2 = r"C:\Users\walid\Desktop\jira_test_amal_second_capture.png"
        driver.save_screenshot(screenshot_path_2)
        print(f"Capture d'écran 2 enregistrée sous : {screenshot_path_2}")
        
        # Faire défiler vers la fin du formulaire
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", overlay_dialogue_body)
        time.sleep(2)  # Attente pour le défilement
        
        # 3ème capture d'écran - Après avoir fait défiler jusqu'en bas
        screenshot_path_3 = r"C:\Users\walid\Desktop\jira_test_amal_third_capture.png"
        driver.save_screenshot(screenshot_path_3)
        print(f"Capture d'écran 3 enregistrée sous : {screenshot_path_3}")
        
except Exception as e:
    print(f"Erreur lors de la prise des captures d'écran : {e}")

# **Fermer la fenêtre en cliquant sur 'Close'**
try:
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='overlay-dialogue-header'] button[title='Close']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
    close_button.click()
    print("Fenêtre fermée avec succès.")
    time.sleep(2)  # Attente pour s'assurer que la fermeture est effectuée
    
except Exception as e:
    print(f"Erreur lors de la fermeture de la fenêtre : {e}")
    # **Retour à la page précédente et cliquer sur 'Alertes'**
try:
    # Faire un retour arrière
    driver.back()
    print("Retour à la page précédente effectué.")
    time.sleep(2)  # Attente pour la navigation

    # Cliquer à nouveau sur 'Alertes' pour afficher son contenu
    alerts_css_selector = driver.find_element(By.CSS_SELECTOR, ".zi-alerts")
    driver.execute_script("arguments[0].scrollIntoView(true);", alerts_css_selector)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".zi-alerts")))
    driver.execute_script("arguments[0].click();", alerts_css_selector)
    print("Clic sur 'Alertes' effectué à nouveau.")
    time.sleep(2)  # Attente pour le chargement
except Exception as e:
    print(f"Erreur lors du retour et du clic sur 'Alertes' : {e}")
    # Localiser et cliquer sur l'élément 'Actions' en utilisant CSS Selector
try:
    actions_css_selector = driver.find_element(By.CSS_SELECTOR, "body > aside:nth-child(1) > div:nth-child(4) > nav:nth-child(1) > ul:nth-child(1) > li:nth-child(7) > ul:nth-child(2) > li:nth-child(1) > a:nth-child(1)")
    driver.execute_script("arguments[0].scrollIntoView(true);", actions_css_selector)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > aside:nth-child(1) > div:nth-child(4) > nav:nth-child(1) > ul:nth-child(1) > li:nth-child(7) > ul:nth-child(2) > li:nth-child(1) > a:nth-child(1)")))

    # Clic sur 'Actions'
    driver.execute_script("arguments[0].click();", actions_css_selector)
    print("Clic sur 'Actions' effectué avec succès.")
    time.sleep(3)  # Attente pour que le contenu de 'Actions' se charge

    # Affichage du contenu de l'élément 'Actions' après le clic
    # Vous pouvez adapter cette partie en fonction de ce que vous voulez afficher (par exemple : obtenir le texte ou l'HTML de l'élément)
    content_element = wait_for_element(By.CSS_SELECTOR, ".actions-content", timeout=10)  # Remplacez '.actions-content' par le bon sélecteur du contenu affiché
    if content_element:
        print("Contenu de 'Actions' affiché avec succès.")
    else:
        print("Impossible de trouver le contenu de 'Actions'.")
    
    time.sleep(2)  # Attente avant de passer à l'étape suivante

except Exception as e:
    print(f"Erreur lors du clic sur 'Actions' ou de l'affichage de son contenu : {e}")
    # Localiser et cliquer sur l'élément 'Trigger actions' en utilisant le CSS Selector
try:
    trigger_actions_css_selector = driver.find_element(By.CSS_SELECTOR, "a[href='zabbix.php?action=action.list&eventsource=0']")
    driver.execute_script("arguments[0].scrollIntoView(true);", trigger_actions_css_selector)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='zabbix.php?action=action.list&eventsource=0']")))

    # Clic sur 'Trigger actions'
    driver.execute_script("arguments[0].click();", trigger_actions_css_selector)
    print("Clic sur 'Trigger actions' effectué avec succès.")
    time.sleep(3)  # Attente pour que le contenu de 'Trigger actions' se charge

    # Affichage du contenu de 'Trigger actions' après le clic
    # Vous pouvez adapter cette partie en fonction de ce que vous voulez afficher (par exemple : obtenir le texte ou l'HTML de l'élément)
    trigger_content_element = wait_for_element(By.CSS_SELECTOR, ".trigger-actions-content", timeout=10)  # Remplacez '.trigger-actions-content' par le bon sélecteur du contenu affiché
    if trigger_content_element:
        print("Contenu de 'Trigger actions' affiché avec succès.")
    else:
        print("Impossible de trouver le contenu de 'Trigger actions'.")
    
    time.sleep(2)  # Attente avant de passer à l'étape suivante

except Exception as e:
    print(f"Erreur lors du clic sur 'Trigger actions' ou de l'affichage de son contenu : {e}")
    # Localiser et cliquer sur l'élément 'Jira' en utilisant le CSS Selector
try:
    jira_css_selector = driver.find_element(By.CSS_SELECTOR, "tbody tr:nth-child(1) td:nth-child(2) a:nth-child(1)")
    driver.execute_script("arguments[0].scrollIntoView(true);", jira_css_selector)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "tbody tr:nth-child(1) td:nth-child(2) a:nth-child(1)")))

    # Clic sur 'Jira'
    driver.execute_script("arguments[0].click();", jira_css_selector)
    print("Clic sur 'Jira' effectué avec succès.")
    time.sleep(3)  # Attente pour que le contenu de 'Jira' se charge
except Exception as e:
    print(f"Erreur lors du clic sur 'Jira' : {e}")
    # Localiser et cliquer sur l'élément 'Operations' en utilisant le CSS Selector
try:
    operations_css_selector = driver.find_element(By.CSS_SELECTOR, "#tab_action-operations-tab")
    driver.execute_script("arguments[0].scrollIntoView(true);", operations_css_selector)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#tab_action-operations-tab")))

    # Clic sur 'Operations'
    driver.execute_script("arguments[0].click();", operations_css_selector)
    print("Clic sur 'Operations' effectué avec succès.")
    time.sleep(3)  # Attente pour que le contenu de 'Operations' se charge

    # Prendre une capture d'écran du contenu de la page après le clic
    screenshot_path_operations = r"C:\Users\walid\Desktop\operations_content.png"
    driver.save_screenshot(screenshot_path_operations)
    print(f"Capture d'écran du contenu d'Operations enregistrée sous : {screenshot_path_operations}")

except Exception as e:
    print(f"Erreur lors du clic sur 'Operations' ou de la capture d'écran : {e}")
   
# Clic sur l'élément .zi-users
try:
    # Attendre que l'élément .zi-users soit visible
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".zi-users")))

    # S'assurer que l'élément est visible et dans la vue
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

    # Attendre un peu avant de cliquer
    time.sleep(1)

    # Vérifier s'il y a un overlay ou un autre élément qui recouvre l'élément
    overlay = driver.find_elements(By.CSS_SELECTOR, ".overlay-bg")
    if overlay:
        # Si un overlay existe, on essaie de le fermer ou d'attendre qu'il disparaisse
        print("Overlay détecté, fermeture en cours...")
        driver.execute_script("$('.overlay-bg').click();")
        time.sleep(1)

    # Clic sur l'élément .zi-users
    element.click()
    print("Clic sur '.zi-users' effectué avec succès.")
    time.sleep(2)

except Exception as e:
    print(f"Erreur lors du clic sur '.zi-users' : {e}")

# Localiser et cliquer sur l'élément "Users List" en utilisant XPath relatif
try:
    # Localiser le lien "Users List"
    user_list_link = driver.find_element(By.XPATH, "//a[@href='zabbix.php?action=user.list']")

    # Cliquer sur le lien "Users List"
    user_list_link.click()
    print("Clic sur 'Users List' effectué avec succès.")

    # Attente pour le chargement de la page
    time.sleep(5)

    # Capture d'écran après le clic sur le lien "Users List" (si nécessaire)
    screenshot_path = r"C:\Users\walid\Desktop\user_list_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"Capture d'écran après le clic sur 'Users List' effectuée avec succès sous : {screenshot_path}")

except Exception as e:
    # Si une erreur se produit lors du clic, afficher l'erreur
    print(f"Erreur lors du clic sur 'Users List' : {e}")
  # Localiser et cliquer sur l'élément "Dashboards" en utilisant le CSS Selector
try:
    # Attendre que l'élément soit visible et cliquable
    css_selector_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".zi-dashboards"))
    )

    # Utilisation d'ActionChains pour s'assurer que l'élément soit cliqué même si un autre élément le recouvre
    ActionChains(driver).move_to_element(css_selector_element).click().perform()

    print("Clic sur 'Dashboards' effectué avec succès via CSS Selector.")
except Exception as e:
    print(f"Erreur lors du clic sur 'Dashboards' avec CSS Selector : {e}")

# Attendre quelques secondes pour vérifier l'action
time.sleep(2)
# Localiser et cliquer sur l'élément "dashboard-grid-widget-body"
try:
    # Attendre que l'élément soit visible et cliquable
    css_selector_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.dashboard-grid-widget-contents.dashboard-widget-problems div.dashboard-grid-widget-body"))
    )

    # Faire défiler jusqu'à l'élément si nécessaire
    driver.execute_script("arguments[0].scrollIntoView(true);", css_selector_element)

    # Utilisation d'ActionChains pour s'assurer que l'élément est cliqué même s'il est recouvert par un autre élément
    ActionChains(driver).move_to_element(css_selector_element).click().perform()

    print("Clic sur l'élément 'dashboard-grid-widget-body' effectué avec succès via CSS Selector.")
except Exception as e:
    print(f"Erreur lors du clic sur l'élément 'dashboard-grid-widget-body' avec CSS Selector : {e}")

# Attendre quelques secondes pour vérifier l'action
time.sleep(2)
# Localiser et cliquer sur l'élément "Dashboards"
try:
    # Attendre que l'élément "Dashboards" soit visible et cliquable
    dashboards_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.zi-dashboards"))
    )

    # Faire défiler jusqu'à l'élément si nécessaire
    driver.execute_script("arguments[0].scrollIntoView(true);", dashboards_element)

    # Utilisation d'ActionChains pour s'assurer que l'élément est cliqué même s'il est recouvert par un autre élément
    ActionChains(driver).move_to_element(dashboards_element).click().perform()

    print("Clic sur 'Dashboards' effectué avec succès via CSS Selector.")
except Exception as e:
    print(f"Erreur lors du clic sur 'Dashboards' avec CSS Selector : {e}")

# Attendre quelques secondes pour vérifier l'action
time.sleep(2)

# Localiser et cliquer sur l'élément avec le CSS Selector spécifique
try:
    # Attendre que l'élément avec le sélecteur spécifique soit visible et cliquable
    event_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='tr_events.php?triggerid=24851&eventid=2186799']"))
    )

    # Faire défiler jusqu'à l'élément si nécessaire
    driver.execute_script("arguments[0].scrollIntoView(true);", event_element)

    # Utilisation d'ActionChains pour s'assurer que l'élément est cliqué
    ActionChains(driver).move_to_element(event_element).click().perform()

    print("Clic sur l'élément '2025-01-13 02:45:06 AM' effectué avec succès via CSS Selector.")
except Exception as e:
    print(f"Erreur lors du clic sur l'élément '2025-01-13 02:45:06 AM' avec CSS Selector : {e}")

# Attendre quelques secondes pour vérifier l'action
time.sleep(2)

# Localiser et cliquer sur le bouton "1 action" via le CSS Selector
try:
    # Attendre que l'élément avec le sélecteur spécifique soit visible et cliquable
    action_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-icon.zi-bullet-right-with-content[data-content='1'][data-hintbox-preload='{\"type\":\"eventactions\",\"data\":{\"eventid\":\"2186799\"}}']"))
    )

    # Faire défiler jusqu'à l'élément si nécessaire
    driver.execute_script("arguments[0].scrollIntoView(true);", action_button)

    # Utilisation d'ActionChains pour s'assurer que l'élément est cliqué
    ActionChains(driver).move_to_element(action_button).click().perform()

    print("Clic sur le bouton '1 action' effectué avec succès via CSS Selector.")
except Exception as e:
    print(f"Erreur lors du clic sur le bouton '1 action' avec CSS Selector : {e}")

# Attendre 3 secondes pour vérifier l'action avant de prendre la capture d'écran
time.sleep(3)

# Prendre une capture d'écran après le clic
screenshot_path = r"C:\Users\walid\Desktop\screenshot_after_action_click.png"
driver.get_screenshot_as_file(screenshot_path)
print(f"Capture d'écran sauvegardée à l'emplacement: {screenshot_path}")

# Attendre quelques secondes pour vérifier l'action
time.sleep(2)
# Fermer le navigateur
driver.quit()