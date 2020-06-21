import os
import uuid

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory, send_file
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
    return render_template('music/index.html')


@bp.route('/song/<id>', methods=['GET'])
@login_required
def song(id):
    song_id = id
    if song_id == None:
        return render_template('error/404.html'), 404
    db = get_db()
    sql = 'SELECT * FROM song WHERE id={}'.format(song_id)
    song = db.execute(
        sql
    ).fetchone()
    if song == None:
        return render_template('error/404.html'), 404
    return render_template('music/song.html', song=song)


@bp.route('/search')
@login_required
def search():
    keyword = '{}%'.format(request.args.get('keyword', ''))
    search_type = request.args.get('search_type', '')
    db = get_db()
    sql = 'SELECT * FROM song'
    if search_type == 'title':
        sql += ' WHERE title like \'{}\''.format(keyword)
    elif search_type == 'album':
        sql += ' WHERE album like \'{}\''.format(keyword)
    elif search_type == 'artist':
        sql += ' WHERE artist like \'{}\''.format(keyword)
    songs = db.execute(
        sql
    ).fetchall()
    return render_template('music/index.html', songs=songs)


@bp.route('/all_songs')
@login_required
def list_songs():
    db = get_db()
    sql = 'SELECT * FROM song'
    songs = db.execute(
        sql
    ).fetchall()
    return render_template('music/all_songs.html', songs=songs)


@bp.route('/playlist')
@login_required
def playlist():
    db = get_db()
    sql = 'SELECT * FROM song WHERE user={}'.format(g.user['id'])
    songs = db.execute(
        sql
    ).fetchall()
    return render_template('music/playlist.html', songs=songs)


@bp.route('/delete', methods=['POST'])
@login_required
def delete():
    if request.method == 'POST':
        db = get_db()
        sql = 'DELETE FROM song WHERE id={} and user={}'.format(request.form['id'], g.user['id'])
        db.execute(
            sql
        )
        db.commit()
    return redirect(url_for('music.playlist'))


@bp.route('/<song>')
@login_required
def get_song(song):
    return send_from_directory(current_app.static_folder, 'music/{}'.format(song))


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


@bp.route('/download', methods=('GET',))
def download():
    song_id = request.args.get('id')
    if song_id == None:
        return render_template('error/404.html'), 404
    db = get_db()
    sql = 'SELECT url FROM song WHERE id={}'.format(song_id)
    song = db.execute(
        sql
    ).fetchone()
    if song == None:
        return render_template('error/404.html'), 404
    return send_file(current_app.static_folder+'/music/{}'.format(song['url']), as_attachment=True)
