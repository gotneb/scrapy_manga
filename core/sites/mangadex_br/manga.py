from requests import get
from entities.manga import Manga
from .constants import base_url

from utils.debug_tools import save_text

def get_manga(manga_id: str):
    """
    Get the desiered manga.
    """
    r = get(f'{base_url}/manga/{manga_id}')
    json = r.json()

    # print(r.content.decode())

    #print(json['data']['attributes']['description']['en'])

    title = json['data']['attributes']['title']['en']
    alt_title = get_alt_titles(json)
    author = get_author(json)
    status = json['data']['attributes']['status']
    artist = ''
    score = ''
    thumbnail = get_thumbnail(manga_id, json)
    genres = get_genres(json)
    summary = json['data']['attributes']['description']['en']
    chapters = ''

    return Manga(
        title=title,
        alternative_title=alt_title,
        author=author,
        artist=artist,
        status=status,
        url='',
        origin='mangadex_br',
        language='portuguese',
        thumbnail=thumbnail,
        genres=genres,
        summary=summary,
        chapters=chapters,
        rating=score,
    )


def get_author(json) -> str:
    json['data']['relationships'][0]['id']
    author_id = json['data']['relationships'][0]['id']

    r = get(f'{base_url}/author/{author_id}')
    return r.json()['data']['attributes']['name']


def get_thumbnail(manga_id: str, json):
    cover_id = json['data']['relationships'][4]['id']
    r = get(f'{base_url}/cover/{cover_id}')

    cover_filename = r.json()['data']['attributes']['fileName']
    return f'https://uploads.mangadex.org/covers/{manga_id}/{cover_filename}'


def get_alt_titles(json):
    alt_titles = json['data']['attributes']['altTitles']
    titles = []
    for title in alt_titles:
        extracted_title = list(title.values())[0]
        if extracted_title not in titles:
            titles.append(extracted_title)
    # Well, it shoulb be a list... not a string...
    return (', '.join(titles)).strip()


def get_genres(json):
    tags = json['data']['attributes']['tags']
    return [tag['attributes']['name']['en'] for tag in tags]