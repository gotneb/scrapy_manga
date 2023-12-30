from requests import get

# It uses binary search ;)
def get_pages(chapter_value: str) -> list[str]:
    raise Exception("Don't use this function. Insteadm use get_chapter()!")

    low: int = 1
    high: int = 200 # I don't think there's a manga that has more than 200 pages
    base_url = f'https://img.lermanga.org/B/berserk/capitulo-{chapter_value}'

    while low <= high:
        index = (low + high) // 2
        url = f'{base_url}/{index}.jpg'
        resp = get(url)

        # print(f'{resp.status_code} |-> {url}')

        if resp.status_code != 200:
            high = index - 1
        else:
            low = index + 1

    return [f'{base_url}/{i}.jpg' for i in range(1, low)]