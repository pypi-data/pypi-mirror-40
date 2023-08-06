import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyUDX",
    version="0.0.5",
    author="Unidex",
    author_email="dev@unidex.online",
    url='https://unidex.online',
    license='MIT',
    description="Object-oriented library for the Unidex blockchain platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords = ['unidex', 'blockchain', 'analytics'],
    packages=['pyudx'],
    install_requires=[
	    'base58==0.2.5',
        'pyblake2',
        'python-axolotl-curve25519',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)