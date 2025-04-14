from api.quotes import QuoteFetcher

def test_quotes():
    quote = QuoteFetcher().get_quote()
    
    assert isinstance(quote, str), "Quote should be a string"
    assert len(quote) > 0, "Quote should not be empty"
    assert "-" in quote, "Quote should contain an author"
    assert len(quote.split("-")) == 2, "Quote should be in the format 'quote - author'"