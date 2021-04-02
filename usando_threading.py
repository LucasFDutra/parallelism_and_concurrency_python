"""
Objetivo: Baixar 100 imagens de uma api (pokeapi)

TEMPO: 6s com 5 threads

"""

from datetime import datetime
from requests import get
from urllib.parse import urljoin
from threading import Event, Thread
from queue import Queue
from functions import target
from time import sleep

event = Event()
fila = Queue(maxsize=101)
BASE_URL = 'https://pokeapi.co/api/v2/'


def get_urls():
    pokemons = get(urljoin(BASE_URL, 'pokemon/?limit=100')).json()['results']
    [fila.put(pokemon) for pokemon in pokemons]
    event.set()
    fila.put('Kill')

class Worker(Thread):
    def __init__(self, target, queue, *, name='Worker'):
        super().__init__()
        self.name = name
        self.queue = queue
        self._target = target
        self._stoped = False
        print(self.name, 'started')

    def run(self):
        event.wait()
        while not self.queue.empty():
            pokemon = self.queue.get()
            if pokemon == 'Kill':
                self.queue.put(pokemon)
                self._stoped = True
                print(self.name, pokemon)
                break
            print(self.name, pokemon)
            self._target(pokemon)

    def join(self):
        while not self._stoped:
            sleep(0.1)


def set_workers(n, target, queue):
    return [Worker(target=target, queue=queue, name=f'worker_{n}') for n in range(n)]


def start_workers(workers):
    [worker.start() for worker in workers]


def join_workers(workers):
    [worker.join() for worker in workers]


strart_time = datetime.now()

get_urls()
workers = set_workers(5, target=target, queue=fila)
start_workers(workers)
join_workers(workers)

time_elapsed = datetime.now() - strart_time

print(f'Tempo total {time_elapsed}')
