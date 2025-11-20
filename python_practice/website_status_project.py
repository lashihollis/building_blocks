import requests
from requests import Response

def format_url(url):
    return url if url.startswith(('http://', 'https://')) else f'https://{url}'


def check_website(url, timeout=5):
    """
    Returns diagnostic data rather than printing it.
    """
    url = format_url(url)

    try:
        response: Response = requests.get(url, timeout=timeout)
    except Exception as e:
        return {"error": str(e), "url": url}

    return {
        "url": url,
        "status_code": response.status_code,
        "reason": response.reason,
        "elapsed_time": response.elapsed.total_seconds(),
        "headers": dict(response.headers)
    }


def display_website(data):
    """
    Prints the diagnostic data to the console.
    """
    print(f"\n=== Website diagnostics for {data['url']} ===")

    if "error" in data:
        print(f"Error: {data['error']}")
        return

    print(f"Status code  : {data['status_code']} ({data['reason']})")
    print(f"Elapsed time : {data['elapsed_time']}s")


# Example usage:
result = check_website("github.com/lashihollis/building_blocks")
display_website(result)
