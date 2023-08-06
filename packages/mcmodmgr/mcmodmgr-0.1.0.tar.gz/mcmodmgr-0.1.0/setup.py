from setuptools import find_packages, setup
from mcmodmgr._version import __version__ as version

install_reqs = [
    'PyYaml>=3.13',
    'cssselect>=1.0.3',
    'lxml>=4.3.0',
    'requests>=2.21.0',
]

setup(
    name='mcmodmgr',
    description='Minecraft mod downloader',
    long_description='',
    version=version,
    url='https://github.com/Kjwon15/mcmodmgr',
    download_url='https://github.com/Kjwon15/mcmodmgr/releases',
    author='Kjwon15',
    author_email='kjwonmail@gmail.com',
    entry_points={
        'console_scripts': [
            'mcmodmgr = mcmodmgr.command:main'
        ]
    },
    packages=find_packages(),
    install_requires=install_reqs,
)
