import os
from datetime import date, timedelta, datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///plants.db")


# Configure application
app = Flask(__name__)


@app.route("/")
def index():
    # read all plants from database and then render template
    plants = db.execute("SELECT * FROM plants")
    return render_template(
        "index.html",
        plants=plants,
    )


@app.route("/addPlant", methods=["GET", "POST"])
def addPlant():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # check for empty parts of form and then add to database
        if not request.form.get("nickName"):
            return redirect("/apology")
        elif not request.form.get("species"):
            return redirect("/apology")
        elif not request.form.get("subspecies"):
            return redirect("/apology")
        elif not request.form.get("source"):
            return redirect("/apology")
        else:
            # Add plant to database of plants
            db.execute(
                "INSERT INTO plants (nickName, species, subspecies, source, DOP, lastWater, lastFert, lastPcheck, lastPest) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                request.form.get("nickName"),
                request.form.get("species"),
                request.form.get("subspecies"),
                request.form.get("source"),
                date.today(),
                date.today(),
                date.today(),
                date.today(),
                date.today(),
            )
            return redirect("/")

    else:
        return render_template("addPlant.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check if Days ago watered and days ago fertilzed are numbers
        try:
            if request.form.get("daysAgoWater"):
                int(request.form.get("daysAgoWater"))
            if request.form.get("daysAgoFert"):
                int(request.form.get("daysAgoFert"))
        except ValueError:
            return redirect("/apology")
        # Check to see if entered numbers in nickname, subspecies, or source
        if (
            request.form.get("nickName").isnumeric()
            or request.form.get("subspecies").isnumeric()
            or request.form.get("source").isnumeric()
        ):
            return redirect("/apology")
        # Check if all parts of form are empty
        if (
            not request.form.get("nickName")
            and not request.form.get("species")
            and not request.form.get("subspecies")
            and not request.form.get("source")
            and not request.form.get("daysAgoWater")
            and not request.form.get("daysAgoFert")
        ):
            return redirect("/apology")
        # Search by nickname
        elif request.form.get("nickName"):
            plants = db.execute(
                "SELECT * FROM plants WHERE nickName = ?", request.form.get("nickName")
            )
        # Search by species
        elif request.form.get("species"):
            plants = db.execute(
                "SELECT * FROM plants WHERE species = ?", request.form.get("species")
            )
        # Search by subspecies
        elif request.form.get("subspecies"):
            plants = db.execute(
                "SELECT * FROM plants WHERE subspecies = ?",
                request.form.get("subspecies"),
            )
        # Search by source
        elif request.form.get("source"):
            plants = db.execute(
                "SELECT * FROM plants WHERE source = ?", request.form.get("source")
            )
        # Search by watered within n days
        elif request.form.get("daysAgoWater"):
            plants = db.execute(
                "SELECT * FROM plants WHERE lastWater > ?",
                date.today() - timedelta(days=int(request.form.get("daysAgoWater"))),
            )
        # Search by fertilized within n days
        elif request.form.get("daysAgoFert"):
            plants = db.execute(
                "SELECT * FROM plants WHERE lastFert > ?",
                date.today() - timedelta(days=int(request.form.get("daysAgoWater"))),
            )
        # combo search, species and n days watered
        elif request.form.get("species") and request.form.get("daysAgoWater"):
            plants = db.execute(
                "SELECT * FROM plants WHERE species = ? AND lastWater > ?",
                request.form.get("species"),
                date.today() - timedelta(days=int(request.form.get("daysAgoWater"))),
            )
        # combo search, species and n days fert
        elif request.form.get("species") and request.form.get("daysAgoFert"):
            plants = db.execute(
                "SELECT * FROM plants WHERE species = ? AND lastFert > ? ",
                request.form.get("species"),
                date.today() - timedelta(days=int(request.form.get("daysAgoFert"))),
            )
        # combo search, source and n days watered
        elif request.form.get("source") and request.form.get("daysAgoWater"):
            plants = db.execute(
                "SELECT * FROM plants WHERE source = ? AND lastWater > ?",
                request.form.get("source"),
                date.today() - timedelta(days=int(request.form.get("daysAgoWater"))),
            )
        # combo search, source and n days Fert
        elif request.form.get("source") and request.form.get("daysAgoFert"):
            plants = db.execute(
                "SELECT * FROM plants WHERE source = ? AND lastFert > ? ",
                request.form.get("source"),
                date.today() - timedelta(days=int(request.form.get("daysAgoFert"))),
            )
        return render_template("search.html", plants=plants)
    else:
        return render_template("search.html")


@app.route("/alerts")
def alerts():
    date_start, date_end = date(date.today().year, 3, 19), date(
        date.today().year, 9, 23
    )
    # check if watered within a week
    plantsWater = db.execute(
        "SELECT * FROM plants WHERE lastWater <= ?", date.today() - timedelta(days=7)
    )
    # if Spring or summer, check for fertilization within a week, else check for monthly fertilization
    if date.today() >= date_start and date.today() <= date_end:
        plantsFert = db.execute(
            "SELECT * FROM plants WHERE lastFert <= ?", date.today() - timedelta(days=7)
        )
    else:
        plantsFert = db.execute(
            "SELECT * FROM plants WHERE lastFert <= ?",
            date.today() - timedelta(days=30),
        )
    # check if pest check within a week
    plantsPcheck = db.execute(
        "SELECT * FROM plants WHERE lastPcheck <= ?", date.today() - timedelta(days=7)
    )
    # check if pest mangement within 8 weeks.
    plantsPest = db.execute(
        "SELECT * FROM plants WHERE lastPest <= ?", date.today() - timedelta(days=56)
    )
    # Render alerts after running searches
    return render_template(
        "alerts.html",
        plantsWater=plantsWater,
        plantsFert=plantsFert,
        plantsPcheck=plantsPcheck,
        plantsPest=plantsPest,
    )


@app.route("/addCare", methods=["GET", "POST"])
def addCare():
    plants = db.execute("SELECT * FROM plants")
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Update if they watered
        if request.form.get("watered"):
            db.execute(
                "UPDATE plants SET lastWater = ? WHERE nickName = ?",
                date.today(),
                request.form.get("nickName"),
            )
        # Update if they fertilized
        if request.form.get("fertilized"):
            db.execute(
                "UPDATE plants SET lastFert = ? WHERE nickName = ?",
                date.today(),
                request.form.get("nickName"),
            )
        # Update if they checked for pest
        if request.form.get("checkPest"):
            db.execute(
                "UPDATE plants SET lastPcheck = ? WHERE nickName = ?",
                date.today(),
                request.form.get("nickName"),
            )
        # Update if they completed pest management
        if request.form.get("pestManage"):
            db.execute(
                "UPDATE plants SET lastPest = ? WHERE nickName = ?",
                date.today(),
                request.form.get("nickName"),
            )
        # Return to index
        return redirect("/")
    else:
        return render_template("care.html", plants=plants)


@app.route("/apology")
def apology():
    # render an apology if an error
    return render_template("apology.html")
