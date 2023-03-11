from core.sites.readm import manga_detail
from server.functions import add_manga

if __name__ == "__main__":
    manga = manga_detail("https://readm.org/manga/one-piece")
    manga.show()
    add_manga(manga)