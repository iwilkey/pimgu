from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pimgu',
    version='v05.04.2023.2',
    description='A simple framework for creating robust 2D GUI applications using Pygame and ImGui.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ian Wilkey',
    author_email='iwilkey@mail.bradley.edu',
    url='https://github.com/iwilkey/pimgu',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'PyOpenGL',
        'imgui',
        'numpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
)
