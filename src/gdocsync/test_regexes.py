from .regexes import RE_JOHNNY_DECIMAL, RE_PUNCT


def test_johnny_decimal_regex():
    positive = RE_JOHNNY_DECIMAL.match("[12.34] - Name")
    assert positive.groups() == ("12", "34", "Name")
    positive = RE_JOHNNY_DECIMAL.match("[12.34] Name")
    assert positive.groups() == ("12", "34", "Name")
    negative = RE_JOHNNY_DECIMAL.match("07/20 - Birthday")
    assert negative is None


def test_punctuation_regex():
    result = RE_PUNCT.findall("Hello, {[world]}!")
    assert result == [", {[", "]}!"], result
