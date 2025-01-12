import re
import string

RE_JOHNNY_DECIMAL = re.compile(r"\[?(\d{1,2})\.(\d{2})\]?[ -]*(.+)")
RE_PUNCT = re.compile(f"[{re.escape(string.punctuation)} ]+")
