from core.sites.readm import manga_detail, get_latest_updates
from server.database import db

if __name__ == "__main__":
    print(db.get_details("Shishunki na Adam"))