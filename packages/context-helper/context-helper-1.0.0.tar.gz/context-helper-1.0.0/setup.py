import io

from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='context-helper',
    version='1.0.0',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    author='Robert Parker',
    author_email='rob@parob.com',
    url = 'https://gitlab.com/gloopio/context-helper',
    download_url = 'https://gitlab.com/gloopio/context-helper/-/archive/v1.0.0/context-helper-v1.0.0.tar.gz',
    keywords = ['Context', 'Helper'],
    description='Context helpers for Python.',
    long_description=readme,
    install_requires=[
        "werkzeug>=0.13"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
