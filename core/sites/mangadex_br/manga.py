import math
from requests import get
from entities.chapter import Chapter
from entities.manga import Manga
from .constants import base_url

def get_manga(manga_id: str):
    """
    Get the desiered manga.
    """
    r = get(f'{base_url}/manga/{manga_id}')
    json = r.json()

    # print(r.content.decode())

    #print(json['data']['attributes']['description']['en'])

    # Should I use the raw or the mangadex url?
    url = json['data']['attributes']['links']['raw']
    # I think it could be better using a list
    alt_title = get_alt_titles(json)

    title = json['data']['attributes']['title']['en']
    author = get_author(json)
    status = json['data']['attributes']['status']
    artist = None
    score = get_score(manga_id)
    thumbnail = get_thumbnail(manga_id, json)
    genres = get_genres(json)
    summary = json['data']['attributes']['description']['en']
    chapters = get_chapters(manga_id)

    return Manga(
        title=title,
        alternative_title=alt_title,
        author=author,
        artist=artist,
        status=status,
        url=url,
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


def get_artist(json) -> str:
    json['data']['relationships'][3]['id']
    artist_id = json['data']['relationships'][0]['id']

    r = get(f'{base_url}/artist/{artist_id}')
    print(r.content.decode())
    artist = r.json()['data']['attributes']['name']
    print(artist)


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


def get_score(manga_id: str):
    r = get(f'{base_url}/statistics/manga/{manga_id}')
    sc = r.json()['statistics'][manga_id]['rating']['average']
    return float(sc)


def get_chapters(manga_id: str):
    chapters = []

    r = get(
        f"{base_url}/manga/{manga_id}/feed",
        params={
            'limit': 100,
            'offset': 0,
            'translatedLanguage[]': ['pt-br'],
        }
    )

    json = r.json()
    total = math.ceil(int(json['total']) / 100)

    for i in range(0, total):
        r = get(
            f"{base_url}/manga/{manga_id}/feed",
            params={
                'limit': 100,
                'offset': i * 100,
                'translatedLanguage[]': ['pt-br'],
            }
        )
    
        json = r.json()
        for value in json['data']:
            c = json2chapter(value)
            chapters.append(c)
    
    # From the api pagination, the chapters come randomly...
    chapters.sort(key=lambda c: float(c.name))
    
    return chapters


def json2chapter(json) -> Chapter:
    return Chapter(
        name=json["attributes"]['chapter'],
        title=json["attributes"]['title'],
        pages=[0]
    )