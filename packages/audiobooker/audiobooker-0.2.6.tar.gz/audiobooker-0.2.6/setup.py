from setuptools import setup

setup(
    name='audiobooker',
    version='0.2.6',
    packages=['audiobooker', 'audiobooker.scrappers', 'audiobooker.utils'],
    install_requires=["requests", "bs4", "feedparser", "fuzzywuzzy"],
    url='https://github.com/JarbasAl/audiobooker',
    license='MIT',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description='audio book scrapper'
)
