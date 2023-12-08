from flask import Flask, render_template, request
import pickle
from tmdbv3api import Movie, TMDb

app = Flask(__name__)

# 객체생성 및 API키 입력 및 한글
movie = Movie()
tmdb = TMDb()
tmdb.api_key = 'c668cda4cf75bf267ef2aeffa2da0341'
tmdb.language = 'ko-KR'


@app.route("/")
def index():
    return render_template("index.html")


### 인기영화 탑텐
@app.route("/page1")
def page1():
    return render_template("page1.html")

@app.route('/movie1.json')
def movie1():
    movies = pickle.load(open('./data/movies1.pickle', 'rb'))
    json = []
    for i in range(10):
        id = movies['id'].iloc[i]
        details = movie.details(id)
        title = details['title']
        etitle = movies['title'].iloc[i]
        image = details['poster_path']
        if image:
            image = "https://image.tmdb.org/t/p/w500" + image
        else:
            image = 'http://via.placeholder.com/100x100'
            
        score = round(movies['score'].iloc[i], 2)
        data = {'title':title, 'etitle':etitle, 'id':str(id), 'image':image, 'score':str(score)}
        json.append(data)
    return json



### 전체 영화 제목.json
@app.route('/movies.json')
def movies():
    movies = pickle.load(open('./data/movies.pickle', 'rb'))    
    json = movies.to_json(orient='records')
    return json



### 줄거리가 내가좋아하는영화랑 비슷한거 추천하는 페이지
@app.route("/page2")
def page2():
    return render_template("page2.html")

@app.route('/movie2.json/<title>')
def movies2(title):
    movies = pickle.load(open('./data/movies.pickle', 'rb'))
    sim = pickle.load(open('./data/sim.pickle', 'rb'))
    # 1. 제목에 대한 인덱스값 가져오기
    filter = movies['title'] == title
    idx = movies[filter].index[0]
    # 2. 유사도테이블에서 idx번째 유사도값 가져오기
    sim_scores = sim[idx]
    #. 영화인덱스번호와 유사도값 배열로 만들어줌
    sim_scores = list(enumerate(sim_scores))
    # 4. 유사도가 높은 순으로 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # 5. 상위 10개 영화 가져오기
    sim_scores = sim_scores[1:13]
    sim_movies = [i[0] for i in sim_scores]
    ###movies[['id', 'title']].iloc[sim_movies]
    json = []
    for i in range(12):
        id = movies['id'].iloc[sim_movies[i]]
        details = movie.details(id)
        etitle = movies['title'].iloc[sim_movies[i]]
        title = details['title']
        image = details['poster_path']
        if image:
            image = "https://image.tmdb.org/t/p/w500" + image
        else:
            image = 'http://via.placeholder.com/100x100'
        data = {'etitle':etitle, 'title':title, 'image':image}
        json.append(data)
    return json




### 감독/배우로 영화 추천하는 페이지
@app.route("/page3")
def page3():
    return render_template("page3.html")

@app.route('/movie3.json/<title>')
def movies3(title):
    movies = pickle.load(open('./data/movies.pickle', 'rb'))
    sim = pickle.load(open('./data/sim2.pickle', 'rb'))
    # 1. 제목에 대한 인덱스값 가져오기
    filter = movies['title'] == title
    idx = movies[filter].index[0]
    # 2. 유사도테이블에서 idx번째 유사도값 가져오기
    sim_scores = sim[idx]
    #. 영화인덱스번호와 유사도값 배열로 만들어줌
    sim_scores = list(enumerate(sim_scores))
    # 4. 유사도가 높은 순으로 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # 5. 상위 10개 영화 가져오기
    sim_scores = sim_scores[1:13]
    sim_movies = [i[0] for i in sim_scores]
    ###movies[['id', 'title']].iloc[sim_movies]
    json = []
    for i in range(12):
        id = movies['id'].iloc[sim_movies[i]]
        details = movie.details(id)
        etitle = movies['title'].iloc[sim_movies[i]]
        title = details['title']
        image = details['poster_path']
        if image:
            image = "https://image.tmdb.org/t/p/w500" + image
        else:
            image = 'http://via.placeholder.com/100x100'
        data = {'etitle':etitle, 'title':title, 'image':image}
        json.append(data)
    return json





if __name__ == "__main__":
    app.run(port=5000, debug=True)