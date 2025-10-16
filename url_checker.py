from googlesearch import search
import requests
from typing import List, Optional

def find_url_for_app(app_name: str, num_results: int = 5) -> Optional[str]:
    """
    Use google search to get likely URL for the application.
    Returns the first URL that returns a 200-OK when checked, or the first result if none are OK.
    """
    query = f"{app_name} official site"
    for url in search(query, num_results=num_results):
        # simple heuristic: skip if it’s a google result wrapper etc.
        if url.startswith("http"):
            return url
    return None

def check_site_reachable(url: str, timeout: float = 5.0) -> bool:
    """
    Return True if HTTP GET returns status code in 200–399 range.
    """
    try:
        resp = requests.get(url, timeout=timeout)
        if 200 <= resp.status_code < 400:
            return True
        else:
            return False
    except Exception as e:
        return False

def test_applications(app_names: List[str]):
    results = {}
    for app in app_names:
        print(f"Testing {app} …")
        url = find_url_for_app(app)
        if not url:
            results[app] = {"url": None, "reachable": False}
            continue
        reachable = check_site_reachable(url)
        results[app] = {"url": url, "reachable": reachable}
    return results

if __name__ == "__main__":
    apps = [
        "Slack",
        "Zoom",
        "Dropbox",
        "Netskope",
        "Microsoft Teams",
        "Notepad++"
    ]
    res = test_applications(apps)
    for app, info in res.items():
        print(f"{app}: URL = {info['url']!r}, reachable = {info['reachable']}")
