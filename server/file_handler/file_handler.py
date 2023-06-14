import os
from datetime import datetime


current_path = os.getcwd()


def file_exist(file_name: str) -> bool:
    return os.path.exists(file_name)


def get_last_update_data(file_name: str) -> datetime:
    with open(os.path.join(current_path, file_name), "r") as file:
        row = file.readline()

    date_string = row.replace("\n", "")
    date_format = "%Y-%m-%d %H:%M:%S.%f"

    date = datetime.strptime(date_string, date_format)

    return date


def get_time_since_last_update(file_name: str) -> int:
    time = (datetime.now() - get_last_update_data(file_name)).total_seconds()
    time = time / (60 * 60)
    return time


def save_operation_file(file_name: str, urls: list[str]) -> None:
    with open(os.path.join(current_path, file_name), "w") as file:
        file.write(f"{datetime.now()}\n")

        for url in urls:
            status = 0
            file.write(f"{status} {url} null\n")


def change_operation_status(file_name: str, status: bool, url: str) -> None:
    with open(os.path.join(current_path, file_name), "r") as file:
        rows = file.readlines()

    with open(os.path.join(current_path, file_name), "w") as file:
        for i in range(len(rows)):
            if url in rows[i]:
                rows[i] = rows[i].replace(
                    f"{(not status ) * 1} {url}", f"{status * 1} {url}"
                )
                break

        file.writelines(rows)


def add_message_error(file_name: str, url: str, error_message: str) -> None:
    with open(os.path.join(current_path, file_name), "r") as file:
        rows = file.readlines()

    with open(os.path.join(current_path, file_name), "w") as file:
        for i in range(len(rows)):
            if url in rows[i]:
                rows[i] = rows[i].replace("null\n", f"{error_message}\n")
                break

        file.writelines(rows)


def get_urls_not_processed(file_name: str) -> list[str]:
    urls = []

    with open(file_name, "r+") as url_file:
        rows = url_file.readlines()[1:]

        for row in rows:
            if row.startswith("0"):
                url = row.split(" ")[1].replace("\n", "")
                urls.append(url)

    return urls
