"""The setup script."""

from setuptools import setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    author="Yann Michel Le Coz",
    author_email='yann.lecoz@ynov.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Natural Language :: French",
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Cette application permet de jouer au jeu d'arcade Pong.",
    license="GNU General Public License v3",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='Pong19-Zero',
    name='Pong19-Zero',
    packages=["Pong19-Zero"],
    url='https://github.com/Zocel/Pong19-Zero',
    version = '0.0.1',
    zip_safe=False,
)
