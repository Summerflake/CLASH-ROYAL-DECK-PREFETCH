import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import requests
from io import BytesIO

API_TOKEN = 'Bearer API_TOKEN'

headers = {
    'Authorization': API_TOKEN,
    'Accept': 'application/json'
}

def getClanByName(clan_name, limit=50):
    params = {'name': clan_name, 'limit': limit}
    response = requests.get("https://api.clashroyale.com/v1/clans", headers=headers, params=params)
    if response.status_code == 200:
        clans = response.json().get('items', [])
        clan_tags = [clan['tag'] for clan in clans]
        return [clan_tags[i:i + 5] for i in range(0, len(clan_tags), 5)]
    return []

def getPlayerInClan(clan_groups, target_name, target_trophies):
    found_players = []
    for group in clan_groups:
        for clan_tag in group:
            encoded_tag = clan_tag.replace("#", "%23")
            url = f"https://api.clashroyale.com/v1/clans/{encoded_tag}/members"
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                continue
            for member in response.json().get("items", []):
                if (member.get("name", "").lower() == target_name.lower()
                        and member.get("trophies", 0) == target_trophies):
                    found_players.append({
                        "name": member["name"],
                        "tag": member["tag"],
                        "trophies": member["trophies"],
                        "clan_tag": clan_tag
                    })
                    return found_players
    return found_players

def getPlayerLastUsedDeck(player_tag):
    encoded_tag = player_tag.replace("#", "%23")
    url = f"https://api.clashroyale.com/v1/players/{encoded_tag}/battlelog"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        for battle in response.json():
            if 'team' in battle and battle['team']:
                cards = battle['team'][0].get('cards', [])
                return [card['name'] for card in cards]
    return []

def show_deck_images(deck):
    for widget in result_frame.winfo_children():
        widget.destroy()
    for idx, card_name in enumerate(deck):
        row, col = divmod(idx, 4)
        url_name = card_name.replace(" ", "-").replace(".", "").lower()
        image_url = f"https://royaleapi.github.io/cr-api-assets/cards/{url_name}.png"
        try:
            img_data = requests.get(image_url).content
            img = Image.open(BytesIO(img_data)).resize((100, 120))
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(result_frame, image=img_tk)
            label.image = img_tk
            label.grid(row=row, column=col, padx=5, pady=5)
        except:
            tk.Label(result_frame, text=card_name).grid(row=row, column=col)

def fetch_deck():
    clan = clan_entry.get().strip()
    username = name_entry.get().strip()
    try:
        trophies = int(trophy_entry.get().strip())
    except ValueError:
        result_label.config(text="❌ Invalid trophy count.")
        return

    result_label.config(text="🔍 Searching...")
    root.update()

    grouped = getClanByName(clan)
    matches = getPlayerInClan(grouped, username, trophies)
    if not matches:
        result_label.config(text="❌ Player not found.")
        return
    deck = getPlayerLastUsedDeck(matches[0]['tag'])
    if not deck:
        result_label.config(text="⚠️ No recent deck found.")
    else:
        result_label.config(text=f"✅ Last deck of {username}:")
        show_deck_images(deck)

def reset_fields():
    clan_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    trophy_entry.delete(0, tk.END)
    result_label.config(text="")
    for widget in result_frame.winfo_children():
        widget.destroy()

# GUI
root = tk.Tk()
root.title("Clash Royale Deck Finder")

tk.Label(root, text="Clan Name:").grid(row=0, column=0, sticky="e")
tk.Label(root, text="Player Name:").grid(row=1, column=0, sticky="e")
tk.Label(root, text="Trophies:").grid(row=2, column=0, sticky="e")

clan_entry = ttk.Entry(root, width=30)
name_entry = ttk.Entry(root, width=30)
trophy_entry = ttk.Entry(root, width=30)

clan_entry.grid(row=0, column=1)
name_entry.grid(row=1, column=1)
trophy_entry.grid(row=2, column=1)

ttk.Button(root, text="Fetch Deck", command=fetch_deck).grid(row=3, column=0, pady=10)
ttk.Button(root, text="Check Another Player", command=reset_fields).grid(row=3, column=1, pady=10)

result_label = tk.Label(root, text="", fg="blue")
result_label.grid(row=4, column=0, columnspan=2)

result_frame = tk.Frame(root)
result_frame.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
