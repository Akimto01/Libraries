from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def test_saucedemo_flow(headless=False):
    # Nastavení prohlížeče (Chrome)
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        # 1) Login
        driver.get("https://www.saucedemo.com/")
        wait.until(EC.visibility_of_element_located((By.ID, "user-name")))

        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # 2) Přidat item do košíku (Sauce Labs Backpack)
        backpack_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
        )
        backpack_btn.click()

        # 3) Ověřit badge „1“
        cart_badge = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        assert cart_badge.text == "1", f"Badge má být 1, ale je {cart_badge.text}"

        # 4) Otevřít košík a zkontrolovat název položky
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        item_name = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        ).text
        assert item_name == "Sauce Labs Backpack", f"Očekáván ‚Sauce Labs Backpack‘, ale je ‚{item_name}‘"

        # 5) Odebrat položku a ověřit prázdný košík
        driver.find_element(By.ID, "remove-sauce-labs-backpack").click()
        # krátká čekací smyčka – badge by měl zmizet
        time.sleep(0.5)
        badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        assert len(badges) == 0, "Košík by měl být prázdný (badge zmizí)."

        # 6) Logout
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        logout = wait.until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logout.click()

        # Kontrola, že jsme zpět na loginu
        wait.until(EC.visibility_of_element_located((By.ID, "login-button")))
        print("✅ Selenium test proběhl úspěšně.")

    except TimeoutException as e:
        print("❌ Timeout při čekání na prvek:", e)
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    test_saucedemo_flow(headless=False)  # nastav True, pokud chceš headless režim
