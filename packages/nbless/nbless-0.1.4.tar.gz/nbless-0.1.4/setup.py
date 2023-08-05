import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nbless",
    version="0.1.4",
    author="Martin Skarzynski",
    author_email="marskar@gmail.com",
    description="Create Jupyter notebooks from Markdown and Python scripts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marskar/nbless",
    packages=setuptools.find_packages('src/nbless'),
    # scripts=['nbless.py', 'nbuild.py', 'nbexec.py'],
     entry_points={
         'console_scripts': [
             'nbless = src.nbless.cli.nbless_click:nbless_click',
             'nbuild = src.nbless.cli.nbuild_click:nbuild_click',
             'nbexec = src.nbless.cli.nbexec_click:nbexec_click',
             'nbconv = src.nbless.cli.nbconv_click:nbconv_click',
         ]
     },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
        install_requires=[
        'jupyter'
    ]
)

