import os
import uuid

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort

from src.auth import login_required
from src.db import get_db, current_app

bp = Blueprint('music', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/')
@login_required
def index():
    db = get_db()
    sql = 'SELECT * FROM song WHERE user={}'.format(g.user['id'])
    songs = db.execute(
        sql
    ).fetchall()
    return render_template('music/index.html', songs=songs)


@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        album = request.form['album']
        error = None

        if not title:
            error = 'Title is required.'

        if not artist:
            error = 'Title is required.'

        if not album:
            error = 'Title is required.'

        if 'file' not in request.files:
            error = 'No file part'

        file = request.files['file']
        if not len(file.filename):
            error = 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename('{}.mp3'.format(str(uuid.uuid4())))
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        else:
            error = 'Only mp3 file can be upoaded'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO song (user, title, artist, album, url)'
                ' VALUES (?, ?, ?, ?, ?)',
                (g.user['id'], title, artist, album, filename)
            )
            db.commit()
            return redirect(url_for('music.index'))

    return render_template('music/upload.html')
