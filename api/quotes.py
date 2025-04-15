import requests

class QuoteFetcher:
    def get_quote(self):
        res = requests.get("https://zenquotes.io/api/random")
        if res.status_code == 200:
            quote = res.json()[0]
            return f"{quote['q']} - {quote['a']}"
        else:
            return "Failed to fetch quote"
