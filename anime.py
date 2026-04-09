import urllib.request
import urllib.parse
import json
import sys
import time

CYAN    = "\033[96m"
YELLOW  = "\033[93m"
GREEN   = "\033[92m"
MAGENTA = "\033[95m"
RED     = "\033[91m"
BOLD    = "\033[1m"
RESET   = "\033[0m"
DIM     = "\033[2m"
WHITE   = "\033[97m"

BANNER = r"""
                 _                 _____                     _                
     /\         (_)               / ____|                   | |               
    /  \   _ __  _ _ __ ___   ___| (___   ___  __ _ _ __ ___| |__   ___ _ __  
   / /\ \ | '_ \| | '_ ` _ \ / _ \\___ \ / _ \/ _` | '__/ __| '_ \ / _ \ '__| 
  / ____ \| | | | | | | | | |  __/____) |  __/ (_| | | | (__| | | |  __/ |    
 /_/    \_\_| |_|_|_| |_| |_|\___|_____/ \___|\__,_|_|  \___|_| |_|\___|_|
"""

def divider(char="=", width=60, color=CYAN):
    print(f"{color}{char * width}{RESET}")

def make_request(url):
    req = urllib.request.Request(url, headers={"User-Agent": "AnimeInfoApp/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        print(f"\n  {RED}Network error: {e}{RESET}\n")
        return None
    except Exception as e:
        print(f"\n  {RED}Something went wrong: {e}{RESET}\n")
        return None

def fetch_anime(name):
    query = urllib.parse.urlencode({"q": name, "limit": 10})
    url = f"https://api.jikan.moe/v4/anime?{query}"
    return make_request(url)

def fetch_recommendations(anime_id):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/recommendations"
    return make_request(url)

def fetch_characters(anime_id):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/characters"
    return make_request(url)

def fetch_staff(anime_id):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/staff"
    return make_request(url)

def get_number_input(prompt, min_val, max_val):
    while True:
        try:
            raw = input(f"\n{CYAN}{BOLD}  {prompt}: {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            return None
        if not raw.isdigit():
            print(f"  {RED}Please enter a number.{RESET}")
            continue
        val = int(raw)
        if val < min_val or val > max_val:
            print(f"  {RED}Enter a number between {min_val} and {max_val}.{RESET}")
            continue
        return val

def pick_from_list(results):
    print()
    divider("-", 60, CYAN)
    print(f"  {BOLD}{CYAN}Results{RESET}  {DIM}(pick a number){RESET}")
    divider("-", 60, CYAN)

    for i, a in enumerate(results, 1):
        title = a.get("title_english") or a.get("title", "N/A")
        typ   = a.get("type", "?")
        eps   = a.get("episodes") or "?"
        score = a.get("score") or "N/A"
        year  = (a.get("aired") or {}).get("prop", {}).get("from", {}).get("year") or "?"
        print(f"  {YELLOW}{BOLD}[{i:>2}]{RESET}  {title}  "
              f"{DIM}| {typ} | {eps} eps | score: {score} | {year}{RESET}")

    divider("-", 60, CYAN)
    choice = get_number_input(f"Choose (1-{len(results)}) or 0 to go back", 0, len(results))
    if choice is None or choice == 0:
        return None
    return results[choice - 1]

def wrap_text(text, width=56):
    words = text.split()
    line = []
    lines = []
    for word in words:
        if sum(len(w) + 1 for w in line) + len(word) > width:
            lines.append(" ".join(line))
            line = [word]
        else:
            line.append(word)
    if line:
        lines.append(" ".join(line))
    return lines

def display_anime_details(a):
    title_en = a.get("title_english") or a.get("title", "N/A")
    title_jp = a.get("title", "N/A")
    anime_id   = a.get("mal_id")
    anime_type = a.get("type", "N/A")
    episodes   = a.get("episodes") or "?"
    status     = a.get("status", "N/A")
    score      = a.get("score") or "N/A"
    rank       = a.get("rank") or "N/A"
    popularity = a.get("popularity") or "N/A"
    aired      = a.get("aired", {}).get("string", "N/A")
    duration   = a.get("duration", "N/A")
    rating     = a.get("rating", "N/A")
    source     = a.get("source", "N/A")
    studios    = ", ".join(s["name"] for s in a.get("studios", [])) or "N/A"
    genres     = ", ".join(g["name"] for g in a.get("genres", [])) or "N/A"
    synopsis   = a.get("synopsis") or "No synopsis available."
    trailer    = a.get("trailer", {}).get("url") or None

    if len(synopsis) > 350:
        synopsis = synopsis[:350].rsplit(" ", 1)[0] + "..."

    print()
    divider("=", 60, YELLOW)
    print(f"  {BOLD}{WHITE}{title_en}{RESET}")
    if title_jp != title_en:
        print(f"  {DIM}{title_jp}{RESET}")
    divider("=", 60, YELLOW)

    def row(label, value, color=GREEN):
        print(f"  {BOLD}{color}{label:<14}{RESET} {value}")

    row("Type",       anime_type)
    row("Episodes",   str(episodes))
    row("Status",     status)
    row("Aired",      aired)
    row("Duration",   duration)
    row("Source",     source)
    row("Rating",     rating)
    row("Score",      f"{YELLOW}{score}{RESET}" if score != "N/A" else score, CYAN)
    row("Rank",       f"#{rank}" if rank != "N/A" else rank, MAGENTA)
    row("Popularity", f"#{popularity}" if popularity != "N/A" else popularity, MAGENTA)
    row("Studios",    studios)
    row("Genres",     genres)

    if trailer:
        row("Trailer",    trailer, CYAN)

    divider("-", 60, CYAN)
    print(f"  {BOLD}{CYAN}Synopsis{RESET}")
    divider("-", 60, CYAN)
    for l in wrap_text(synopsis):
        print(f"  {l}")

    divider("-", 60, DIM)
    print()

    if anime_id:
        show_anime_submenu(anime_id, title_en)

def show_anime_submenu(anime_id, title):
    while True:
        print(f"\n  {BOLD}{CYAN}What do you want to see for {title}?{RESET}")
        print(f"  {YELLOW}[1]{RESET}  Characters and Voice Actors")
        print(f"  {YELLOW}[2]{RESET}  Staff and Directors")
        print(f"  {YELLOW}[3]{RESET}  Recommendations")
        print(f"  {YELLOW}[0]{RESET}  Go back")
        divider("-", 60, DIM)

        choice = get_number_input("Choose", 0, 3)
        if choice is None or choice == 0:
            break

        if choice == 1:
            show_characters(anime_id)
        elif choice == 2:
            show_staff(anime_id)
        elif choice == 3:
            show_recommendations(anime_id)

def show_characters(anime_id):
    print(f"\n  {DIM}Fetching characters...{RESET}")
    time.sleep(0.4)
    data = fetch_characters(anime_id)
    if not data or not data.get("data"):
        print(f"  {RED}Could not load characters.{RESET}")
        return

    characters = data["data"][:15]
    print()
    divider("-", 60, MAGENTA)
    print(f"  {BOLD}{MAGENTA}Characters{RESET}")
    divider("-", 60, MAGENTA)

    for entry in characters:
        char = entry.get("character", {})
        char_name = char.get("name", "N/A")
        role = entry.get("role", "N/A")
        voices = entry.get("voice_actors", [])
        va_name = "N/A"
        for va in voices:
            if va.get("language") == "Japanese":
                va_name = va.get("person", {}).get("name", "N/A")
                break
        print(f"  {BOLD}{WHITE}{char_name}{RESET}  {DIM}({role}){RESET}")
        print(f"  {DIM}Voice: {va_name}{RESET}")
        print()

    divider("-", 60, DIM)

def show_staff(anime_id):
    print(f"\n  {DIM}Fetching staff...{RESET}")
    time.sleep(0.4)
    data = fetch_staff(anime_id)
    if not data or not data.get("data"):
        print(f"  {RED}Could not load staff.{RESET}")
        return

    staff_list = data["data"][:12]
    print()
    divider("-", 60, MAGENTA)
    print(f"  {BOLD}{MAGENTA}Staff{RESET}")
    divider("-", 60, MAGENTA)

    for entry in staff_list:
        person = entry.get("person", {})
        person_name = person.get("name", "N/A")
        positions = entry.get("positions", [])
        pos_str = ", ".join(positions) if positions else "N/A"
        print(f"  {BOLD}{WHITE}{person_name}{RESET}  {DIM}{pos_str}{RESET}")

    print()
    divider("-", 60, DIM)

def show_recommendations(anime_id):
    print(f"\n  {DIM}Fetching recommendations...{RESET}")
    time.sleep(0.4)
    data = fetch_recommendations(anime_id)
    if not data or not data.get("data"):
        print(f"  {RED}Could not load recommendations.{RESET}")
        return

    recs = data["data"][:8]
    print()
    divider("-", 60, GREEN)
    print(f"  {BOLD}{GREEN}You might also like{RESET}")
    divider("-", 60, GREEN)

    for i, rec in enumerate(recs, 1):
        entry = rec.get("entry", {})
        rec_title = entry.get("title", "N/A")
        votes = rec.get("votes", 0)
        print(f"  {YELLOW}[{i}]{RESET}  {rec_title}  {DIM}({votes} votes){RESET}")

    print()
    divider("-", 60, DIM)

    pick = get_number_input(f"View details (1-{len(recs)}) or 0 to skip", 0, len(recs))
    if pick and pick > 0:
        chosen = recs[pick - 1]
        entry = chosen.get("entry", {})
        rec_id = entry.get("mal_id")
        rec_title = entry.get("title", "N/A")
        if rec_id:
            print(f"\n  {DIM}Fetching info for {rec_title}...{RESET}")
            time.sleep(0.5)
            url = f"https://api.jikan.moe/v4/anime/{rec_id}"
            result = make_request(url)
            if result and result.get("data"):
                display_anime_details(result["data"])

def search_and_display():
    while True:
        try:
            query = input(f"\n{CYAN}{BOLD}  Anime name (or 0 to go back): {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            return

        if query == "0" or query.lower() in ("back", "b"):
            return

        if not query:
            print(f"  {DIM}Please type something.{RESET}")
            continue

        print(f"\n  {DIM}Searching for \"{query}\"...{RESET}")
        time.sleep(0.2)

        data = fetch_anime(query)
        if not data:
            continue

        results = data.get("data", [])
        if not results:
            print(f"  {RED}No results found. Try a different name.{RESET}")
            continue

        chosen = pick_from_list(results)
        if chosen is None:
            continue

        display_anime_details(chosen)

def show_main_menu():
    print(BANNER)
    print(f"  {DIM}Welcome. Type an anime name to get started.{RESET}\n")

    while True:
        print()
        divider("=", 60, CYAN)
        print(f"  {BOLD}{CYAN}Main Menu{RESET}")
        divider("=", 60, CYAN)
        print(f"  {YELLOW}[1]{RESET}  Search by anime name")
        print(f"  {YELLOW}[0]{RESET}  Quit")
        divider("-", 60, DIM)

        choice = get_number_input("Choose", 0, 1)

        if choice is None or choice == 0:
            print(f"\n  {YELLOW}Goodbye!{RESET}\n")
            sys.exit(0)
        elif choice == 1:
            search_and_display()

def main():
    try:
        show_main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Goodbye!{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()