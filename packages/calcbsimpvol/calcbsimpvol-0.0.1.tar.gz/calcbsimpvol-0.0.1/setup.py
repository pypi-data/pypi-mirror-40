from setuptools import setup, find_packages


setup(
    name='calcbsimpvol',
    version='0.0.1',
    license='MIT',
    description='Calculate Black Scholes Implied Volatility - Vectorwise',
    url='https://duckduckgo.com',
    author='Erkan Demiralay',
    author_email='erkan@erkan.io',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial ',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='options implied volatility option iv ivol options-on-futures ivsurface black-scholes',
    install_requires=['numpy', 'scipy', 'matplotlib'],
#    packages=find_packages(exclude=['tests*', 'docs']),
#    package_data={'data': ['*.json']},
    project_urls={
        'Documentation': 'https://dukcduckgo.com',
        'Bug Reports': 'https://dukcduckgo.com',
        'Source': 'https://dukcduckgo.com',
    },
)

