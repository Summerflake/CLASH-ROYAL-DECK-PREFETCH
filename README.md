# CLASH-ROYAL-DECK-PREFETCH

## Overview
A Python utility to search for Clash Royale players by name, clan, and trophy count, and retrieve their most recently used deck.

This tool supports both command-line (CLI) and graphical user interface (GUI) interactions, with automatic dependency installation. Useful for stat tracking, player scouting, or building companion tools using the official Clash Royale API.

## Features
- Search clans by name and scan up to 50 results
- Match a player by name and exact trophy count
- Fetch the last used deck from player’s battle log
- Show card images in a grid using GUI
- Python Script installer for required dependencies
- Supports both CLI and Tkinter-based UI workflows

## Dependencies
- [requests](https://pypi.org/project/requests/) (for HTTP requests)  
- [pillow](https://pypi.org/project/pillow/) (for image display in GUI)

## Installation
Instead of manually running `pip`, this project includes a helper script.

```python
python install-dependencies.py
```

Alternatively, install manually:

```bash
pip install requests
pip install pillow
```

## Usage

> ### 1) Command-Line Version (main-python.py)

![Command-Line Version](/example/main-python.png)

Launch the cli interface:
```python
python main-python.py
```

Modify the follow code:
```python
player_deck = main("CLAN_NAME", "USERNAME", TROPHY_COUNT)
print(f"Deck --> {player_deck}")
```

> ### 2) GUI Version (main-tkinter.py)

![GUI Version Image](/example/main-tkinter.png)

Launch the graphical interface:
```python
python main-tkinter.py
```

- Enter Clan Name, Player Name, and Trophies
- Press "Fetch Deck"
- If found, the player's most recent deck will be shown with card images
- "Check Another Player" resets the form

## Notes
This tool only finds exact matches for both player name and trophy count

Card images are loaded from: `https://royaleapi.github.io/cr-api-assets/cards/{card-name}.png`

API token must be set in the script under API_TOKEN = 'Bearer <your_token>' which can be registered at `https://developer.clashroyale.com/`

This will search for a specific clan and locate the player with the exact trophy count specified.

## ⚠️ Disclaimer

This project uses the **official Clash Royale API** but is not affiliated with Supercell.
Use is subject to Clash Royale API Terms of Service.

This tool is provided as-is, for **educational** and **non-commercial use** only.
