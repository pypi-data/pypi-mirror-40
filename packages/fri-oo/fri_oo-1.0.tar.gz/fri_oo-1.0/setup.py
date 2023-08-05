from setuptools import setup

setup(name = 'fri_oo',
    version = '1.0',
    description = 'FRI algorithm implementation',
    author = 'Leo Serena',
    author_email = 'leo.serena@epfl.ch',
    licence = 'EPFL',
    packages = ['fri_oo'],
    url = 'https://c4science.ch/source/FRIsOO.git',
    install_requires = [
        'scipy',
        'numpy',
         'pandas',
        'matplotlib',
        'joblib' ],
    zip_safe = False,
    include_package_data = True)
