from distutils.core import setup

with open("README.txt", "r") as fh:
    long_description = fh.read()

    
setup(
    name="my_print_nester",
    version="0.0.1",
    py_modules=["my_print_nester"],
    author="Muhammad Khalid",
    author_email="khalid41825@outlook.com",
    description="A simple printer that print list of list",
    long_description=long_description,
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
