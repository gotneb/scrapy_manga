from dataclasses import dataclass


@dataclass
class Chapter:
    # I know it doesn't make any sense, but there are some rare chapters
    # whose value "it isn't a number", that's a bug from the site itself.
    number: str
    # mangalivre.net has a internal business logic for its chapters
    # readm.org doesn't need one, so it's `None` by default
    id: str = None
