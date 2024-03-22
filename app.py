import datetime

from time import time

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

import atexit
from apscheduler.schedulers.background import BackgroundScheduler

import database
import formatting

data = {
    "02282024-new": [('fyzika', 'note', 'Nič sme nerobili, bola voľná', None, None, None), ('elektrotechnika', 'homework', 'Cvičenia 1 a 2 na mylearninga', datetime.date(2024, 3, 6), None, None), ('slovina', 'test', 'Novoveká literatúra', datetime.date(2024, 2, 29), None, None), ('anglina', 'lesson', 'Úlohy 64/5,6,7 a 78/1,2,3 v učebnici', None, None, None), ('matika', 'links', None, None, None, 'https://youtube.com/;https://google.com/;https://mylearning.spseke.sk/')]
}

originalViews = {
    "02292024-new": 23,
    "03012024-upto": 11
}
views = {
    "02292024-new": 25,
    "03012024-upto": 12
}

print("Creating flask app")
app = Flask(__name__)
print("Successfully created flask app")

print("Connecting to the database")
database.initiate_connection()
print("Successfully connected to the database")

print("Creating scheduler and scheduling events")
scheduler = BackgroundScheduler(daemon=True)
print("Successfully created and started scheduler with all of its events")


# Checks if a string looks like this: "02282024".
def is_a_date(date: str) -> bool:
    return date.isdigit() and len(date) == 8


@app.route('/')
def start():
    return redirect("/skola?den=dnes")


def _get_views(date: datetime.date, upto: bool = False) -> int:
    global views
    if not upto:
        dateStr = date.strftime("%m%d%Y-new")
    else:
        dateStr = date.strftime("%m%d%Y-upto")
    if dateStr in views.keys():
        return views[dateStr]
    else:
        views[dateStr] = 0
        return 0


@app.route('/skola')
def skola():
    global views, originalViews, data
    den = request.args.get("den", '')

    if den == "dnes":
        date = datetime.date.today()
        date = date.strftime("%m%d%Y")
        return redirect(f"/skola?den={date}")
    elif den == "vcera":
        date = datetime.date.today() - datetime.timedelta(days=1)
        date = date.strftime("%m%d%Y")
        return redirect(f"/skola?den={date}")
    elif den == "zajtra":
        date = datetime.date.today() + datetime.timedelta(days=1)
        date = date.strftime("%m%d%Y")
        return redirect(f"/skola?den={date}")
    elif not is_a_date(den):
        return render_template(
            "404.html",
            message=f"Invalidný argument ?den={den}."
        )

    date = den[0] + den[1] + '/' + den[2] + den[3] + '/' + den[4] + den[5] + den[6] + den[7]
    date = datetime.datetime.strptime(date, "%m/%d/%Y")

    if date.weekday() == 5:
        date = date - datetime.timedelta(days=1)
    elif date.weekday() == 6:
        date = date - datetime.timedelta(days=2)
    datum = date.strftime("%d.%m.%Y")

    if date.strftime("%m%d%Y-new") not in data.keys():
        return render_template(
            "404.html",
            message=f"Hľadaný deň {datum} nebol nájdený v databáze."
        )

    views[date.strftime("%m%d%Y-new")] = _get_views(date) + 1

    return render_template("skola.html",
                           datum=datum,
                           videni=views[date.strftime("%m%d%Y-new")],
                           classes=formatting.process_skola(
                               data[date.strftime("%m%d%Y") + "-new"],
                               date
                           ),
                           calendar=formatting.calendar_skola(date))


@app.route("/kalendar")
def kalendar():
    global views, originalViews, data
    den = request.args.get("den", '')

    if den == "dnes":
        date = datetime.date.today()
        date = date.strftime("%m%d%Y")
        return redirect(f"/kalendar?den={date}")
    elif den == "vcera":
        date = datetime.date.today() - datetime.timedelta(days=1)
        date = date.strftime("%m%d%Y")
        return redirect(f"/kalendar?den={date}")
    elif den == "zajtra":
        date = datetime.date.today() + datetime.timedelta(days=1)
        date = date.strftime("%m%d%Y")
        return redirect(f"/kalendar?den={date}")
    elif not is_a_date(den):
        return render_template(
            "404.html",
            message=f"Invalidný argument ?den={den}."
        )

    date = den[0] + den[1] + '/' + den[2] + den[3] + '/' + den[4] + den[5] + den[6] + den[7]
    date = datetime.datetime.strptime(date, "%m/%d/%Y")

    if date.weekday() == 5:
        date = date + datetime.timedelta(days=2)
    elif date.weekday() == 6:
        date = date + datetime.timedelta(days=1)
    datum = date.strftime("%d.%m.%Y")

    if date.strftime("%m%d%Y-upto") not in data.keys():
        return render_template(
            "404.html",
            message=f"Hľadaný deň {datum} nebol nájdený v databáze."
        )

    views[date.strftime("%m%d%Y-upto")] = _get_views(date, True) + 1

    return render_template("kalendar.html",
                           datum=datum,
                           videni=views[date.strftime("%m%d%Y-upto")],
                           classes=formatting.process_upto(
                               data[date.strftime("%m%d%Y") + "-upto"],
                               date
                           ),
                           calendar=formatting.calendar_upto(date))


