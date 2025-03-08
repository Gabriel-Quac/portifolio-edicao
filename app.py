from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, Video
from flask_migrate import Migrate
from visu import get_youtube_views, get_b1_value  # Importando nova função

# Configuração da aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Configuração do Flask-Migrate
migrate = Migrate(app, db)

# Criar banco de dados e aplicar migrações
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    total_views = get_b1_value()  # Chama a função para somar as visualizações
    return render_template('index.html', total_views=total_views)

@app.route('/admin', methods=['GET', 'POST'])
def administrador():
    if request.method == 'POST':
        title = request.form.get('title')
        video_url = request.form.get('url')
        new_video = Video(title=title, url=video_url)
        db.session.add(new_video)
        db.session.commit()
    
    videos = Video.query.all()
    return render_template('admin.html', videos=videos)

@app.route('/admin/delete_video/<int:video_id>', methods=['GET'])
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    return redirect(url_for('administrador'))

if __name__ == '__main__':
    app.run(debug=True)
