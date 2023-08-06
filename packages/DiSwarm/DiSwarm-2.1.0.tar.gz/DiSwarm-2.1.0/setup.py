import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DiSwarm",
    version="2.1.0",
    author="iTecX",
    author_email="matteovh@gmail.com",
    description="Discord-based Swarm Protocol Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iTecAI/DiSwarm",
    py_modules=['keydet'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['discord','cryptography'],
    include_package_data = True,
    package_data={'keydet': ['*.pyc']},
)
