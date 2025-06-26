import re
import os
try:
    import yt_dlp
except ImportError:
    print("⚠️ Aviso: yt-dlp não está instalado. Instalando agora...")
    os.system('pip install yt-dlp')
    import yt_dlp
import unicodedata
from multiprocessing import Process, cpu_count
from sys import argv
from tkinter import filedialog
from time import sleep
from random import randint
import subprocess
DECIBEIS = 0.6

invalid_filename_chars = [34, 42, 47, 58, 60, 62, 63, 92, 124]

VIDEOFORMATLISTMP3 = ["mov", "wmv", "avi", "webm", "avchd", "mp4",
                      "mkv", "flv", "f4v", "swf", "mpeg", "mpeg2", "mpeg-4"]
audio_extensions = [
    "aac",
    "wav",
    "flac",
    "ogg",
    "wma",
    "m4a",
    "alac",
    "aiff",
    "opus",
    "amr",
    "dsd",
    "pcm",
]
VIDEOFORMATLISTMP3 = list(set(VIDEOFORMATLISTMP3+audio_extensions))
COMMANDMP3 = """ffmpeg -i "{}" -vn -ar 44100 -ac 2 -b:a 198k -hide_banner -loglevel quiet -y "{}" """

VIDEOFORMATLISTDVD = ["mp4", "mov", "wmv", "avi", "webm", "avchd",
                      "mkv", "flv", "f4v", "swf", "mpeg2", "mpeg-4"]


import os
import re

def renomear_arquivos_da_pasta(pasta):
    for nome_antigo in os.listdir(pasta):
        caminho_antigo = os.path.join(pasta, nome_antigo)

        if os.path.isfile(caminho_antigo):
            # Remove múltiplos espaços e espaços no início/fim
            nome_novo = re.sub(r'\s+', ' ', nome_antigo).strip()

            # Renomeia se o nome novo for diferente
            if nome_novo != nome_antigo:
                caminho_novo = os.path.join(pasta, nome_novo)
                os.rename(caminho_antigo, caminho_novo)
                print(f'Renomeado: "{nome_antigo}" → "{nome_novo}"')



