from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    video_info = None
    if request.method == 'POST':
        link = request.form['link']
        audio_only = 'audio_only' in request.form

        if link:
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
            }

            if audio_only:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                ydl.download([link])

            video_info = {
                'title': info.get('title'),
                'views': info.get('view_count'),
                'duration': info.get('duration'),
                'description': (info.get('description') or '')[:300],
                'uploader': info.get('uploader'),
                'thumbnail': info.get('thumbnail'),
            }

    return render_template('index.html', video_info=video_info)

if __name__ == '__main__':
    app.run(debug=True)