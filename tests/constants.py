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
