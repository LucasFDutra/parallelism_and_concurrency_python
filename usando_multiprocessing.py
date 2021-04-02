"""
Objetivo: Baixar 100 imagens de uma api (pokeapi)

TEMPO: 10s com 5 processos

"""

from datetime import datetime
from requests import get
from urllib.parse import urljoin
from functions import target_class
from time import sleep
from multiprocessing import Pool, Queue


fila = Queue(maxsize=101)
BASE_URL = 'https://pokeapi.co/api/v2/'

def get_urls():
    return get(urljoin(BASE_URL, 'pokemon/?limit=100')).json()['results']


strart_time = datetime.now()

pokemons = get_urls()
worker = Pool(5)
result = worker.map(target_class, pokemons)

time_elapsed = datetime.now() - strart_time

print(f'Tempo total {time_elapsed}')

