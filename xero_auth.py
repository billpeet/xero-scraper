from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import json
import argparse
import os

def get_access_token(email, password, verbose=False):
    """
    Authenticates with Xero using Selenium and returns an access token.
    """
    options = webdriver.ChromeOptions()
    service = None

    if not verbose:
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = ChromeService(log_output=os.devnull)

    driver = webdriver.Chrome(options=options, service=service)
    driver.get("https://login.xero.com/")

    try:
        # Wait for the email field to be present
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "xl-form-email"))
        )
        email_field.send_keys(email)

        # Find and click the submit button
        submit_button = driver.find_element(By.ID, "xl-form-submit")
        driver.execute_script("arguments[0].click();", submit_button)

        # Wait for the password field to be present
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "xl-form-password"))
        )
        password_field.send_keys(password)

        # Find and click the login button
        login_button = driver.find_element(By.ID, "xl-form-submit")
        driver.execute_script("arguments[0].click();", login_button)

        if verbose:
            print("Please complete the login process in the browser (2FA, CAPTCHA, etc.).")
            print("The script will continue after you are redirected to the dashboard.")

        # Wait for the user to be redirected to the dashboard
        WebDriverWait(driver, 300).until(
            EC.url_contains("go.xero.com")
        )

        if verbose:
            print("Waiting for dashboard to load...")
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".mf-bank-widget-heading-large"))
        )
        if verbose:
            print("Dashboard loaded.")

        # After successful login, get the access token from session storage with retries
        session_storage_key = "oidc.user:https://identity.xero.com:xero_business_go"
        access_token = None
        retries = 5
        delay = 3  # seconds

        for i in range(retries):
            token_data_json = driver.execute_script(f"return sessionStorage.getItem('{session_storage_key}');")
            if token_data_json:
                try:
                    token_data = json.loads(token_data_json)
                    access_token = token_data.get('access_token')
                    if access_token:
                        return access_token
                except json.JSONDecodeError:
                    if verbose:
                        print(f"Attempt {i+1}/{retries}: Error decoding JSON from session storage.")
            
            if verbose:
                print(f"Attempt {i+1}/{retries}: Could not find access token. Retrying in {delay} seconds...")
            time.sleep(delay)

        if verbose:
            print("Could not find access token in session storage after multiple attempts.")
        return None

    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Xero access token.")
    parser.add_argument("email", help="Xero email address")
    parser.add_argument("password", help="Xero password")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    token = get_access_token(args.email, args.password, args.verbose)
    if token:
        print(token)
    else:
        if args.verbose:
            print("Failed to retrieve access token.")