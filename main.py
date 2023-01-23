from core.sites.readm import manga_detail

if __name__ == "__main__":
    manga = manga_detail("https://readm.org/manga/one-piece")
    manga.show()