@app.route("/rozvrh")
def rozvrh():
    return render_template("rozvrh.html")


@app.route('/demo/skola')
def demo_skola():
    return render_template("demo/skola.html")


@app.route("/demo/kalendar")
def demo_kalendar():
    return render_template("demo/kalendar.html")


@app.route("/demo/rozvrh")
def demo_rozvrh():
    return render_template("demo/rozvrh.html")


# Called every 60 seconds (1min)
# Used to check for database changes
def interval(first: bool = False) -> None:
    ms = round(time(), 2)
    print("Calling an interval")
    global data, originalViews, views

    if first:
        print("Getting first data from the database")

        datesToCheck = []
        for i in range(-7, 7 + 1):
            datesToCheck.append((datetime.date.today() + datetime.timedelta(days=i)).strftime("%m%d%Y-new"))
            datesToCheck.append((datetime.date.today() + datetime.timedelta(days=i)).strftime("%m%d%Y-upto"))

        data = database.get_changed_data(datesToCheck)

        # for i in datesToCheck:
        #     data[i] = []
        #     pass
        # data[datetime.date.today().strftime("%m%d%Y-new")] = [
        #     ("matika", "attachment", None, None, "2", None),
        #     ("elektrotechnika", "lesson", "Multisim labáku meranie výkonu", None, None, None),
        #     ("anglina", "lesson", "Písali sme písomku", None, None, None),
        #     ("aplikovana-informatika", "lesson", "Korešpondencia vo worde", None, None, None),
        #     ("aplikovana-informatika", "test", "Praktická časť wordu", datetime.date.today() + datetime.timedelta(days=7), None, None)
        # ]
        # data["03112024-upto"] = [
        #     ('uvod-do-programovania', 'attachment', None, None, '2', None),
        #     ('anglina', 'note', 'Asi bude chýbať malachovská', None, None, None),
        #     ('slovina', 'homework', 'Vypracovať PL', datetime.date(2024, 3, 7), None, None)
        # ]

        for key, value in data.items():
            for component in value:
                if component[1] == "attachment":
                    for imageId in component[4].split(';'):
                        if not database.is_image_downloaded(int(imageId)):
                            database.download_image_and_get_path(int(imageId))

        views = database.get_views(datesToCheck)
        originalViews = database.get_views(datesToCheck)

        print("Successfully got all the first data")
    else:

        print("Updating changed data")

        replacementData = database.get_changed_data(
            database.get_changed_tables()
        )
        for key, value in data.items():
            if key in replacementData.keys():
                data[key] = replacementData[key]
            else:
                data[key] = value

        for key, value in data.items():
            for component in value:
                if component[1] == "attachment":
                    for imageId in component[4].split(';'):
                        if not database.is_image_downloaded(int(imageId)):
                            database.download_image_and_get_path(int(imageId))

        database.update_views(originalViews, views)
        datesToCheck = []
        for i in range(-7, 7 + 1):
            datesToCheck.append((datetime.date.today() + datetime.timedelta(days=i)).strftime("%m%d%Y-new"))
            datesToCheck.append((datetime.date.today() + datetime.timedelta(days=i)).strftime("%m%d%Y-upto"))
        originalViews = database.get_views(datesToCheck)

        print("Successfully updated changed data")

    print(f"Finished an interval in {round(time() - ms, 2)}s")


print("Calling first interval")
scheduler.start()
scheduler.add_job(func=interval, trigger="interval", seconds=60)
atexit.register(lambda: scheduler.shutdown())
interval(first=True)
print("Finished first calling of interval")


if __name__ == '__main__':
    app.run()
    database.break_connection()
