from distutils.core import setup
import codecs

import main

setup (

    name = "NuO",
    version = "0.1.3",
    author = "Akshit Grover",
    author_email = "akshit.grover2016@gmail.com",
    description = "Static website templating engine, Generates HTML pages using .nuo template files and data in JSON files.",
    packages = ["."],
    long_description = open("README.rst").read(),
    entry_points={
        "console_scripts": [
            "nuo = main:main"
        ]
    },
    install_requires = [
        "PyYAML"
    ],
    license = "LICENSE",
    url = "https://github.com/akshitgrover/NuO",
    keywords = "static html website parser nuo",
    classifiers = [

        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
    
    ]

)