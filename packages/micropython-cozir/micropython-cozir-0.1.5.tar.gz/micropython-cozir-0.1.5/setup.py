import pathlib
from setuptools import setup

CWD = pathlib.Path(__file__).parent
README = (CWD / "README.md").read_text()


setup(
    name="micropython-cozir",
    version="0.1.5",
    author="Dmitry Larkin",
    author_email="dmitry.larkin@gmail.com",
    maintainer="Dmitry Larkin",
    maintainer_email="dmitry.larkin@gmail.com",
    description="COZIR CO2 Sensor Library",
    keywords='COZIR CO2 Sensor micropython',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dml/micropython-cozir",
    py_modules=["cozir"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: MIT License",
    ],
)
