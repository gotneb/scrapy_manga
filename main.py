from server.database import MangaDatabase
from server.readm_handler import ReadmHandler as Handler

if __name__ == "__main__":
    db = MangaDatabase()
    db.connect()
    handler = Handler(db)
    handler.start()

    db.close()
