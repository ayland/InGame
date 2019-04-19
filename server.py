import eel
import Filters
import DBhandlers
import seed
from WebScrapping import Down_Games, Down_Movies, Down_Series
from urllib.error import URLError
import urllib

eel.init('web')

current = None
to_show = []
index = 0
start = 0
end = 0 
load_amount = 10
find_match = []

@eel.expose
def current():
    global index
    return index

@eel.expose
def get_more(i = 1):
    global to_show
    global load_amount
    global start
    global end
    print('Start --> ', start, '   End --> ', end )
    print('got here with ', i)
    l = len(to_show)
    r = []
    if int(i) == 1:
        if end == l or end == 0:
            print('h1')
            down = 0
            up = min(l, down + load_amount)
            print('* ', l, '*', down, '*', load_amount)
        else:
            print('h2')
            up = min(l, end + load_amount)
            down = end
        r = to_show[down: up]
        print('Low:', down , '    high:', up)
        start = down
        end = up
    else:
        if start == 0:
            low = l - l%load_amount
            high = l
        else:
            low = max(0, start - load_amount)
            high = start
        r = to_show[low : high]
        print('Low:', low, '    high:', high)
        start = low
        end = high
    print('returning:', len(r), '   Start: ', start, '   End: ', end)
    print()
    print()
    return r
@eel.expose
def next_obj(id, direction = 1):
    print('*', id, '*', direction)
    cui =find_match[id]
    if int(direction) == 1 and cui < len(to_show) - 1:
        return to_show[cui + 1]
    elif int(direction) != 1 and cui > 0:
        return to_show[cui - 1]

@eel.expose
def filter_series(name="", gender=[],actor="",director="", score=0, year=0, topic=""):
    global to_show
    global index
    global start
    global end
    if score == '':
        score = 0
    if year == '':
        year = 0
    year = int(year)
    score = float(score)
    print('*', name, '*' ,gender, '*' ,actor, '*' ,director, '*' ,score, '*' ,year)
    series = Filters.filter_series(name, gender,actor,director, score, year, topic)
    to_show = series
    for i in to_show:
        find_match.append(i['id'])
    start = 0
    end = 0
    return get_more()

@eel.expose
def filter_movies(name="", gender=[],actor="",director="", score=0, year = 0, topic=""):
    global to_show
    global index
    global start
    global end
    if score == '':
        score = 0
    if year == '':
        year = 0
    year = int(year)
    score = float(score)
    print('*', name, '*' ,gender, '*' ,actor, '*' ,director, '*' ,score, '*' ,year)
    movies = Filters.filter_movies(name, gender, actor, director, score, year, topic)
    to_show = movies
    for i in to_show:
        find_match.append(i['id'])
    start = 0
    end = 0
    return get_more()

@eel.expose
def filter_games(name = "", gender = "", launch=0, players=0,game_mode="", category="", lenguage="", score=0):
    global to_show
    global index
    global start
    global end
    if category == 'Todos':
        category = ''
        gender=''
    if gender == 'Todos':
        gender = ''
    games = Filters.filter_games(name=name, gender=gender, launch=launch, game_mode=game_mode, category=category, lenguage=lenguage, score=score)
    to_show = games
    for i in to_show:
        find_match.append(i['id'])
    start = 0
    end = 0
    return get_more()

@eel.expose
def get_recent():
    recent = Filters.get_recent()
    return recent

@eel.expose
def CRUD_Serie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],score=0,id=-1, image="", topics=[], delete=0):
     #(image)
    if current is None or current == -1:
        if delete == 0:
            dele = False
        else:
            dele = True
        DBhandlers.CRUD_Serie(title, year, pais, sinopsis, generos, directors, reparto, score, id, image, topics, dele)
    else:
        DBhandlers.CRUD_Serie(title, year, pais, sinopsis, generos, directors, reparto,score, current.id, image, topics, delete = False)
        Done_update()

