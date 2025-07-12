import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

# Target circuits (exact name used for image matching)
target_tracks = [
    "Albert Park Grand Prix Circuit", 
    "Bahrain International Circuit", 
    "Shanghai International Circuit", 
    "Baku City Circuit", 
    "Circuit de Barcelona-Catalunya", 
    "Circuit de Monaco", 
    "Circuit Gilles Villeneuve", 
    "Circuit Paul Ricard", 
    "Red Bull Ring", 
    "Silverstone Circuit", 
    "Hockenheimring",
    "Hungaroring",
    "Circuit de Spa-Francorchamps",
    "Autodromo Nazionale di Monza",
    "Marina Bay Street Circuit",
    "Sochi Autodrom",
    "Suzuka Circuit",
    "Circuit of the Americas", 
    "Autódromo Hermanos Rodríguez",
    "Yas Marina Circuit",
    "Autodromo Internazionale del Mugello",
    "Nürburgring",
    "Autódromo Internacional do Algarve",
    "Autodromo Enzo e Dino Ferrari",
    "Istanbul Park",
    "Circuit Park Zandvoort",
    "Losail International Circuit", 
    "Jeddah Corniche Circuit", 
    "Miami International Autodrome",
    "Las Vegas Strip Street Circuit", 
    "Autódromo José Carlos Pace"
]

# Output folder
save_folder = "selected_f1_circuit_images"
os.makedirs(save_folder, exist_ok=True)

# Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_Formula_One_circuits"
headers = {"User-Agent": "Mozilla/5.0"}

# Get page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Loop through circuit names
for track in target_tracks:
    found = False
    # Search in all rows of all wikitable tables
    for row in soup.select("table.wikitable tr"):
        if track.lower() in row.get_text(strip=True).lower():
            img = row.find("img")
            if img and img.get("src"):
                img_url = urljoin("https:", img["src"])
                filename = track.replace(" ", "_").replace("/", "_") + os.path.splitext(img_url)[-1]
                filepath = os.path.join(save_folder, filename)

                # Download image
                img_data = requests.get(img_url, headers=headers).content
                with open(filepath, "wb") as f:
                    f.write(img_data)

                print(f"✅ Saved: {filename}")
                found = True
                break
    if not found:
        print(f"❌ Not found: {track}")

print(f"\n✅ Done. Images saved in: {save_folder}")
