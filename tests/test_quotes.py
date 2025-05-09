from api.quotes import QuoteFetcher

def test_quotes():
    quote = QuoteFetcher().get_quote()

    assert isinstance(quote, str), "Quote should be a string"
    assert len(quote.strip()) > 0, "Quote should not be empty"
    assert "-" in quote, "Quote should contain a hyphen for author separation"

    parts = [part.strip() for part in quote.split("-", 1)]
    assert len(parts) == 2, "Quote should be in the format 'quote - author'"
    assert len(parts[0]) > 0, "Quote part should not be empty"
    assert len(parts[1]) > 0, "Author part should not be empty"
