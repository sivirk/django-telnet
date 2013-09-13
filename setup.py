from distutils.core import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="django-telnet",
    packages=["telnet", "telnet.management", "telnet.management.commands"],
    version="0.1",
    extras_require={
        'telnetsrvlib': ['telnetsrv'],
    },
    description="Telnet server for django commands",
    long_description=readme(),
    author="Ivan Svegentcev",
    author_email="sivirk@gmail.com",
    url="https://github.com/sivirk/django-telnet",
    keywords=["gevent", "telnet", "django", "server"],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications",
        "Topic :: Communications :: BBS",
        "Topic :: System :: Shells",
        "Topic :: Terminals",
        "Topic :: Terminals :: Telnet",
    ],
)
