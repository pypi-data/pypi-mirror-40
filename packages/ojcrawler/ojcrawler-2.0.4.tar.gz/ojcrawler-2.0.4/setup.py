from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ojcrawler',
    version='2.0.4',
    packages=find_packages(),
    url='https://github.com/LETTersOnline/ojcrawler',
    license='MIT',
    author='crazyX',
    author_email='xu_jingwei@outlook.com',
    description='crawler of some online judge system',
    long_description=long_description,
    install_requires=['psutil', 'requests', 'robobrowser', 'beautifulsoup4', 'html5lib'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
