from core.sites.readm import get_manga

if __name__ == "__main__":
    manga = get_manga("https://readm.org/manga/one-piece")
    manga.show()