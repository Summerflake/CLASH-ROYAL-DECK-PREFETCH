import requests

# search through max 50 clans
# list clan id in groups of 5
# search for player by name % trophy group by group

# Headers
headers = {
    'Authorization': API_TOKEN,
    'Accept': 'application/json'
}

def getClanByName(clan_name, limit=50):
    params = {
        'name': clan_name,
        'limit': limit
    }

    response = requests.get("https://api.clashroyale.com/v1/clans", headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        clans = data.get('items', [])
        total = data.get('paging', {}).get('total', len(clans))

        print(f"Total matching clans: {total}")

        clan_tags = [clan['tag'] for clan in clans]
        grouped_tags = [clan_tags[i:i + 5] for i in range(0, len(clan_tags), 5)]

        for group_num, group in enumerate(grouped_tags, 1):
            print(f"Group {group_num}: {group}")
        return grouped_tags

    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return []

def getPlayerInClan(clan_groups, target_name="username", target_trophies=None):
    target_name_lower = target_name.lower()
    base_url = "https://api.clashroyale.com/v1/clans"

    print(f"\n🔍 Searching for player '{target_name}' with trophies = {target_trophies} in {len(clan_groups)} groups...")
    
    found_players = []

    for group_idx, group in enumerate(clan_groups, 1):
        print(f"\n➡️ Checking Group {group_idx} ({len(group)} clans)...")
        
        for clan_tag in group:
            encoded_tag = clan_tag.replace("#", "%23")
            url = f"{base_url}/{encoded_tag}/members"

            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"❌ Failed to fetch clan {clan_tag}: {response.status_code}")
                continue

            members = response.json().get("items", [])
            for member in members:
                player_name = member.get("name", "")
                trophies = member.get("trophies", 0)

                name_match = player_name.lower() == target_name_lower
                trophy_match = (target_trophies is None or trophies == target_trophies)

                if name_match and trophy_match:
                    player_info = {
                        "name": player_name,
                        "tag": member.get("tag"),
                        "trophies": trophies,
                        "clan_tag": clan_tag
                    }
                    found_players.append(player_info)
                    print(f"✅ Found: {player_name} | Tag: {player_info['tag']} | Trophies: {trophies} | Clan: {clan_tag}")
                    return found_players
                    
    if not found_players:
        print("\n❗ No exact matches found.")
    else:
        print(f"\n🎯 Total exact matches found: {len(found_players)}")
    
    return found_players

def getPlayerLastUsedDeck(player_tag):
    encoded_tag = player_tag.replace("#", "%23")
    url = f"https://api.clashroyale.com/v1/players/{encoded_tag}/battlelog"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to get battlelog for {player_tag}: {response.status_code}")
        return None

    battles = response.json()
    for battle in battles:
        if 'team' in battle and battle['team']:
            cards = battle['team'][0].get('cards', [])
            if cards:
                deck = [card['name'] for card in cards]
                print(f"🃏 Last used deck for {player_tag}:")
                print(", ".join(deck))
                return deck
    
    print(f"⚠️ No deck found in recent battles for {player_tag}.")
    return None

def main(clan, username, trophy):
  grouped = getClanByName(clan)
  matches = getPlayerInClan(grouped, target_name=username, target_trophies=trophy)
  print(f"Found player --> {matches[0]['tag']}")
  return getPlayerLastUsedDeck(matches[0]['tag'])

player_deck = main("CLAN_NAME", "USERNAME", TROPHY_COUNT)
print(f"Deck --> {player_deck}")