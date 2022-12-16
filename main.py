from flask import Flask,render_template,jsonify,request,make_response,url_for,redirect
import json, requests, random
from requests.structures import CaseInsensitiveDict

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("welcome.html")
    
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        response = requests.post("http://localhost:8080/api/auth/signin", json={"username":username,"password":password})
        jwt = response.json()['accessToken']
        resp = make_response(redirect('/dashboard'))
        resp.set_cookie('SESSIONID', jwt)  
        return resp
    else:
        jwt = request.cookies.get('SESSIONID')
        print("jwt"+str(jwt))
        if jwt is None:
            return render_template("login.html")
        else:
            return make_response(redirect('/dashboard'))
        

@app.route("/register",methods=["GET","POST"])
def signUp():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        response = requests.post("http://localhost:8080/api/auth/signup", json={"username":username,"password":password,"email":email,"roles":["user"]})
        msg = response.json()['message']
        resp = make_response(redirect('/login'))
        return resp
    else:
        return render_template("register.html")

@app.route("/forgotPassword",methods=["GET","POST"])
def forgotPassword():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    jwt = request.cookies.get('SESSIONID')
    if jwt is None:
        return make_response(redirect('/login'))
    else:
        url = "http://localhost:8080/api/user/getDetails/"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer "+jwt

        response = requests.get(url, headers=headers)
        data = response.json()
        return render_template("dashboard.html", username=data['username'], stars_count=data['stars_count'], score_total=data['score_total'], score1=data['score1'], score2=data['score2'], score3=data['score3'])

@app.route("/info")
def plasticInfo():
    jwt = request.cookies.get('SESSIONID')
    if jwt is None:
        return make_response(redirect('/login'))
    else:
        url = "http://localhost:8080/api/user/getDetails/"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer "+jwt

        response = requests.get(url, headers=headers)
        data = response.json()
        return render_template("plasticinfo.html")

@app.route("/guide")
def howToPlay():
    jwt = request.cookies.get('SESSIONID')
    if jwt is None:
        return make_response(redirect('/login'))
    else:
        url = "http://localhost:8080/api/user/getDetails/"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer "+jwt

        response = requests.get(url, headers=headers)
        data = response.json()
        return render_template("howtoplay.html")

@app.route("/leaderboard")
def leaderboard():
    jwt = request.cookies.get('SESSIONID')
    if jwt is None:
        return make_response(redirect('/login'))
    else:
        url = "http://localhost:8080/api/user/getDetails/"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer "+jwt

        response = requests.get(url, headers=headers)
        data = response.json()
        return render_template("leaderboard.html", username=data['username'], stars_count=data['stars_count'], score_total=data['score_total'], score1=data['score1'], score2=data['score2'], score3=data['score3'])

@app.route("/scorepage")
def scorepage():
    jwt = request.cookies.get('SESSIONID')
    print("jwt"+str(jwt))
    if jwt is None:
        return make_response(redirect('/login'))
    else:
        args = request.args
        url = "http://localhost:8080/api/user/setScore"+args.get("level")
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer "+jwt
        data = '{"score":'+str(int(args.get("total_score"))*20)+'}'
        data = json.loads(data)
        response = requests.post(url, headers=headers, data=data)
        print(response.json())

        url2 = "http://localhost:8080/api/user/setScoreTotal/"
        data2 = '{"score":'+str(int(args.get("total_score"))*20)+'}'
        data2 = json.loads(data2)
        response2 = requests.post(url2, headers=headers, data=data2)
        print(response2.json())

        url3 = "http://localhost:8080/api/user/setStarsCount/"
        data3 = '{"stars":'+str(5-int(args.get("total_score")))+'}'
        data3 = json.loads(data3)
        response3 = requests.post(url3, headers=headers, data=data3)
        print(response3.json())
        
        return render_template("scorepage.html",score_total=args.get("total_score"), level=args.get("level"))

@app.route('/level<level>',methods=["GET","POST"])
def level(level):
    url = "http://localhost:8080/api/question/getCategory/"+str(level)
    jwt = request.cookies.get('SESSIONID')
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer "+jwt

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    # random.shuffle(data)

    question=[]
    solution=[]
    answer=[]
    images=[]
    benar_salah=[]

    for i in range(0,len(data)):
        question.append(data[i]['question'])
        solution.append(data[i]['solution'])
        answer.append(data[i]['answer'])
        images.append(data[i]['image'])

    if True: 
        if request.method=='POST':
            return render_template('scorepage.html',user=user,level=level,star=star,score=score, score_max=score_max, star_max=star_max, corect=count, wrong=countt, benar_salah=benar_salah, jawaban=jawaban_, jawaban_user=jawaban_user_)     
        return render_template(f'level{level}.html', data=data, question=question, solution=solution, answer=answer, benar_salah=benar_salah, level=level, gambar=images)
    else:
        return redirect(url_for('./login'))

@app.route('/logout')
def logout():
    resp = make_response(redirect('./login'))
    resp.set_cookie('SESSIONID', '', expires=0)
    return resp
    
if __name__ == "__main__":
    app.run(debug=True)