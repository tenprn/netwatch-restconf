import requests

def get_restconf_data(url, headers, username, password):
    try:
        response = requests.get(
            url,
            headers=headers,
            auth=(username, password),
            timeout=15,
            verify=False
        )
        if not response.ok:
            raise RuntimeError(
                f"Request failed: HTTP {response.status_code}\n"
                f"{response.text[:500]}"
            )
    except Exception as e:
        print(e)
        return None
    return response.json()
