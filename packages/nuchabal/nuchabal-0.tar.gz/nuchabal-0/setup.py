from setuptools import setup, find_packages

setup(
    name='nuchabal',
    version='0',
    packages=find_packages(),
    url='',
    download_url='https://github.com/julienmalard/nuchabal',
    license='GNU GPL 3',
    author='Julien Jean Malard',
    author_email='julien.malard@mail.mcgill.ca',
    description='Kinuk\' ri taq chab\'äl pa ri xekaj wachulew',
    package_data={
        '': ['*.json', '*.txt'],
    }
)
