import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Dosie",
    version="0.0.1",
    author="Eliezer Odjao",
    author_email="eliezerodjaoofficial@gmail.com",
    description="A search engine that makes knowledge a resource, and creates liberation with information sharing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://eliezerodjao.com/desktop/portfolio.php?sent=dosie",
    license="Proprietary",
    packages=setuptools.find_packages(),
    include_package_data=True,
    keywords='search searchEngine information web internet data',
    install_requires=['Synx','Pillow'],
    python_requires='~=3.3',
    classifiers=[
        "Environment :: Win32 (MS Windows)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Topic :: Communications",
        "Topic :: Education",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search"
    ],
    project_urls={
    'Documentation': 'https://eliezerodjao.com/docs/Dosie_User_Documentation.docx',
    'Source': 'https://eliezerodjao.com/desktop/portfolio.php?sent=dosie'
    },
)
