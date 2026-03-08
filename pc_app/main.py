import uvicorn
import requests

def get_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    ip = get_ip()
    uvicorn.run("Server.server:app", host="127.0.0.1", port=8000)
