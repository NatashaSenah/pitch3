from flask_login import login_required
from flask import render_template,request,redirect,url_for,abort
from ..models import Reviews, User
from .forms import ReviewForm,UpdateProfile
from .. import db,photos
@main.route('/pitch/review/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_review(id):
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
