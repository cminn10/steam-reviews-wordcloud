from flask import Flask, render_template, request
from crawl_steam import get_all
import base64
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_key_for_dev_purpose'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=['POST'])
async def search():
    game_title = request.form['game_title']
    # flash('Searching for game reviews...')

    reviews = await get_all(game_title)
    if not reviews:
        return render_template('index.html', game_tile=game_title, not_found_msg="This game content cannot be reached by anonymous user :(")

    data = io.BytesIO()
    reviews.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template('index.html', img_data=encoded_img_data.decode('utf-8'), game_tile=game_title)
