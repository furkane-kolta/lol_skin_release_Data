from datetime import datetime
from flask import Flask, render_template
from get_champions import get_champions

app = Flask(__name__)

champions_and_skins = get_champions()

@app.route('/')
def index():
    return render_template(
        'index.html',
        title='LoL Skin Count Data',
        champions = champions_with_day_approximations(),
    )

def champions_with_day_approximations():
    full_list = champions_and_skins
    today = datetime.today()
    for champion in full_list:
        champion_released_in = datetime.strptime(champion["champion_release_date"], "%d %B %Y")
        difference_days = (today - champion_released_in).days
        champion["champion_attention_division"] = difference_days // champion["champion_skin_count"]
    
    return(full_list)

if __name__ == "__main__":
    app.run()