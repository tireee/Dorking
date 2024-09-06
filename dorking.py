from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium_stealth import stealth
import random
import pytesseract
from PIL import Image
import io
import sys
from urllib.parse import quote
# import webbrowser
from rich.table import Table
from rich.live import Live

if len(sys.argv) < 2 or not any(arg in sys.argv for arg in ['--google', '--duckduckgo']):
    print("Please use one of the following options: [--google, --duckduckgo]")
    print("Example: python <filename>.py --google")
    sys.exit(1)

print("DORKING BY DD3 V1.0")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

service = ChromeService("chromedriver.exe")
options = webdriver.ChromeOptions()

options.add_argument("--headless")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-popup-blocking')
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=service, options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

user_agents = [
    # ADD MORE IF YOU WANT
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0 Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:117.0) Gecko/20100101 Firefox/117.0 Chrome/117.0.0.0 Safari/537.36'
]
    
def dorkTemplates(query,url,openweb):
    ran = random.randint(0, len(user_agents) - 1)
    options.add_argument(f'user-agent={user_agents[ran]}')
    
    link = url + f"{quote(query)}"
    driver.get(link)
    text = pytesseract.image_to_string(Image.open(io.BytesIO(driver.get_screenshot_as_png())).crop((230, 270, 700, 350)))

    if "Make sure all words are spelled correctly." in text:
        table.add_row(f"[red]{link}", "[red]No")
    else:
        table.add_row(f"[green]{link}", "[green]Yes")
        # if openweb: webbrowser.open(link);time.sleep(1) <- doesnt work

if __name__ == "__main__":
    table = Table()
    table.add_column("Urls")
    table.add_column("Content")

    with open("test.txt", "r") as file:
        dorks = file.readlines()

    duckduck_url = f"https://duckduckgo.com/?q="
    google_url = f"https://www.google.com/search?q="
    open_web=False

    with Live(table, refresh_per_second=4):
        # if "-o" in sys.argv:
        #     open_web=True
        if '--google' in sys.argv and '--duckduckgo' in sys.argv:
            for dork in dorks:
                dorkTemplates(dork,duckduck_url,open_web)
                dorkTemplates(dork,google_url,open_web)
        elif '--google' in sys.argv:
            for dork in dorks:
                dorkTemplates(dork,google_url,open_web)
        elif '--duckduckgo' in sys.argv:
            for dork in dorks:
                dorkTemplates(dork,duckduck_url,open_web)

    driver.quit()