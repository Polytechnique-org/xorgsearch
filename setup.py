from setuptools import find_packages, setup

setup(
    name="xorgsearch",
    install_requires=[
        'elasticsearch-dsl'
    ],
    setup_requires=[
        'setuptools',
    ],
    extras_requires={
        'dump': ['mysqlclient'],
    },
    entry_points={
        'console_scripts': [
            'xorgsearch-dump = xorgsearch.dump.main [dump]',
            'xorgsearch-inject = xorgsearch.load_json.main',
        ],
    },
    license='GPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.4",
    ],
)
