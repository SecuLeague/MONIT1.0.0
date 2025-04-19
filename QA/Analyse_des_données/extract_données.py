from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

GECKO_DRIVER_PATH = "/usr/local/bin/geckodriver"
SCREENSHOT_PATH = r"C:\Users\walid\Desktop\latest_data.png"
ZABBIX_URL = "http://192.168.10.193/zabbix/"


def setup_driver():
    if not os.path.exists(GECKO_DRIVER_PATH):
        raise FileNotFoundError(f"GeckoDriver introuvable à : {GECKO_DRIVER_PATH}")
    options = Options()
    options.add_argument('--headless')
    service = Service(GECKO_DRIVER_PATH)
    return webdriver.Firefox(service=service, options=options)


def wait_for_element(driver, selector_type, selector_value, timeout=30):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((selector_type, selector_value))
        )
    except Exception as e:
        print(f"Erreur lors de l'attente de l'élément {selector_value}: {e}")
        return None


def login(driver):
    driver.get(ZABBIX_URL)
    driver.set_window_size(1024, 768)
    driver.set_window_position(0, 0)
    print("Fenêtre redimensionnée et déplacée.")

    username_input = wait_for_element(driver, By.CSS_SELECTOR, "input#name")
    password_input = wait_for_element(driver, By.CSS_SELECTOR, "input#password")
    login_button = wait_for_element(driver, By.ID, "enter")

    if username_input and password_input and login_button:
        username_input.send_keys("Admin")
        time.sleep(1)
        password_input.send_keys("zabbix")
        time.sleep(1)
        login_button.click()
        time.sleep(3)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".zi-monitoring"))
            )
            print("Connexion réussie.")
            return True
        except Exception as e:
            print(f"Échec de la connexion : {e}")
    return False


def navigate_to_monitoring(driver):
    try:
        monitoring = driver.find_element(By.CSS_SELECTOR, ".zi-monitoring")
        monitoring.click()
        time.sleep(2)
        print("Navigation vers 'Monitoring' réussie.")
        return True
    except Exception as e:
        print(f"Erreur lors de la navigation vers 'Monitoring' : {e}")
        return False


def navigate_to_latest_data(driver):
    try:
        latest = driver.find_element(By.CSS_SELECTOR, "a[href='zabbix.php?action=latest.view']")
        latest.click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Latest data') or contains(@class, 'latest-data-title')]"))
        )
        print("Navigation vers 'Latest data' confirmée.")
        return True
    except Exception as e:
        print(f"Erreur lors de la navigation vers 'Latest data' : {e}")
        return False


def capture_screenshot(driver, path):
    result = driver.save_screenshot(path)
    if result and os.path.exists(path):
        print(f"Capture d'écran enregistrée à : {path}")
        return True
    print("Échec de la capture d'écran.")
    return False


def main():
    test_passed = login_success = nav_monitoring = nav_latest = screenshot_ok = False

    driver = setup_driver()

    try:
        login_success = login(driver)
        if login_success:
            nav_monitoring = navigate_to_monitoring(driver)
            if nav_monitoring:
                nav_latest = navigate_to_latest_data(driver)
                if nav_latest:
                    screenshot_ok = capture_screenshot(driver, SCREENSHOT_PATH)

        test_passed = all([login_success, nav_monitoring, nav_latest, screenshot_ok])

    except Exception as e:
        print(f"Erreur critique : {e}")

    finally:
        driver.quit()
        print("Navigateur fermé.")

        print("\n=== TEST {} ===".format("PASSED ✅" if test_passed else "FAILED ❌"))
        print(f"Connexion : {'✔️' if login_success else '❌'}")
        print(f"Monitoring : {'✔️' if nav_monitoring else '❌'}")
        print(f"Latest data : {'✔️' if nav_latest else '❌'}")
        print(f"Capture : {'✔️' if screenshot_ok else '❌'}")


if __name__ == "__main__":
    main()
