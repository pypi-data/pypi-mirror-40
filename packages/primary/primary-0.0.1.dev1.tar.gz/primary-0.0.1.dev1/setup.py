from distutils.core import setup
from setuptools import find_packages
import primary


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='primary',
    packages=find_packages(),
    version=primary.__version__,
    license='MIT',
    description='Client for Primary\'s trading/market-data/etc. APIs (http://api.primary.com.ar/).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Martín Raúl Villalba',
    author_email='martin@martinvillalba.com',
    url='https://github.com/mvillalba/python-primary',
    python_requires='>=3',
    install_requires=[
        'requests>=2.21.0',
    ],
    entry_points={
        'console_scripts': [
            'primary=primary.cli.main',
        ],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ],
)
