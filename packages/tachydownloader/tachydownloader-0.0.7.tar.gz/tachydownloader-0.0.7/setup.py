import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tachydownloader",
    version="0.0.7",
    author="Akshat Bisht",
    author_email="akshatbisht002@gmail.com",
    description="Tachyon — The faster than light media downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aaaakshat/tachyon",
    packages=setuptools.find_packages(),
    py_modules=['requests', 'click', 'tqdm'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': [
            'tachyon = tachyon:executeDownload',
        ],
    }
)
