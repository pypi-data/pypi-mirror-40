import os
import pathlib
import re
from distutils.core import setup

here = pathlib.Path(__file__).parent
fname = here / "mem_usage_ui" / "__init__.py"


with fname.open() as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'$", fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

with open("requirements.txt") as f:
    requirements = [line for line in f.readlines()]

setup(
    name='mem_usage_ui',
    version=version,
    description='UI for memory usage of processes',
    long_description=README,
    author='Dmytro Smyk',
    author_email='porovozls@gmail.com',
    url='https://github.com/parikls/mem_usage_ui',
    packages=["mem_usage_ui"],
    package_data={
        'mem_usage_ui': ['templates/index.html', 'static/js/build.js']
    },
    classifiers=[
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=requirements,
    python_requires='>=3.5.3',
    entry_points={
        'console_scripts': ['mem_usage_ui = mem_usage_ui.__main__:main']
    }
)
