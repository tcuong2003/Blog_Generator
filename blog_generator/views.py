from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import json
import os
import assemblyai as aai
import yt_dlp
import google.generativeai as genai
from django.utils.text import slugify
from django.http import HttpRequest
from blog.models import BlogPost


@login_required
def blog_generator_form(request):
    return render(request, 'blog_generator_form.html')

@csrf_exempt
@login_required
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)

        title = yt_title(yt_link)

        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': " Failed to get transcript"}, status=500)

        blog_content = generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error': " Failed to generate blog article"}, status=500)

        new_blog_article = BlogPost.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_link=yt_link,
            generated_content=blog_content,
        )
        new_blog_article.save()

        return JsonResponse({'content': blog_content})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def yt_title(yt_link):
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(yt_link, download=False)
            return info_dict.get('title', 'Unknown Title')
    except Exception as e:
        print(f"Error fetching YouTube title: {e}")
        return None

def download_audio(yt_link, request=None):
    output_path = settings.MEDIA_ROOT
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{output_path}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'postprocessor_args': ['-loglevel', 'panic'],
            'keepvideo': True,
            'noplaylist': True,
            'quiet': True,
            'no-warnings': True,
            'ignoreerrors': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_link, download=True)
            original_title = info.get('title', 'audio_file')
            safe_title = slugify(original_title)
            expected_audio_path = os.path.join(output_path, f"{safe_title}.mp3")

            for file in os.listdir(output_path):
                if file.endswith(".mp3") and safe_title in slugify(file):
                    actual_audio_path = os.path.join(output_path, file)
                    if actual_audio_path != expected_audio_path:
                        os.rename(actual_audio_path, expected_audio_path)
                    return expected_audio_path

    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = "3e9d7920cecb498f99538fe7c802f35e"

    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(language_detection=True) 

    try:
        transcript = transcriber.transcribe(audio_file, config=config)
        return transcript.text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


genai.configure(api_key="AIzaSyBkfIJFu6F2C7I5NqfGAWxdcO3DZQCP53A")
def generate_blog_from_transcription(transcription):
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""Dựa vào bản chép lại từ một video YouTube dưới đây, hãy viết một bài blog chi tiết bằng tiếng Việt. 
    Hãy viết bài một cách tự nhiên, không giống như một video YouTube, mà giống một bài viết chuyên nghiệp trên blog.

    Bản chép lại:
    {transcription}

    Bài viết:"""

    response = model.generate_content(prompt)

    if response and hasattr(response, 'text'):
        return response.text.strip()
    else:
        return "Lỗi khi tạo nội dung bằng AI."