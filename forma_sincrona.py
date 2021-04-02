"""
Objetivo: Baixar 100 imagens de uma api (pokeapi)

TEMPO: 32s

"""

from datetime import datetime
from os import makedirs
from os.path import exists
from shutil import rmtree, copyfileobj
from requests import get
from urllib.parse import urljoin

PATH = 'download'
BASE_URL = 'https://pokeapi.co/api/v2/'

if exists(PATH):
    rmtree(PATH)
makedirs(PATH)

def download_file(name, url, *, path=PATH, type_='png'):
    """Faz o download de um arquivo."""
    response = get(url, stream=True)
    file_name = f'{path}/{name}.{type_}'
    with open(file_name, 'wb') as f:
        copyfileobj(response.raw, f)
    return file_name

def get_sprite_url(url, sprite='front_default'):
    return get(url).json()['sprites']['front_default']


strart_time = datetime.now()

pokemons = get(urljoin(BASE_URL, 'pokemon/?limit=100')).json()['results']

images_url = {image['name']: get_sprite_url(image['url'])  for image in pokemons}

files = [download_file(name, url) for name, url in images_url.items()]

time_elapsed = datetime.now() - strart_time

print(f'Tempo total {time_elapsed}')