from flask import Blueprint,render_template,url_for,request,redirect,escape
import string
from math import floor
from .extensions import db
from .models import Link

short=Blueprint('short',__name__)

@short.route('/<short_url>')
def redirect_to_url(short_url):
    ##search in db if short url is exist if true redirect to the original url else redirect to page not found
    link=Link.query.filter_by(short_url=short_url).first_or_404()
    
    link.visits=link.visits + 1

    
    db.session.commit()
    
    return redirect(link.original_url)
    

##home page
@short.route('/')
def index():
    return render_template('index.html')

##handling the post request
@short.route('/add_link',methods=['POST'])
def add_link():
    
    original_url=request.form['original_url']
    
    link=Link(original_url=original_url)
    ##update the db
    db.session.add(link)
    db.session.commit()

    ##create short url using base62
    link.short_url=toBase62(link.id)
    
    db.session.commit()

    new_link="http://localhost:5000/"+link.short_url
    return redirect(url_for("short.link",new_link=new_link, original_url=link.original_url))

@short.route("/link")
def link():
    return render_template('link_added.html', 
        new_link=escape(request.args.get('new_link')), original_url=escape(request.args.get('original_url')))
##statistic info
@short.route('/stats')
def stats():
    pass

##heandling the error massage
@short.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


def toBase62(num, b = 62):
    if b <= 0 or b > 62:
        return 0
    base = string.digits + string.ascii_lowercase + string.ascii_uppercase
    r = num % b
    res = base[r]
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res