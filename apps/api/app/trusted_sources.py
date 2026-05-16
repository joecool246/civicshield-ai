import json
import re
from dataclasses import dataclass
from pathlib import Path

from app.models import Source

TRUSTED_SOURCE_DIR = Path(__file__).resolve().parents[1] / "data" / "trusted_sources"
INDIANA_TERMS = {"indiana", "hoosier"}
OTHER_STATE_NAMES = {
    "alabama",
    "alaska",
    "arizona",
    "arkansas",
    "california",
    "colorado",
    "connecticut",
    "delaware",
    "florida",
    "georgia",
    "hawaii",
    "idaho",
    "illinois",
    "iowa",
    "kansas",
    "kentucky",
    "louisiana",
    "maine",
    "maryland",
    "massachusetts",
    "michigan",
    "minnesota",
    "mississippi",
    "missouri",
    "montana",
    "nebraska",
    "nevada",
    "new hampshire",
    "new jersey",
    "new mexico",
    "new york",
    "north carolina",
    "north dakota",
    "ohio",
    "oklahoma",
    "oregon",
    "pennsylvania",
    "rhode island",
    "south carolina",
    "south dakota",
    "tennessee",
    "texas",
    "utah",
    "vermont",
    "virginia",
    "washington",
    "west virginia",
    "wisconsin",
    "wyoming",
}
SEARCH_STOPWORDS = {
    "about",
    "does",
    "have",
    "need",
    "what",
    "when",
    "where",
    "which",
    "with",
    "vote",
    "voter",
    "voting",
}


@dataclass(frozen=True)
class TrustedSource:
    id: str
    title: str
    url: str
    publisher: str
    jurisdiction: str
    topics: list[str]
    content: str

    def to_source(self) -> Source:
        return Source(title=self.title, url=self.url, publisher=self.publisher)


def _contains_phrase(text: str, phrase: str) -> bool:
    return re.search(rf"\b{re.escape(phrase)}\b", text) is not None


def mentions_other_state(text: str) -> bool:
    lowered = text.lower()
    return any(_contains_phrase(lowered, state) for state in OTHER_STATE_NAMES)


def mentions_indiana(text: str) -> bool:
    lowered = text.lower()
    return any(_contains_phrase(lowered, term) for term in INDIANA_TERMS)


def load_trusted_sources() -> list[TrustedSource]:
    sources = []
    for path in sorted(TRUSTED_SOURCE_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        sources.append(TrustedSource(**data))
    return sources


def search_trusted_sources(query: str, limit: int = 4) -> list[TrustedSource]:
    lowered = query.lower()
    if mentions_other_state(lowered) or not mentions_indiana(lowered):
        return []

    tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", lowered)
        if len(token) > 2 and token not in SEARCH_STOPWORDS
    }
    scored: list[tuple[int, TrustedSource]] = []

    for source in load_trusted_sources():
        haystack = " ".join([source.title, source.publisher, *source.topics, source.content]).lower()
        score = sum(2 for topic in source.topics if topic in lowered)
        score += sum(1 for token in tokens if token in haystack)
        if score > 0:
            scored.append((score, source))

    return [source for _, source in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]
