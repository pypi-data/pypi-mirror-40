from setuptools import setup

setup(
    name="x256_img",
    author="Jacob Jäger",
    maintainer="Jacob Jäger",
    version="0.0.1",
    description="Display pictures in a terminal using x256 color codes",
    py_modules=['x256_img'],
    install_requires=["x256", "pillow"],
    entry_points={
        'console_scripts': [
            "x256-img=x256_img:_cli_init"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ]
)
