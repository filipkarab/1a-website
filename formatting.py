import datetime

import database

monday = {
    "slovina": "1",
    "anglina": "3-4",
    "nemcina": "5",
    "uvod-do-programovania": "6-7",
    "triednicka": "8"
}

tuesday = {
    "nemcina": "1",
    "matika": "2",
    "fyzika": "3",
    "slovina": "4",
    "robotika": "5-6",
    "hardver-pocitaca": "7"
}

wednesday = {
    "fyzika": "1",
    "elektrotechnika": "2",
    "etika": "3",
    "slovina": "4",
    "anglina": "5",
    "nemcina": "6",
    "matika": "7"
}

thursday = {
    "matika": "1",
    "elektrotechnika": "2",
    "odborna-prax": "3-4",
    "fyzika": "5",
    "slovina": "7"
}

friday = {
    "elektrotechnika": "1-2",
    "anglina": "3",
    "matika": "4",
    "aplikovana-informatika": "5-6"
}


def insert_double(lessonSpan):
    if len(lessonSpan) > 1:
        return " double"
    return ""


def full_class_name(subject):
    if subject == "slovina":
        return "Slovina"
    elif subject == "anglina":
        return "Anglina"
    elif subject == "nemcina":
        return "Nemčina"
    elif subject == "matika":
        return "Matika"
    elif subject == "uvod-do-programovania":
        return "Úvod do programovania"
    elif subject == "triednicka":
        return "Triednicka"
    elif subject == "fyzika":
        return "Fyzika"
    elif subject == "robotika":
        return "Robotika"
    elif subject == "hardver-pocitaca":
        return "Hardvér počítača"
    elif subject == "elektrotechnika":
        return "Elektrotechnika"
    elif subject == "odborna-prax":
        return "Odborná prax"
    elif subject == "aplikovana-informatika":
        return "Aplikovaná informatika"
    elif subject == "etika":
        return "Etika"
    return "Neznámy predmet"


# [('slovina', 'homework', 'Vypracovať úlohu 123/4,5 a 124/6,7,8,9', datetime.date(2024, 2, 27), None, None), ('anglina',
# 'test', 'Unit 4 slovíčka', datetime.date(2024, 2, 27), None, None), ('anglina', 'note', 'Pripraviť sa na niečo', None, None, None),
# ('uvod-do-programovania', 'lesson', 'Robili sme for cyklus', None, None, None), ('triednicka', 'nic', None, None, None, None)]
def process_skola(data, den):
    res = ""

    classes = {}
    day = den.weekday()
    if day == 0:  # Monday
        classes = monday
    elif day == 1:  # Tuesday
        classes = tuesday
    elif day == 2:  # Wednesday
        classes = wednesday
    elif day == 3:  # Thursday
        classes = thursday
    else:  # Friday | Saturday | Monday
        classes = friday

    for key, value in classes.items():

        addition = f'<li><div class="classes__subject subject--{key}{insert_double(value)}"><h1 class="lessons">{value}</h1><h1>{full_class_name(key)}</h1><ul class="components">{"{}"}</ul></div></li>'

        components = ""
        for row in data:

            lesson = row[0]
            typee = row[1]
            message = row[2]
            deadline = row[3]
            imageIds = row[4]
            links = row[5]

            if lesson == key:

                if typee == "note":
                    components = components + f'<li class="component note"><img class="note__icon" src="../static/images/icons/note.ico" alt="A note icon" /><div class="note__content"><h4 class="note__title">Poznámka</h4><p class="note__message">{message}</p></div></li>'
                elif typee == "lesson":
                    components = components + f'<li class="component lesson"><img class="lesson__icon" src="../static/images/icons/book.png" alt="A book icon" /><div class="lesson__content"><h4 class="lesson__title">Na hodine</h4><p class="lesson__message">{message}</p></div></li>'
                elif typee == "test":
                    components = components + f'<li class="component test"><img class="test__icon" src="../static/images/icons/test.png" alt="A test icon" /><div class="test__content"><h4 class="test__title">Ohlásená písomka</h4><p class="test__message">{message}</p></div><p class="test__deadline">{_weekday_name_a(deadline).lower()} ({deadline.strftime("%d.%m.%Y")})</p></li>'
                elif typee == "homework":
                    components = components + f'<li class="component homework"><img class="homework__icon" src="../static/images/icons/homework_backpack.png" alt="A backpack icon" /><div class="homework__content"><h4 class="homework__title">Domáca úloha</h4><p class="homework__message">{message}</p></div><p class="homework__deadline">{_weekday_name_a(deadline).lower()} ({deadline.strftime("%d.%w.%Y")})</p></li>'
                elif typee == "links":
                    components = components + '<li class="component links"><img class="links__icon" src="../static/images/icons/link.png" alt="A link icon" /><div class="links__content"><h4 class="links__title">Odkazy</h4><div class="links__urls">'
                    for link in links.split(';'):
                        components = components + f'<a href="{link}" target="_blank"><p>{link}</p></a>'
                    components = components + '</div></div></li>'
                elif typee == "attachment":
                    components = components + f'<li class="component attachment"><img class="attachment__icon" src="../static/images/icons/attachment.png" alt="A paperclip icon" /><div class="attachment__content"><h4 class="attachment__title">Priložené obrázky</h4><div class="attachment__images">'

                    for imageId in imageIds.split(';'):
                        components = components + f'<a href="/static/attachments/{imageId}.png" target="_blank"><img src="../static/attachments/{imageId}.png" alt="An image of notes from the lesson" /></a>'

                    components = components + '</div></div></li>'

        if components == "":
            components = f'<li class="component nothing"><img class="nothing__icon" src="../static/images/icons/nic.png" alt="An icon of an empty magnifying glass with a red cross through the glass" /><div class="nothing__content"><h4 class="nothing__title">Zatiaľ ešte nič</h4><p class="nothing__message">Z tejto hodiny sa zatiaľ nič nenašlo ¯\_(ツ)_/¯</p></div></li>'

        addition = addition.format(components)
        res = res + addition

    return res


