from flask import Flask, render_template, request, redirect, send_file
from extractors.wwr import extract_wwr_jobs
from extractors.ro import extract_ro_jobs
from extractors.saramin import extract_saramin_jobs
from file import save_to_file

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

db = {}
@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None or keyword == "":
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        wwr = extract_wwr_jobs(keyword)
        ro = extract_ro_jobs(keyword)
        saramin = extract_saramin_jobs(keyword)
        jobs = wwr + ro + saramin
        db[keyword] = jobs
    return render_template("search.html", keyword = keyword, jobs = jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None or keyword == "":
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)

app.run("0.0.0.0")