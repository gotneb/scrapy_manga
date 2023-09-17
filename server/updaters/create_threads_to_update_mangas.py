from concurrent.futures import ThreadPoolExecutor, Future
from ..api import *
from core.sites.manga_livre import *
from typing import Callable


default_number_of_works = 1


def create_threads_to_update_mangas(
    urls: list[str],
    update_function: Callable[[list[str]], None],
    number_of_works: int = default_number_of_works,
):
    """Create N threads to update mangas"""
    with ThreadPoolExecutor(max_workers=number_of_works) as executor:
        futures: list[Future] = []

        for url in urls:
            futures.append(executor.submit(update_function, url))

        executor.shutdown(wait=True)
