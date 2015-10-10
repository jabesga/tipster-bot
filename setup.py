from setuptools import setup, find_packages


def get_version(fname='bot.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


setup(
    name='tipster-bot',
    description='The tipster bot',
    version=get_version(),
    url='https://github.com/jabesga/tipster-bot',
    install_requires=['setuptools', 'requests'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            "tipster = bot:main",
        ],
    },
)