def process_upto(data, den):
    res = ""

    classes = {}
    day = den.weekday()
    if day == 0:  # Monday
        classes = monday
    elif day == 1:  # Tuesday
        classes = tuesday
    elif day == 2:  # Wednesday
        classes = wednesday
    elif day == 3:  # Thursday
        classes = thursday
    elif day == 4:  # Friday
        classes = friday
    else:  # Saturday | Monday
        classes = monday

    for key, value in classes.items():

        addition = f'<li><div class="classes__subject subject--{key}{insert_double(value)}"><h1 class="lessons">{value}</h1><h1>{full_class_name(key)}</h1><ul class="components">{"{}"}</ul></div></li>'

        components = ""
        for row in data:

            lesson = row[0]
            typee = row[1]
            message = row[2]
            deadline = row[3]
            imageIds = row[4]
            links = row[5]

            if lesson == key:

                if typee == "note":
                    components = components + f'<li class="component note"><img class="note__icon" src="../static/images/icons/note.ico" alt="A note icon" /><div class="note__content"><h4 class="note__title">Poznámka</h4><p class="note__message">{message}</p></div></li>'
                elif typee == "test":
                    components = components + f'<li class="component test"><img class="test__icon" src="../static/images/icons/test.png" alt="A test icon" /><div class="test__content"><h4 class="test__title">Píšeme písomku</h4><p class="test__message">{message}</p></div><p class="test__deadline"{_weekday_name_g(deadline).lower()} ({deadline.strftime("%d.%m.%Y")})</p></li>'
                elif typee == "homework":
                    components = components + f'<li class="component homework"><img class="homework__icon" src="../static/images/icons/homework_backpack.png" alt="A backpack icon" /><div class="homework__content"><h4 class="homework__title">Máme mať domácu</h4><p class="homework__message">{message}</p></div><p class="homework__deadline">{_weekday_name_g(deadline).lower()} ({deadline.strftime("%d.%w.%Y")})</p></li>'
                elif typee == "links":
                    components = components + '<li class="component links"><img class="links__icon" src="../static/images/icons/link.png" alt="A link icon" /><div class="links__content"><h4 class="links__title">Odkazy</h4><div class="links__urls">'
                    for link in links.split(';'):
                        components = components + f'<a href="{link}" target="_blank"><p>{link}</p></a>'
                    components = components + '</div></div></li>'
                elif typee == "attachment":
                    components = components + f'<li class="component attachment"><img class="attachment__icon" src="../static/images/icons/attachment.png" alt="A paperclip icon" /><div class="attachment__content"><h4 class="attachment__title">Priložené obrázky</h4><div class="attachment__images">'

                    for imageId in imageIds.split(';'):
                        components = components + f'<a href="/static/attachments/{imageId}.png" target="_blank"><img src="../static/attachments/{imageId}.png" alt="An image of notes from the lesson" /></a>'

                    components = components + '</div></div></li>'

        if components == "":
            components = f'<li class="component nothing"><img class="nothing__icon" src="../static/images/icons/nic.png" alt="An icon of an empty magnifying glass with a red cross through the glass" /><div class="nothing__content"><h4 class="nothing__title">Najskôr nič</h4><p class="nothing__message">Na túto hodinu najskôr nič špecifické netreba</p></div></li>'

        addition = addition.format(components)
        res = res + addition

    return res


def _generate_relevant_dates(upto: bool = False) -> list[str]:
    dates = []

    if upto:
        for i in range(0, 7 + 1):
            dates.append((datetime.date.today() + datetime.timedelta(days=i)).strftime("%m%d%Y-upto"))
    else:
        for i in range(-7, 0 + 1):
            dates.append((datetime.date.today() + datetime.timedelta(days=i)).strftime("%m%d%Y-new"))

    return dates


