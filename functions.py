from os import makedirs
from os.path import exists
from shutil import rmtree, copyfileobj
from requests import get


PATH = 'download'

if exists(PATH):
    rmtree(PATH)
makedirs(PATH)

def get_sprite_url(url, sprite='front_default'):
    """Pega a url do sprite"""
    return url['name'], get(url['url']).json()['sprites']['front_default']


def get_bin_file(args):
    """"Faz download do binário do sprite"""
    name, url = args
    return name, get(url, stream=True).raw


def save_file(args, path=PATH, type_='png'):
    """Salva o binário no disco como imagem."""
    name, binary = args
    file_name = f'{path}/{name}.{type_}'
    with open(file_name, 'wb') as f:
        copyfileobj(binary, f)
    return file_name


# isso aqui é uma closure, mas o multiprocessing não aceita closure, então para ele vou criar uma classe
def pipeline(*funcs):
    def inner(argument):
        state = argument
        for func in funcs:
            state = func(state)
    
    return inner


class Pipeline:
    def __init__(self, *funcs):
        self.funcs = funcs

    def __call__(self, argument):
        state = argument
        for func in self.funcs:
            state = func(state)
        return state


target = pipeline(get_sprite_url, get_bin_file, save_file)
target_class = Pipeline(get_sprite_url, get_bin_file, save_file)