@eel.expose
def CRUD_Movie(title="", year=0, pais="", sinopsis="", generos=[], directors=[], reparto=[],score=0, id=-1, image="", topics=[], delete=0):
    if current is None or current == -1:
        if delete == 0:
            dele = False
        else:
            dele = True
        DBhandlers.CRUD_Movie(title, year, pais, sinopsis, generos, directors, reparto, score, id, image, topics, dele)
    else:
        DBhandlers.CRUD_Movie(title, year, pais, sinopsis, generos, directors, reparto,score, current.id, image, topics, delete = False)
        Done_update()

@eel.expose
def CRUD_Game(name="", description="", game_mode="", language="", launch=0, puntuacion=0, category="", genders=[], requirements=[[],[]], id=-1, cover="", captures=[],size=0, delete=0):
    if current is None or current == -1:
         #('h2')
        if delete == 0:
            dele = False
        else:
            #qqqqqqq
            dele = True
        if len(requirements) == 0:
             #('had to')
            requirements = [[],[]]
        #'DEl:', dele)
        DBhandlers.CRUD_Game(name, description, game_mode, language, launch, puntuacion, category, genders, requirements, id, image=cover, captures=captures, size = size, delete=dele)
    else:
         #('begin_update')
        #'WTF???????')
        #current)
        DBhandlers.CRUD_Game(name, description, game_mode, language, launch, puntuacion, category, genders, requirements, current.id, image=cover, captures=captures,size=size, delete=False)
         #('done_update')
        Done_update()

@eel.expose
def Set_Game(id):
    global current
     #('id', id )
    current = DBhandlers.find_game(id)
     #('current:' , current)

@eel.expose
def Set_Serie(id):
     #('ID:',id)
    global current
    current = DBhandlers.find_serie(id)
     #('çurrent: ', current)
@eel.expose
def Set_Movie(id):
    global current
    current = DBhandlers.find_movie(id)

@eel.expose
def Done_update():
    global current
    current = None
    #'Done update')

@eel.expose
def add_director(name):
    DBhandlers.add_director2(current, name)

@eel.expose
def del_director(name):
    DBhandlers.del_director(current, name)

@eel.expose
def add_actor(name):
    DBhandlers.add_actor2(current, name)

@eel.expose
def del_actor(name):
    DBhandlers.del_actor(current, name)

@eel.expose
def add_tv_gender(name, typ=True):
     #('Serv: ', typ)
    DBhandlers.add_tv_gender2(current, name, typ)

@eel.expose
def del_tv_gender(name):
    DBhandlers.del_tv_gender(current, name)

@eel.expose
def add_topic(name):
    DBhandlers.add_topic2(current, name)

@eel.expose
def del_topic(name):
    DBhandlers.del_topic(current, name)

@eel.expose
def add_game_gender(name):
    DBhandlers.add_game_gender(current, name)

@eel.expose
def del_game_gender(name):
    DBhandlers.del_game_gender(current, name)

@eel.expose
def get_game_genders():
    return seed.game_categories

@eel.expose
def get_video_genders():
    return seed.video_category

@eel.expose
def get_serie_topics():
    return Filters.get_serie_topics()

@eel.expose
def get_movie_genders():
    return Filters.get_movie_genders()

@eel.expose
def get_movie_topics():
    return Filters.get_movie_topics()

@eel.expose
def get_downloads():
    return DBhandlers.get_downloads()

def try_connection():
    try:
        r = urllib.request.urlopen('http://google.com')
        return 2
    except URLError:
        print('No tienes conexion a internet, compruebe su conexion e intentelo mas tarde')
        return -1

@eel.expose
def download_games():
    r = try_connection()
    if r == 2:
        Down_Games()
    return r

@eel.expose
def download_series():
    try:
        Down_Series()
        return 2
    except URLError:
        print('No tienes conexion a internet, compruebe su conexion e intentelo mas tarde')
        return -1

@eel.expose
def download_movies():
    try:
        Down_Movies()
        return 2
    except URLError:
        print('No tienes conexion a internet, compruebe su conexion e intentelo mas tarde')
        return -1

@eel.expose
def gen_pdf():
    pass

@eel.expose
def get_counters():
    a = DBhandlers.get_counters()
    return a

eel.start('index_vue.html')


