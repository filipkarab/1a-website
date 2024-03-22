import datetime

from mysql.connector import connect
from time import time

import os.path

conf = {
    "host": "23.137.104.153",
    "port": "3306",
    "user": "u7402_yvBREAA9TW",
    "password": "YMNfm^Ivmb3ZeV^e+GANyejK",
    "database": "s7402_dsbot"
}

cnx = connect(**conf)
cursor = cnx.cursor()


def initiate_connection():
    cnx = connect(**conf)
    cursor = cnx.cursor()


# CREATE TABLE `{date}-new` (`lesson` VARCHAR(22) NOT NULL, `type` VARCHAR(16) NOT NULL, `message` VARCHAR(512), `deadline` DATE, `image-ids` VARCHAR(72), `links` VARCHAR(512));


def new_day_exists(date):
    cnx.commit()
    cursor.execute(
        f"SELECT EXISTS (SELECT * FROM information_schema.tables WHERE table_schema = 's7402_dsbot' AND table_name = '{date}-new');"
    )
    res = cursor.fetchall()
    if res[0][0] == 1:
        return True
    return False


def force_get_new_components(date: str):
    cnx.commit()
    cursor.execute(f"SELECT * FROM `{date}-new`;")
    return cursor.fetchall()


def force_get_new_components_table(table: str):
    cnx.commit()
    cursor.execute(f"SELECT * FROM `{table}`;")
    return cursor.fetchall()


def get_components_if_new_day_exists(date):
    if new_day_exists(date):
        return force_get_new_components(date)
    return []


def view_row_exists_skola(date) -> bool:
    cnx.commit()
    datum = date.strftime("%Y-%m-%d")
    cursor.execute(f"SELECT * FROM `views-new` WHERE `date` = '{datum}'")
    return len(cursor.fetchall()) > 0


def create_view_row_skola(date) -> None:
    datum = date.strftime("%Y-%m-%d")
    cursor.execute(f"INSERT INTO `views-new` (date, views) VALUES ('{datum}', 1)")
    cnx.commit()


def get_views_skola(date) -> int:
    datum = date.strftime("%Y-%m-%d")
    cnx.commit()
    cursor.execute(f"SELECT * FROM `views-new` WHERE date = '{datum}'")
    return cursor.fetchall()[0][1]


def add_one_view_skola(date):
    if not view_row_exists_skola(date):
        create_view_row_skola(date)
    else:
        views = get_views_skola(date)
        datum = date.strftime("%Y-%m-%d")
        cursor.execute(f"UPDATE `views-new` SET views = {views + 1} WHERE date = '{datum}'")
        cnx.commit()


def view_row_exists_upto(date) -> bool:
    cnx.commit()
    datum = date.strftime("%Y-%m-%d")
    cursor.execute(f"SELECT * FROM `views-upto` WHERE `date` = '{datum}'")
    return len(cursor.fetchall()) > 0


def create_view_row_upto(date) -> None:
    datum = date.strftime("%Y-%m-%d")
    cursor.execute(f"INSERT INTO `views-upto` (date, views) VALUES ('{datum}', 1)")
    cnx.commit()


def get_views_upto(date) -> int:
    datum = date.strftime("%Y-%m-%d")
    cnx.commit()
    cursor.execute(f"SELECT * FROM `views-upto` WHERE date = '{datum}'")
    return cursor.fetchall()[0][1]


def add_one_view_upto(date):
    if not view_row_exists_upto(date):
        create_view_row_upto(date)
    else:
        views = get_views_upto(date)
        datum = date.strftime("%Y-%m-%d")
        cursor.execute(f"UPDATE `views-upto` SET views = {views + 1} WHERE date = '{datum}'")
        cnx.commit()


def view_row_exists(table: str) -> bool:
    cnx.commit()
    tablee = table.split('-')[0]
    date = datetime.datetime.strptime("%m/%d/%Y", tablee[0] + tablee[1] + '/' + tablee[2] + tablee[3] + '/' + tablee[4] + tablee[5] + tablee[6] + tablee[7])
    datum = date.strftime("%Y-%m-%d")
    cursor.execute(f"SELECT * FROM `views-new` WHERE `date` = '{datum}'")
    res = len(cursor.fetchall()) > 0
    cursor.execute(f"SELECT * FROM `views-upto` WHERE `date` = '{datum}'")
    return len(cursor.fetchall()) > 0 or res > 0


def get_views(tables: list[str]):
    newStatement = f"SELECT * FROM `views-new` WHERE "
    uptoStatement = f"SELECT * FROM `views-upto` WHERE "
    firstNew, firstUpto = True, True
    for i, table in enumerate(tables):
        tablee = table.split('-')[0]
        date = datetime.datetime.strptime(tablee[0] + tablee[1] + '/' + tablee[2] + tablee[3] + '/' + tablee[4] +
                                          tablee[5] + tablee[6] + tablee[7],
                                          "%m/%d/%Y")
        datum = date.strftime("%Y-%m-%d")
        typ = table.split('-')[1]
        if typ == "new":
            if firstNew:
                newStatement = newStatement + f'`views-new`.date = "{datum}"'
                firstNew = False
            else:
                newStatement = newStatement + f' OR `views-new`.date = "{datum}"'
        else:
            if firstUpto:
                uptoStatement = uptoStatement + f'`views-upto`.date = "{datum}"'
                firstUpto = False
            else:
                uptoStatement = uptoStatement + f' OR `views-upto`.date = "{datum}"'
    newStatement = newStatement + ";"
    uptoStatement = uptoStatement + ";"
    cnx.commit()
    cursor.execute(newStatement)
    res1 = cursor.fetchall()
    cursor.execute(uptoStatement)
    res2 = cursor.fetchall()
    res = {}
    for i in res1:
        res[i[0].strftime("%m%d%Y") + "-new"] = i[1]
    for i in res2:
        res[i[0].strftime("%m%d%Y") + "-upto"] = i[1]
    return res


