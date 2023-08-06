import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="turtle3D",
    version="0.1",
    author="Javiera Del Escoval",
    author_email="javieradelescoval@javiswebsites.ga",
    py_modules=["Turtle3D"],
    description="A pakage to draw 3D models with the python turtle",
    long_description="A pakage to draw 3D models with the python turtle, you can import .OBJ models and adjust X & Y position, colour, Y Rotation Angle and the size.",
    long_description_content_type="text/markdown",
    url="http://javiswebsites.ga",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
