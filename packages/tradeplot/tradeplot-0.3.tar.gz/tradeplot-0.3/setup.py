from setuptools import find_packages, setup

requirements = [
    'numpy',
    'pyecharts',
    'pyecharts_snapshot',
]

setup(
    name='tradeplot',
    version='0.3',
    author='YVictor',
    author_email='yvictor3141@gmail.com',
    url='https://github.com/Yvictor/TradePlot',
    description='use pyecharts to realize trading chart',
    long_description=__doc__,
    packages=find_packages(exclude=['tests*']),
    zip_safe=False,
    install_requires=requirements,
    platforms='any',
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])
