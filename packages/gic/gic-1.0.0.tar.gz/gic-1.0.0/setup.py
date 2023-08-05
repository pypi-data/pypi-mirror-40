import setuptools

setuptools.setup(
        name="gic",
        version="1.0.0",
        description="Group Image Compressor (GIC)",
        long_description="An image compressor that compresses all images in the working directory.",
        long_description_content_type="text/markdown",
        url="https://github.com/poyynt",
        author="Parsa Torbati",
        author_email="parsa@programmer.net",
        packages=setuptools.find_packages(),
        python_requires=">=3.2",
        install_requires=[
            "python-opencv",
            "tkinter",
            ],
        entry_points={
            "console_scripts": [
                "gic=gic.main:run",
                ],
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Operating System :: OS Independent",
            ],
        )
