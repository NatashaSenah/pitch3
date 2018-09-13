from flask_login import login_required, current_user
from flask import render_template,request,redirect,url_for,abort
from ..models import  User,Pitch
from .forms import CommentForm,UpdateProfile,AddPitch
from .. import db,photos
from . import main
import markdown2


@main.route('/')
def index():
    return render_template('index.html',title='tasha')
@main.route('/pitch/comment/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_review(id):
    form = CommentForm()
    pitch = get_pitch(id)
    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data

        # Updated review instance
        new_comment = Comment(pitch_id=pitch.id,pitch_title=title,pitch_comment=comment,user=current_user)

        # save review method
        new_review.save_review()
        return redirect(url_for('.pitch',id = pitch.id ))

    title = f'{pitch.title} review'
    return render_template('new_review.html',title = title, review_form=form, pitch=pitch)
@main.route('/review/<int:id>')
def single_review(id):
    review=Review.query.get(id)
    if review is None:
        abort(404)
    format_review = markdown2.markdown(review.movie_review,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('review.html',review = review,format_review=format_review)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST','GET'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/user/pitch', methods=['GET', 'POST'])
def post():
    form = AddPitch()
    if form.validate_on_submit():
        new_pitch = Pitch(pitch_content=form.pitch.data, user_id=current_user.id)
        db.session.add(new_pitch)
        db.session.commit()
    pitch=Pitch.query.all()
    return render_template('profile/update.html',form=form,pitch=pitch)
@main.route('/user/comment',methods=['GET','POST'])
def comment():
    form = form
