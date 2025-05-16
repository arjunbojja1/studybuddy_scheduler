"""Quote fetching for the StudyBuddy Scheduler.

This script defines the QuoteFetcher class, which retrieves motivational
quotes from the ZenQuotes API.
"""

import requests

class QuoteFetcher:
    """Fetches motivational quotes from the ZenQuotes API."""

    def get_quote(self):
        """Fetches a random quote from the ZenQuotes API.

        Returns:
            str: A motivational quote in the format 'quote - author'.
                 Returns an error message if the API request fails.
        """
        res = requests.get("https://zenquotes.io/api/random")
        if res.status_code == 200:
            quote = res.json()[0]
            return f"{quote['q']} - {quote['a']}"
        else:
            return "Failed to fetch quote"