def _weekday_name(date: datetime.date) -> str:
    weekdayIndex = date.weekday()

    if weekdayIndex == 0:
        return "Pondelok"
    elif weekdayIndex == 1:
        return "Utorok"
    elif weekdayIndex == 2:
        return "Streda"
    elif weekdayIndex == 3:
        return "Štvrtok"
    elif weekdayIndex == 4:
        return "Piatok"
    elif weekdayIndex == 5:
        return "Sobota"
    elif weekdayIndex == 6:
        return "Nedeľa"
    else:
        return "Invalidný deň"


def _weekday_name_a(date: datetime.date) -> str:
    weekdayIndex = date.weekday()

    if weekdayIndex == 0:
        return "na Pondelok"
    elif weekdayIndex == 1:
        return "na Utorok"
    elif weekdayIndex == 2:
        return "na Stredu"
    elif weekdayIndex == 3:
        return "na Štvrtok"
    elif weekdayIndex == 4:
        return "na Piatok"
    elif weekdayIndex == 5:
        return "na Sobotu"
    elif weekdayIndex == 6:
        return "na Nedeľu"
    else:
        return "Invalidný deň"


def _weekday_name_g(date: datetime.date) -> str:
    weekdayIndex = date.weekday()

    if weekdayIndex == 0:
        return "z Pondelku"
    elif weekdayIndex == 1:
        return "z Utorku"
    elif weekdayIndex == 2:
        return "zo Stredy"
    elif weekdayIndex == 3:
        return "zo Štvrtku"
    elif weekdayIndex == 4:
        return "z Piatku"
    elif weekdayIndex == 5:
        return "zo Soboty"
    elif weekdayIndex == 6:
        return "z Nedele"
    else:
        return "Invalidný deň"


def _date_from_str(dateStr: str) -> datetime.date:
    return datetime.datetime.strptime(
        dateStr[4:8] + '-' + dateStr[0:2] + '-' + dateStr[2:4],
        "%Y-%m-%d"
    ).date()


# <li><a href="/skola?den=02262024"><h3>Pondelok</h3><p>26.2.2024</p><hr /></a></li><li><a href="/skola?den=02272024"><h3>Utorok</h3><p>27.2.2024</p><hr /></a></li><li><a href="/skola?den=02282024"><h3>Streda</h3><p>28.2.2024</p></a><hr /></li><li><a href="/skola?den=02292024"><h3>Štvrtok</h3><p>29.2.2024</p></a><hr /></li><li class="selected"><a href="/skola?den=03012024"><h3>Piatok</h3><p>1.3.2024</p></a><hr /></li><li><a href="/skola?den=03042024"><h3>Pondelok</h3><p>4.3.2024</p></a><hr /></li><li><a href="/skola?den=03052024"><h3>Utorok</h3><p>5.3.2024</p></a><hr /></li><li><a href="/skola?den=03062024"><h3>Streda</h3><p>6.3.2024</p></a><hr /></li><li><a href="/skola?den=03072024"><h3>Štvrtok</h3><p>7.3.2024</p></a><hr /></li><li><a href="/skola?den=03082024"><h3>Piatok</h3><p>8.3.2024</p></a></li>
def calendar_skola(day: datetime.date) -> str:
    relevantDates = _generate_relevant_dates()

    result = ""
    for i, dateStr in enumerate(relevantDates):

        date = _date_from_str(dateStr)
        weekday = _weekday_name(date)

        if weekday == "Sobota" or weekday == "Nedeľa":
            continue

        if day.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"):
            result = result + '<li class="selected">'
        else:
            result = result + '<li>'

        result = (result + '<a href="/skola?den='
                  + date.strftime("%m%d%Y")
                  + '"><h3>'
                  + weekday
                  + '</h3><p>'
                  + date.strftime("%d.%m.%Y")
                  + '</p>')

        if i < len(relevantDates) - 1:
            result = result + '<hr />'

        result = result + '</a></li>'

    return result


def calendar_upto(day: datetime.date) -> str:
    relevantDates = _generate_relevant_dates(upto=True)

    result = ""
    for i, dateStr in enumerate(relevantDates):

        date = _date_from_str(dateStr)
        weekday = _weekday_name(date)

        if weekday == "Sobota" or weekday == "Nedeľa":
            continue

        if day.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"):
            result = result + '<li class="selected">'
        else:
            result = result + '<li>'

        result = (result + '<a href="/kalendar?den='
                  + date.strftime("%m%d%Y")
                  + '"><h3>'
                  + weekday
                  + '</h3><p>'
                  + date.strftime("%d.%m.%Y")
                  + '</p>')

        if i < len(relevantDates) - 1:
            result = result + '<hr />'

        result = result + '</a></li>'

    return result
