from server.updaters.readm import update_mangas as readm_update_mangas
from server.updaters.golden_mangas import update_mangas as golden_mangas_update_mangas


def update_database(exec_all: bool = False):
    print("Starting the website update process\n")

    print("\nUpdating readm.org\n")
    readm_update_mangas(exec_all)

    print("\nUpdating goldenmangas.top\n")
    golden_mangas_update_mangas(exec_all)
