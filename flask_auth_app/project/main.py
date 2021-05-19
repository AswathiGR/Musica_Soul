
from flask import Blueprint, render_template,request,send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import secrets
from . import db
import os, sys
from moviepy.editor import *
from .models import Post,User
from . import db

main = Blueprint('main', __name__,static_folder='static',template_folder='templates')


@main.route('/')
def index():
    if current_user.is_authenticated:
        user = User.query.filter_by(name=current_user.name).first_or_404()
        posts = Post.query.filter_by(author=user)
        return render_template('index.html',post=posts)
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/profile',methods=['POST'])
def profile_post():
    file=request.files['input']
    x= secrets.token_hex(20)
    y=x+'.mp3'
    filePath = "./project/static/file/"+secure_filename(y)
    file.save(filePath)
        
    audio = AudioFileClip(filePath)
    image = VideoFileClip('./2.mp4').set_duration(audio.duration) 

    video = image.set_audio(audio)
    z=x+'.mp4'

    video.write_videofile('./project/static/file/'+z, fps=1)
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_post = Post(author=current_user,video_file= z)

    # add the new user to the database
    db.session.add(new_post)
    db.session.commit()
    
    return render_template('profile.html', o=z, name=current_user.name)

@main.route('/down/<paths>')
def down(paths):
    o='./static/file/'+str(paths)
    return send_file(o,as_attachment=True)
