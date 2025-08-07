# Xero Scraper

This script uses Selenium to automate the process of logging into Xero and retrieving an access token. This is useful for accessing Xero API endpoints that are not available through the public API.

## Prerequisites

*   Python 3.6+
*   Google Chrome

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/xero-scraper.git
    cd xero-scraper
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To get your Xero access token, run the following command:

```bash
python xero_auth.py your_email@example.com your_password
```

Replace `your_email@example.com` and `your_password` with your actual Xero credentials.

### Verbose Mode

If you need to see detailed logs for debugging, you can use the `--verbose` or `-v` flag:

```bash
python xero_auth.py your_email@example.com your_password --verbose
```

## How It Works

The script automates the following steps:

1.  **Launches a browser:** It opens a new Chrome browser window (or runs in headless mode).
2.  **Navigates to the login page:** It opens the Xero login page.
3.  **Enters your credentials:** It fills in your email and password.
4.  **Handles the login process:** It clicks the login button and waits for you to complete any two-factor authentication (2FA) or CAPTCHA challenges.
5.  **Waits for the dashboard:** It waits for the main dashboard page to load.
6.  **Retrieves the access token:** It gets the access token from the browser's session storage.
7.  **Prints the token:** It prints the access token to the console.

## Disclaimer

This script is not an official Xero integration and relies on the structure of the Xero website. If the website changes, this script may break. Use it at your own risk.
