from flask_login import login_required, current_user
from flask import render_template,request,redirect,url_for,abort
from ..models import Reviews, User
from .forms import ReviewForm,UpdateProfile
from .. import db,photos
@main.route('/pitch/review/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_review(id):
    form = ReviewForm()
    pitch = get_pitch(id)
    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data

        # Updated review instance
        new_review = Review(pitch_id=pitch.id,pitch_title=title,pitch_review=review,user=current_user)

        # save review method
        new_review.save_review()
        return redirect(url_for('.pitch',id = pitch.id ))

    title = f'{pitch.title} review'
    return render_template('new_review.html',title = title, review_form=form, pitch=pitch)
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
