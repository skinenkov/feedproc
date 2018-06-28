from setuptools import setup, find_packages

setup(
    name='feedproc',
    # Versions should comply with PEP440. Or just http://semver.org/.
    version='0.1.0',
    description='Library for processing xml/csv feeds into json/orm',
    url='http://stash.firstgaming.com/projects/RUB/repos/rub90-slots-outcomebet-client',
    author='Ihor Ivankov',
    author_email='skinenkov@gmail.com',
    classifiers=[
        'Development Status :: 3 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: PARSERS',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='xml feeds processing, convert xml to json',
    packages=find_packages(exclude=[]),
    install_requires=['requests'],
)