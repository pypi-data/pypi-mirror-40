from setuptools import setup


with open('README.md', 'r') as fl:
    long_desc = fl.read()


setup(
    name="bottlecors",
    author="Arjoonn Sharma",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    version="0.34",
    packages=["bottlecors"],
    install_requires=["bottle"],
    python_requires=">=3.6",
    project_urls={"Source": "https://github.com/thesage21/bottlecors"},
    zip_safe=False,
)
