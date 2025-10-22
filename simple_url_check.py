import requests

urls = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.netskope.com",
    "https://nonexistent.example12345.com"
]

def check_url(url, timeout=5):
    try:
        r = requests.get(url, timeout=timeout)
        return 200 <= r.status_code < 400
    except requests.RequestException:
        return False

def main():
    for url in urls:
        ok = check_url(url)
        status = "reachable" if ok else "unreachable"
        print(f"{url}: {status}")

if __name__ == "__main__":
    main()
