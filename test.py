from server.updaters.ler_manga import *

url = "https://lermanga.org/mangas/the-knight-king-who-returned-with-a-god/"
manga = get_manga(url)

print(manga.title)

for chapter in manga.chapters:
    print(chapter.name)
    print(chapter.pages)
    print("")
