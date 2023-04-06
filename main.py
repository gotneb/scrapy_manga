from server.readm_handler import ReadmHandler
from server.database import MangaDatabase

if __name__ == "__main__":
    db = MangaDatabase()

    db.connect()

    handler = ReadmHandler(db)
    handler.start()
    handler.join()

    db.close()
