import setuptools

requirements = [
    'zeep',
    'pyopenssl',
    'clabe'
]

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='stpmex',
    version='1.0.0',
    author='Cuenca',
    author_email='dev@cuenca.io',
    description='Integration to stpmex.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/stpmex-python',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'vcrpy'],
    extras_require={
        'dev': [
            'pytest>=3',
            'ipython',
            'ipdb',
            'pycodestyle',
            'pytest',
            'vcrpy'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'stpmex = stpmex.__main__:main'
        ]
    }
)
