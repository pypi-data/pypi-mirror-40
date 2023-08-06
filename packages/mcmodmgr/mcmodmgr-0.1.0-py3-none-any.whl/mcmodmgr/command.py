import logging
import logging.config
import sys

from multiprocessing.pool import ThreadPool
from os import path
from urllib.parse import urlparse

import requests
import yaml

from lxml import html

from .logging import config_logger

logger = logging.getLogger()


def get_mod_link(mc_version, mod_name, mod_version):
    URL = f'https://minecraft.curseforge.com/projects/{mod_name}/files'
    resp = requests.get(URL)
    doc = html.fromstring(resp.text)
    doc.make_links_absolute(URL)

    for tr in doc.cssselect('table.listing tbody tr'):
        download_link = tr.cssselect('td:nth-child(2) a')[0].get('href')
        name = tr.cssselect('td:nth-child(2) a[data-name]')[0].get('data-name')
        # TODO: parse additional versions
        mc_version = tr.cssselect('td.project-file-game-version .version-label')[0].text

        if mc_version == mc_version and name == mod_version:
            link = download_link
            break
    else:
        logger.error('Cannot find MOD')
        link = None

    return (mod_name, mod_version, link)


def download(mod_name, mod_version, link):
    if link is None:
        logger.error(f'Cannot download {mod_name} {mod_version}')
        return

    logger.info(f'Downloading {link}')

    resp = requests.get(link)
    filename = resp.headers.get('Content-Disposition')
    if filename is None:
        filename = path.basename(urlparse(resp.url).path)

    with open(path.join('mods', filename), 'wb') as fp:
        fp.write(resp.content)


def main():
    config_logger()
    config_file = sys.argv[1]

    pool = ThreadPool(4)

    if not path.isdir('mods'):
        logger.error('Cannot find "mods" directory')
        exit(1)

    with open(config_file) as fp:
        config = yaml.load(fp)

    link_map = pool.map(
        lambda x: get_mod_link(config, *x),
        config['mod_list'].items()
    )

    pool.map(
        lambda x: download(*x),
        link_map
    )

    pool.close()
