from distutils.core import setup

setup(
    name='ProcTitle',
    version='0.1.0',
    author='Glenn Franxman',
    author_email='gfranxman@gmail.com',
    packages=['proctitle'],
    scripts=[],
    url='http://pypi.python.org/pypi/ProcTitle/',
    license='LICENSE.txt',
    description='Context Manager to set/reset the current process name.',
    long_description=open('README.txt').read(),
    install_requires=[
        "setproctitle >= 1.1.10",
    ],
)
