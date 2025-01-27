import requests

# Replace with your Infura credentials
INFURA_API_KEY = 'YOUR_INFURA_API_KEY'
INFURA_API_SECRET = 'YOUR_INFURA_API_SECRET'

def create_infura_project():
    url = "https://api.infura.io/v1/projects"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {INFURA_API_KEY}"
    }
    data = {
        "name": "Capetain-Cetriva Fork",
        "network": "mainnet"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print("Project created successfully:", response.json())
    else:
        print("Failed to create project:", response.status_code, response.text)

if __name__ == "__main__":
    create_infura_project()
