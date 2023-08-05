from setuptools import setup, find_packages

setup(
    name = "qvmake",
    version = "0.0.1",
    decription = "compile your code for qualvision",
    author = "MuxingMax",
    package = find_packages(),
    install_requires = [
        "sh",
        "Click",
    ],
    entry_points = {
        'console_scripts': [
            'qvmake = qvmake:main',
        ],
    }

)