def melhorar_som(input_filename, output_filename, margem_db=0.1):
    """
    Normaliza o volume do áudio com base no pico máximo.
    Se o áudio já estiver perto do máximo, não altera.

    Args:
        input_filename (str): caminho do arquivo de entrada.
        output_filename (str): caminho do arquivo de saída.
        margem_db (float): tolerância em dBFS para considerar que o áudio já está suficientemente alto.
    """
    print(f"Normalizer:: ♻ [{input_filename}]",end='\t')

    # 1. Executa o ffmpeg com astats e captura a saída
    cmd_astats = [
        "ffmpeg", "-i", input_filename,
        "-af", "astats=metadata=1:reset=1",
        "-f", "null", "-"
    ]

    # result = subprocess.run(cmd_astats, stderr=subprocess.PIPE, text=True)
    result = subprocess.run(
        cmd_astats,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True
    )
    stderr = result.stderr

    # 2. Procura o "Max level" (pico máximo) na saída
    match = re.search(r"Overall.*?Max level:\s*([\d.]+)", stderr, re.DOTALL)

    if not stderr:
        print(f"\n⛔[\033[31m{input_filename}\033[m]\n")
        return

    
    if not match:
        print(f"\n❌[\033[31m{input_filename}\033[m]\n")
        return

    max_level = float(match.group(1))

    # 3. Se já estiver suficientemente alto, copia o arquivo
    if max_level >= 1.0 - margem_db:
        print("\n❎[\033[33m{input_filename}\033[m]\n")
        subprocess.run(["ffmpeg", "-y", "-i", input_filename, output_filename],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        return

    # 4. Calcula o ganho necessário
    gain = 1.0 / (.2+max_level)

    # 5. Aplica o ganho
    cmd_volume = [
        "ffmpeg", "-y", "-i", input_filename,
        "-af", f"volume={gain}",
        output_filename
    ]
    subprocess.run(cmd_volume,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)    
    os.remove(input_filename)
    os.rename(output_filename, input_filename)
    print(f"\n✅[\033[32m{input_filename}\033[m]🟢\n")


def obter_urls_playlist(playlist_url):
    try:
        comando = [
            "yt-dlp",
            "--flat-playlist",
            "--print", "url",
            "--quiet",
            "--skip-unavailable-fragments",
            "--default-search",
            "ytsearch"
        ]
        resultado = subprocess.run(
            comando + [playlist_url], capture_output=True, text=True)
        if resultado.returncode != 0:
            print("⚠️ Aviso: Alguns vídeos podem estar indisponíveis.")
        urls = resultado.stdout.strip().split("\n")
        return urls
    except Exception as e:
        print("Erro ao obter a playlist: {}".format(e))
        return []


class FilaDeProcessos:
    def __init__(self, name="", size=10):
        self._id = randint(1, 10000)
        print("\n🟦 Queue ID {} created. . .".format(self._id))
        self.name = f" ({name}) " if name else ""
        self.size = min(size, cpu_count()-2)
        self.list = []
        self.occuped = []
        self.num_process_alive = 0

    def add_process(self, p: Process):
        self.list.append(p)

    def __start_bucket(self):
        if not self.list:
            return False
        for i in range(self.size-len(self.occuped)):
            try:
                proc = self.list.pop()
                proc.start()
                proc.is_joined = False
                print("\n  🔵 START :: {}".format(proc.name+self.name))
                self.occuped.append(proc)
            except:
                pass

    def run(self):
        print("\n  ♻️ Running queue of processes. . .")
        self.__start_bucket()
        while self.list or self.occuped:
            sleep(.5)
            for ix, proc in enumerate(self.occuped):
                if not proc.is_alive():
                    proc = self.occuped.pop(ix)
                    print("\n  🟢 END :: {}".format(proc.name+self.name))
                    self.__start_bucket()
                if not proc.is_joined:
                    proc.is_joined = True
                    proc.join()
        print("\n🟩 Queue ID {} ended. . .".format(self._id))


def sanitize_filename(name):
    name = unicodedata.normalize('NFC', name).title()
    return ''.join(c for c in name if ord(c) not in invalid_filename_chars)[:45]


def get_name_extension(fname):
    *name, ext = fname.split('.')
    if name:
        return ' '.join(name), ext
    return ext, ''


def converte_dvd(fname, new_filename):
    cfg_resolution = " -vf scale=720:576 "
    cfg_aspect_ratio = " -aspect 16:9 "
    cfg_bit_rate = " -b:v 1M "
    cfg_codec_audio = " -c:a ac3 "
    configs_compiladas = cfg_codec_audio + cfg_resolution
    COMMAND = """ffmpeg -i "{}"
  *** -q:v 2 -qmin 2 -qmax 31
  -c:v mpeg2video
  -b:a 192k
  -b:v 4M
  -bufsize 15M
  -maxrate 5M
  -muxrate 6M
  -trellis 2 -bf 2
  -hide_banner -loglevel quiet
  -y "{}"
  """.replace("\n", " ")
    COMMAND = COMMAND.replace('***', configs_compiladas)
    new_name = get_name_extension(new_filename)[0] + '.mpeg'
    try:
        cmd = COMMAND.format(fname, new_name)
        ans = os.system(cmd)
    except Exception as e:
        print("Erro ao converter", e)
    finally:
        sleep(5)
        return


def converte_mp3(fname, new_filename):
    new_name = get_name_extension(new_filename)[0] + '.mp3'
    try:
        cmd = COMMANDMP3.format(fname, new_name)
        ans = os.system(cmd)
    except Exception as e:
        print("Erro ao converter", e)
    finally:
        sleep(5)
        return new_name


def converte(main_opts, fname, new_filename, numero):
    num = "{:03d}-".format(numero) if numero else ''
    here = os.getcwd()
    os.chdir(main_opts['folder'])
    just_one_conversion = False
    if main_opts['d'] and main_opts['3']:
        fila = FilaDeProcessos(name="Conversor: "+fname, size=1)
        fila.add_process(Process(target=converte_dvd,
                                 args=(fname, num+new_filename)))
        fila.add_process(Process(target=converte_mp3,
                                 args=(fname, num+new_filename)))
        fila.run()
    else:
        just_one_conversion = True

    if just_one_conversion and main_opts['d']:
        converte_dvd(fname, num+new_filename)

    if just_one_conversion and main_opts['3']:
       new_name = converte_mp3(fname, num+new_filename)

    if main_opts['r'] and (main_opts['d'] or main_opts['3']):
        os.remove(fname)

    if main_opts['db'] and main_opts['3']:
        melhorar_som(new_name, 'nrm_'+new_name, main_opts['db'])
    os.chdir(here)


def download_video(url, main_opts, numero=None):
    folder = main_opts['folder']
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ignoreerrors': True,
        'nooverwrites': False,
        'retries': 5,
        'extractor_retries': 5,
        'socket_timeout': 30,
        'quiet': True,
        'logtostderr': False,
        'loglevel': 'error',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            output_path = ydl.prepare_filename(info)
            fname = os.path.basename(output_path)
            ydl.download([url])
            new_filename, _ = get_name_extension(sanitize_filename(fname))
            new_filename += '.mp4'
    except Exception as e:
        print("Houve um erro no download do vídeo\n\t\t{}\n:::".format(url, e))
        return
    try:
        converte(main_opts, fname, new_filename, numero)
    except Exception as e:
        print("ERRO: [download_video:converte] {}".format(e))


def download_playlist(main_opts):
    video_urls = obter_urls_playlist(main_opts['url'])
    fila = FilaDeProcessos(name="Processando a Playlist")
    numero = 0
    for video_url in video_urls:
        numero += 1
        p = Process(target=download_video, args=(video_url, main_opts, numero))
        fila.add_process(p)
    fila.run()


def menu():
    print("MENU:")
    print("  1. Você quer fazer download de uma playlist (p) ou apenas um vídeo (v)?")
    print(
        "  2. Você quer converter para mp3 (3) DVD (d)?\n  [Se não puser nenhuma dessas duas opções vou somente baixar]")
    print("  3. Caso você converta (3 ou d), você quer remover o arquivo original e",
          "\n  ficar apenas com o arquivo convertido (r)?")
    print("  4. Você quer normalizar o volume do áudio (db)? Digite n.3 para normalizar com margem de 0.3 dBFS.")
    print("    Exemplo: digite \n    p3r\n    para playlist convertida para mp3 e remover o original")
    print("    Outro exemplo: digite \n    vd\n    para fazer download de um único vídeo e converter para DVD,",
          "\n    ficando com os dois arquivos (não remove o original).")
    escolha = [i for i in input("Entre com sua escolha:\n  ").lower() if i]

    if 'p' not in escolha and 'v' not in escolha:
        print("ERRO: Você deve escolher uma playlist (p) ou um vídeo (v) para começar.")
        print("FIM")
        sleep(10)
        exit()
    elif 'p' in escolha and 'v' in escolha:
        print(
            "ERRO: Você não deve escolher os dois ao mesmo tempo: playlist (p) e vídeo (v).")
        print("FIM")
        sleep(10)
        exit()

    main_opts = dict()
    if 'p' in escolha:
        main_opts['p'] = True

    if 'v' in escolha:
        main_opts['p'] = False

    if '3' in escolha:
        main_opts['3'] = True
    else:
        main_opts['3'] = False

    if 'd' in escolha:
        main_opts['d'] = True
    else:
        main_opts['d'] = False

    if 'r' in escolha:
        main_opts['r'] = True
    else:
        main_opts['r'] = False

    if 'n' in ''.join(escolha):
        s = ''.join(escolha)
        db_value = ''.join([i for i in s if i.isdigit() or i == '.'])
        if db_value:
            value_float = float(db_value)
            value = value_float if value_float < 1 else value_float-value_float//1
            main_opts['db'] = value
    else:
        main_opts['db'] = DECIBEIS

    main(main_opts)


def main(main_opts):
    url = input(
        "Digite ou cole o link/url (clique com o botão direito para colar):\n  ").strip()
    print("\nAgora, selecione uma pasta no computador para salvar os arquivos.")
    input("Pressione ENTER para avançar...")
    folder = filedialog.askdirectory(title="Selecione uma pasta")
    if not folder:
        print("\nInválido. Nenhuma pasta foi selecionada. Fechando o programa")
        sleep(10)
        exit()
    else:
        print("\nLegal. Vou baixar os vídeos e convertê-los dentro da pasta\n  {}".format(folder))
    main_opts['url'] = url
    main_opts['folder'] = folder
    if main_opts['p']:
        download_playlist(main_opts)
    else:
        download_video(url, main_opts)
    
    renomear_arquivos_da_pasta(folder)


if __name__ == '__main__':
    if len(argv) == 1:
        os.system('py ' + __loader__.get_filename().split('\\')[-1] + ' . ')
    else:
        menu()
        print("✅ TERMINEI MEU TRABALHO, OBRIGADO!")
        sleep(160)
