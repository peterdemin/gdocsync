import os

_HERE = os.path.dirname(__file__)
IMAGE_ASSETS = os.path.join(_HERE, "assets/image")
SOURCE_HTML_BUNDLE = os.path.join(IMAGE_ASSETS, "html_bundle.zip")
EXPECTED_RST = os.path.join(IMAGE_ASSETS, "imported.rst")
SOURCE_HTML = os.path.join(IMAGE_ASSETS, "page.html")
CLEAN_HTML = os.path.join(IMAGE_ASSETS, "page_clean.html")
CONVERTED_RST = os.path.join(IMAGE_ASSETS, "converted.rst")
IMAGES_DIR = os.path.join(IMAGE_ASSETS, "images")

MARKUP_ASSETS = os.path.join(_HERE, "assets/markup")
MARKUP_SOURCE_HTML = os.path.join(MARKUP_ASSETS, "page.html")
MARKUP_CLEAN_HTML = os.path.join(MARKUP_ASSETS, "page_clean.html")
MARKUP_CONVERTED_RST = os.path.join(MARKUP_ASSETS, "converted.rst")

LINKS_ASSETS = os.path.join(_HERE, "assets/links")
LINKS_SOURCE_HTML = os.path.join(LINKS_ASSETS, "page.html")
LINKS_CLEAN_HTML = os.path.join(LINKS_ASSETS, "page_clean.html")
LINKS_CONVERTED_RST = os.path.join(LINKS_ASSETS, "converted.rst")

ALT_MARKUP_ASSETS = os.path.join(_HERE, "assets/alt_markup")
ALT_MARKUP_SOURCE_HTML = os.path.join(ALT_MARKUP_ASSETS, "page.html")
ALT_MARKUP_CLEAN_HTML = os.path.join(ALT_MARKUP_ASSETS, "page_clean.html")

MINUTES_ASSETS = os.path.join(_HERE, "assets/minutes")
MINUTES_SOURCE_HTML_BUNDLE = os.path.join(MINUTES_ASSETS, "html_bundle.zip")
MINUTES_EXPECTED_RST = os.path.join(MINUTES_ASSETS, "imported.rst")
MINUTES_SOURCE_HTML = os.path.join(MINUTES_ASSETS, "page.html")
MINUTES_CLEAN_HTML = os.path.join(MINUTES_ASSETS, "page_clean.html")