def get_changed_tables() -> list[str]:
    cnx.commit()
    cursor.execute(f"SELECT * FROM `changes`")
    res = cursor.fetchall()
    changes = []
    for row in res:
        changes.append(row[0])
    return changes


def table_exists(table: str) -> bool:
    cnx.commit()
    cursor.execute(
        f"SELECT EXISTS (SELECT * FROM information_schema.tables WHERE table_schema = 's7402_dsbot' AND table_name = '{table}');"
    )
    return cursor.fetchall()[0][0] == 1


def get_changed_data(changedTables: list[str]):
    cnx.commit()
    res = {}
    for table in changedTables:
        if table_exists(table):
            res[table] = force_get_new_components_table(table)
            cursor.execute("""DELETE FROM `changes` WHERE `table` = %s""", (table,))
            cnx.commit()
        else:
            res[table] = []
    return res


def clear_changes() -> None:
    cursor.execute("SET SQL_SAFE_UPDATES = 0;")
    cursor.execute("DELETE FROM `changes`;")
    cnx.commit()


def _detect_changes(original: dict, after: dict) -> dict:
    changes = {}

    for key, value in after.items():
        if key not in original.keys():
            continue
        if original[key] is not after[key]:
            changes[key] = after[key]

    return changes


def _detect_additions(original: dict, after: dict) -> dict:
    additions = {}

    for key, value in after.items():
        if key not in original.keys():
            additions[key] = after[key]

    return additions


def _datestr_to_db(dateStr: str) -> str:
    dateStr = dateStr.split('-')[0]
    return dateStr[4:8] + '-' + dateStr[0:2] + '-' + dateStr[2:4]


def _update_views_for_date(dateStr: str, views: int) -> None:

    dateType = dateStr.split('-')[1]
    table = ""  # `views-new` / `views-upto`

    if dateType == "new":
        table = "views-new"
    else:
        table = "views-upto"

    dateDb = _datestr_to_db(
        dateStr.split('-')[0]
    )

    statement = f"UPDATE `{table}` SET `views` = {views} WHERE `date` = '{dateDb}';"
    cursor.execute(statement)
    cnx.commit()


def _insert_views(additions: dict) -> None:
    newStatement = f"INSERT INTO `views-new` VALUES "
    uptoStatement = f"INSERT INTO `views-upto` VALUES "

    newIndex = 0
    uptoIndex = 0
    for dateStr, views in additions.items():
        dateType = dateStr.split('-')[1]
        dateDb = _datestr_to_db(
            dateStr.split('-')[0]
        )

        if dateType == "new":
            if newIndex == 0:
                newStatement = newStatement + f"('{dateDb}', {views})"
            else:
                newStatement = newStatement + f", ('{dateDb}', {views})"

            newIndex += 1
            continue

        if dateType == "upto":
            if uptoIndex == 0:
                uptoStatement = uptoStatement + f"('{dateDb}', {views})"
            else:
                uptoStatement = uptoStatement + f", ('{dateDb}', {views})"

            uptoIndex += 1
            continue

    if newIndex != 0:
        newStatement = newStatement + ';'
        cursor.execute(newStatement)
        cnx.commit()

    if uptoIndex != 0:
        uptoStatement = uptoStatement + ';'
        cursor.execute(uptoStatement)
        cnx.commit()


def update_views(originalViews: dict, views: dict) -> None:

    additions = _detect_additions(originalViews, views)
    changes = _detect_changes(originalViews, views)

    _insert_views(additions)
    for date, views in changes.items():
        _update_views_for_date(date, views)


def break_connection():
    cursor.close()
    cnx.close()


def _write_file_and_get_path(imageId: int, data: bytes) -> str:

    path = os.path.relpath(f"./static/attachments/{imageId}.png")
    with open(path, 'wb') as file:
        file.write(data)
        file.close()

    return path


def _get_image(imageId: int) -> bytes:

    cnx.commit()
    statement = """SELECT `image` FROM `images` WHERE id = %s"""
    cursor.execute(statement, (imageId,))

    res = cursor.fetchall()
    imageData = bytes(res[0][0])

    return imageData


def is_image_downloaded(imageId: int) -> bool:
    return os.path.isfile(f"./static/attachments/{imageId}.png")


def download_image_and_get_path(imageId: int) -> str:

    imageData = _get_image(imageId)
    path = _write_file_and_get_path(imageId, imageData)

    return path


def _convert_to_binary(path) -> bytes:
    with open(os.path.relpath(path), 'rb') as file:
        binaryData = file.read()
    return binaryData


def upload_image(path: str) -> None:

    binary = _convert_to_binary(path)
    statement = """INSERT INTO `images` (`image`) VALUE (%s)"""
    cursor.execute(statement, (binary,))
    cnx.commit()


# oTime = round(time() * 1000)
#
# print(f"{round(time() * 1000) - oTime}ms")
