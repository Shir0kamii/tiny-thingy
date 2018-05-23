from setuptools import setup


setup(
    name="Tiny-Thingy",
    version="0.2.0",
    url="https://github.com/Shir0kamii/tiny-thingy",
    license="MIT",
    author="Shir0kamii",
    description="JSON database with python object notation",
    long_description=None,
    py_modules=["tiny_thingy"],
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=[
        "thingy>=0.8.3",
        "tinydb>=3.9.0"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
