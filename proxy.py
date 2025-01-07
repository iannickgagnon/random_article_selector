import requests

# Proxy details
proxy_host = "4.142.254.253"  # Proxy IP
proxy_port = "44119"          # Proxy Port

# Configure the proxy
proxies = {
    "http": f"http://{proxy_host}:{proxy_port}",
    "https": f"http://{proxy_host}:{proxy_port}",
}

# URL for the GET request
url = "https://httpbin.org/ip"  # Test URL to verify the proxy

try:
    # Make the GET request
    response = requests.get(url, proxies=proxies, timeout=10)
    # Print the response
    print("Response status code:", response.status_code)
    print("Response content:", response.json())
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
