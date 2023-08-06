import setuptools

with open("README.md", "rb") as fh:
    long_description = fh.read().decode("utf8")

setuptools.setup(
    name="hay",
    version="0.0.7",
    description='基于pyppeteer的chromenium操控库',
    author='白旭东,储国庆',
    author_email='2216403312@qq.com',
    url='https://github.com/oldlwhite/hay',
    long_description=long_description,
    long_description_content_type="text",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyppeteer',
    ]
)