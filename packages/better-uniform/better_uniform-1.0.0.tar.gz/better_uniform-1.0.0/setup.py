from setuptools import setup, find_packages

setup(
    name = 'better_uniform',
    version = '1.0.0',
    url = 'https://github.com/j-faria/better_uniform.git',
    author = 'João Faria',
    author_email = 'joao.faria@astro.up.pt',
    description = 'A better scipy.stats.uniform',
    packages = find_packages(),
    install_requires = ['scipy'],
)