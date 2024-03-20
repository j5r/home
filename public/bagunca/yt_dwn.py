from pytube import Playlist, YouTube #pytube 15.0.0
#import re
import random
import os
from glob import glob
from string import ascii_letters, digits
CHAR_SET = ascii_letters+digits+"ÁÉÍÓÚáéíóúàÀêôÊÔãõÃÕç_-=()& "


def clean_string(name):
    name = "".join([i for i in name if i in CHAR_SET])
    return " ".join(name.split())


def converte_mp3_pasta(dirname):
    os.chdir(dirname)
    ls = glob("*.mp4")
    print("Convertendo...", dirname, end="")
    for item in ls:
        converte_mp3(item[:-4])
    os.chdir("..")
    print("\rConvertido:", dirname, " "*10, "OK")

def get_filename_without_extension(fname:str):
    if fname.lower().endswith(".mp4") or fname.lower().endswith(".mp3"):
        return fname[:-4]
    else:
        return fname

def converte_mp3(fname):
    comando = """ffmpeg -i "{}" -vn -ar 44100 -ac 2 -b:a 192k "{}" -hide_banner -loglevel error"""
    fname_mp4 = get_filename_without_extension(fname) + ".mp4"
    fname_mp3 = clean_string(get_filename_without_extension(fname).title()) + ".mp3"
    print('Convertendo', fname_mp3, end="\r")
    os.system(comando.format(fname_mp4, fname_mp3))
    print("Fim", " "*len(fname_mp3+'Convertendo '))
    os.remove(fname_mp4)


def download_playlist(playlist, audio_only):
    error_list = []
    fname_list = []
    for ix, video in enumerate(playlist.videos):
        if ix+1 < INDICE:
            continue

        video.title = f"({ix+1}) " + clean_string(video.title.title())
        fname_list.append(get_filename_without_extension(video.title)+".mp4")
        print('Título =', video.title, end='\t')
        if audio_only:
            print('::audio only::')
            try:
                stream = video.streams.get_audio_only()
                stream.download(output_path='.')
            except Exception as e:
                print("ERRO!", ix, video.title, '\n', e)
                error_list.append(
                    {"indice": ix+1, "title": video.title, "erro": str(e)})
                continue
        else:
            print('::video::')
            try:
                stream = video.streams.get_highest_resolution()
                stream.download(output_path='.')
            except Exception as e:
                print("ERRO!", ix, video.title, '\n', e)
                error_list.append(
                    {"indice": ix+1, "title": video.title, "erro": str(e)})
                continue

    if audio_only:
        print("Convertendo...")
        for fname in fname_list:
            try:
                converte_mp3(fname)
            except Exception as e:
                print("Erro durante a conversão do arquivo",fname)
                print(e)
        print("Convertido              OK")

    for i in error_list:
        print(i)


def download_video(video, audio_only):
    video.title = clean_string(video.title.title())
    print(video.title)
    print("Iniciando download...",end="\r")
    if audio_only:
        try:
            stream = video.streams.get_audio_only()
            stream.download(output_path='.')
        except Exception as e:
            print("Houve um erro ao fazer download do vídeo.")
            print(e)
        print("Download concluído com sucesso!")
        print("Convertendo...",end="\r")
        converte_mp3(video.title)        
        print("Convertido com sucesso!")
    else:
        try:
            stream = video.streams.get_highest_resolution()
            stream.download(output_path='.')
        except Exception as e:
            print("Houve um erro ao fazer download do vídeo.")
            print(e)
        print("Download concluído com sucesso!")


if __name__ == "__main__":
    PLAYLIST = bool(int(input("[Playlist=1  Vídeo=0]\t").strip()))
    URL = input('URL\t ').strip()
    PASTA = input('Nome da pasta\t ').strip()
    if PLAYLIST:
        INDICE = int(input('A partir de que vídeo? (digite apenas número)\t '))
    audio_only = bool(int(input('Apenas áudio? [true=1 false=0]\t ')))

    if not URL:
        print("Preciso de uma URL\n\n")
        exit()
    if not PASTA and PLAYLIST:
        PASTA = 'playlist_{:d}'.format(random.randint(100, 100000))
    if not PASTA:
        PASTA = "."

    if PLAYLIST:
        playlist = Playlist(URL)
        print('Um total de', len(playlist.video_urls),
              'vídeos foram encontrados na Playlist.')
    else:
        video = YouTube(URL)
    # playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    try:
        os.mkdir(PASTA)
    except:
        pass
    finally:
        os.chdir(PASTA)
    print(URL)
    print(PASTA)

    # print(''.join([url+'\n' for url in playlist.video_urls]))
    if PLAYLIST:
        download_playlist(playlist,audio_only)
    else:
        download_video(video,audio_only)
