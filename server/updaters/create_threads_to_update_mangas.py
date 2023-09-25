from concurrent.futures import ThreadPoolExecutor, Future
from ..api import *
from core.sites.manga_livre import *
from typing import Callable


default_number_of_works = 1


def create_threads_to_update_mangas(
    urls: list[str],
    upsert_function: Callable[[list[str]], bool],
    number_of_works: int = default_number_of_works,
):
    """
    Creates threads that will execute the manga update function given its URLs.

    Args:
        urls: URLs of the mangas to be updated.
        upsert_function: Update function.
        number_of_works (int): Number of threads used for accessing the website.

    Returns:
        None
    """

    with ThreadPoolExecutor(max_workers=number_of_works) as executor:
        futures: list[Future] = []

        for url in urls:
            futures.append(executor.submit(upsert_function, url))

        executor.shutdown(wait=True)
