import gettext
from typing import Dict, Optional

from src import LOCALES_DIR


def find_locales() -> Dict[str, gettext.GNUTranslations]:
    translations: Dict[str, gettext.GNUTranslations] = {}

    for path in LOCALES_DIR.iterdir():
        if not path.is_dir():
            continue
        mo_path = path / "LC_MESSAGES" / f"texts.mo"

        if mo_path.exists():
            with mo_path.open("rb") as fp:
                translations[path.name] = gettext.GNUTranslations(fp)

    return translations


locales = find_locales()


def gettext(singular: str, plural: Optional[str] = None, n: int = 1, locale: Optional[str] = None) -> str:
    if locale is None:
        locale = "ru"

    if locale not in locales:
        if n == 1:
            return singular
        return plural if plural else singular

    translator = locales[locale]

    if plural is None:
        return translator.gettext(singular)
    return translator.ngettext(singular, plural, n)
