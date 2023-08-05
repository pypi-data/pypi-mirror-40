import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

strings_module = setuptools.Extension('strings',
                           sources=['strings_pkg/strings.c'],
                           language='c')

setuptools.setup(
    name="strings_pkg",
    version="0.0.1",
    author="lpe234",
    author_email="lpe234@qq.com",
    description="string extension package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lpe234/strings_pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    ext_modules=[strings_module]
)
