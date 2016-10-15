from setuptools import find_packages, setup

setup(
    name="xorgsearch",
    install_requires=[
        'mysqlclient',
    ],
    setup_requires=[
        'setuptools',
    ],
    license='GPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.4",
    ],
)
