from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time

apps = [
    "Slack",
    "Zoom",
    "Dropbox",
    "Netskope",
    "Microsoft Teams",
    "Notepad++"
]

def get_first_result_url(driver, query):
    driver.get("https://www.google.com")
    time.sleep(2)
    box = driver.find_element(By.NAME, "q")
    box.send_keys(query)
    box.send_keys(Keys.RETURN)
    time.sleep(2)
    results = driver.find_elements(By.XPATH, "//div[@class='yuRUbf']/a")
    if results:
        return results[0].get_attribute("href")
    return None

def check_url_reachable(url):
    try:
        r = requests.get(url, timeout=5)
        return 200 <= r.status_code < 400
    except Exception:
        return False

driver = webdriver.Chrome()
driver.set_window_size(1000, 800)

results = {}

try:
    for app in apps:
        query = f"{app} official site"
        print(f"Searching for {query} ...")
        url = get_first_result_url(driver, query)
        if not url:
            results[app] = {"url": None, "reachable": False}
            continue
        reachable = check_url_reachable(url)
        results[app] = {"url": url, "reachable": reachable}
        print(f"{app}: {url} → reachable={reachable}")
        time.sleep(3)  # delay to avoid Google rate limits
finally:
    driver.quit()

print("\nSummary:")
for app, info in results.items():
    print(f"{app}: {info['url']} ({'OK' if info['reachable'] else 'FAIL'})")
