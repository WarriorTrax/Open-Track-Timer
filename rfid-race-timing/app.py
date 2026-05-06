from flask import Flask, render_template, jsonify, request
import time, json

app = Flask(__name__)

runners = {}
athletes = {}
race_start = None
race_active = False

try:
    with open("runners.json") as f:
        athletes = json.load(f)
except:
    athletes = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    leaderboard = []

    for tag, r in runners.items():
        total = sum(r["splits"])

        leaderboard.append({
            "id": tag,
            "name": athletes.get(tag, tag),
            "laps": r["laps"],
            "total": round(total, 2)
        })

    leaderboard.sort(key=lambda x: x["total"])
    return jsonify(leaderboard)

@app.route('/start')
def start():
    global race_start, race_active, runners
    race_start = time.time()
    race_active = True
    runners = {}
    return "started"

@app.route('/reset')
def reset():
    global runners
    runners = {}
    return "reset"

@app.route('/add', methods=['POST'])
def add():
    global race_active

    tag = request.json["id"]
    now = time.time()

    if not race_active:
        return "not started"

    if tag not in runners:
        runners[tag] = {
            "laps": 1,
            "splits": [0],
            "last": now
        }
    else:
        split = now - runners[tag]["last"]

        if split < 3:
            return "ignored"

        runners[tag]["laps"] += 1
        runners[tag]["splits"].append(split)
        runners[tag]["last"] = now

    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)