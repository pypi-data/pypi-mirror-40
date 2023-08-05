import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="maquinitas",
    version="0.0.1",
    author="Aarón Montoya-Moraga",
    author_email="montoyamoraga@gmail.com.com",
    description="Control of MIDI hardware devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maquinitas/maquinitas-foxdot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
