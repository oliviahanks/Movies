from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]
    
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name = 'disney_movie_analysis',
    version = '0.1.1',
    description = 'We looked at subsets of Disney movies and ran analysis on them.',
    author = ['Daisy Harris', 'Olivia Hanks'],
    author_email = ['dasharon@byu.edu', 'hankso@byu.edu'],
    packages = find_packages(),
    install_requires = parse_requirements('requirements.txt'),
    package_data = {'disney_movie_analysis': ['datasets/*.csv']},
    long_description = long_description
)
