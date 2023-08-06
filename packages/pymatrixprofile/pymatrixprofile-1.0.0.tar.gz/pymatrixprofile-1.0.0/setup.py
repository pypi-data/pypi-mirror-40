"""Setup pymatrixprofile as a package."""
import setuptools

setuptools.setup(
    name="pymatrixprofile",
    version="1.0.0",
    url="https://github.com/dawran6/cookiecutter-pypackage-minimal",

    author=" ",
    author_email=" ",

    description="My Awesome Package.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
)
