from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

name = 'gw2'
repo = 'python-{}'.format(name)

setup(
    name=name,
    version='0.0.1',
    description=long_description.splitlines()[0],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ravindra Marella',
    author_email='mv.ravindra007@gmail.com',
    url='https://github.com/marella/{}'.format(repo),
    project_urls={
        'Documentation': 'https://marella.github.io/{}/'.format(repo),
        'Source Code': 'https://github.com/marella/{}'.format(repo),
        'Bug Tracker': 'https://github.com/marella/{}/issues'.format(repo),
    },
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='{} guild-wars-2 api client'.format(name),
)
