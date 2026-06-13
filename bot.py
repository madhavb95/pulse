# Pulse - Daily Summary Bot
# Fetches: weather (wttr.in) + quote (zenquotes.io) + date fact (numbersapi.com)
# Runs: every day at 8 AM IST via GitHub Actions
# APIs: all free, no API keys needed

import requests
from datetime import date

# -- FUNCTION 1: Weather ----------------------------------------------
def get_weather(city="Thiruvananthapuram"):
    """Fetch today's weather as a one-line text summary."""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Weather unavailable ({e})"

# -- FUNCTION 2: Quote ------------------------------------------------
def get_quote():
    """Fetch a random motivational quote from ZenQuotes."""
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        quote = data[0]["q"]
        author = data[0]["a"]
        return f'"{quote}"\n    — {author}'
    except Exception as e:
        return f"Quote unavailable ({e})"

# -- FUNCTION 3: Date Fact (custom extension) -------------------------
def get_date_fact():
    """Fetch a fun fact about today's date from Numbers API."""
    today = date.today()
    url = f"http://numbersapi.com/{today.month}/{today.day}/date"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Fact unavailable ({e})"

# -- FUNCTION 4: Build the summary ------------------------------------
def build_summary():
    """Assemble the full daily summary from all data sources."""
    today = date.today().strftime("%A, %d %B %Y")
    weather = get_weather()
    quote = get_quote()
    fact = get_date_fact()

    summary = f"""
╔══════════════════════════════════════════╗
         🌅  PULSE — Daily Summary
         {today}
╚══════════════════════════════════════════╝

🌤️  WEATHER
    {weather}

💬  TODAY'S QUOTE
    {quote}

🧠  ON THIS DAY
    {fact}

──────────────────────────────────────────
   Built by Madhav · Pulse Bot · ZERO2DEV
──────────────────────────────────────────
"""
    return summary

# -- FUNCTION 5: Run everything ---------------------------------------
def run():
    """Main entry point. Called by GitHub Actions."""
    summary = build_summary()
    print(summary)
    with open("daily_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print("✅ Pulse ran successfully.")

# -- Entry point guard ------------------------------------------------
if __name__ == "__main__":
    run()
