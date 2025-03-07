from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, Video
from flask_migrate import Migrate
import os

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
    videos = Video.query.all()  # Buscar todos os vídeos no banco de dados
    return render_template('index.html', videos=videos)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        video_file = request.files['video']
        if video_file and video_file.filename.endswith('.mp4'):
            # Salvar o arquivo de vídeo
            video_filename = video_file.filename
            video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))

            # Adicionar o vídeo ao banco de dados
            novo_video = Video(filename=video_filename, title='Novo')  # Defina um título
            db.session.add(novo_video)
            db.session.commit()

            return redirect(url_for('admin'))  # Redirecionar para a página de admin

    # Buscar todos os vídeos na tabela 'video'
    videos = Video.query.all()  # Certifique-se de que está consultando corretamente

    return render_template('admin.html', videos=videos)

@app.route('/admin/delete_video/<int:video_id>', methods=['GET'])
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    
    # Deletar o vídeo do banco de dados
    db.session.delete(video)
    db.session.commit()

    # Redirecionar de volta para a página de administração
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
