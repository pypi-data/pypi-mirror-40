import setuptools

setuptools.setup(
    name="algo_db_controller",
    version="0.0.1",
    author="Afzal SH @ Tarams",
    author_email="afzal.hameed@tarams.com",
    description="Handles everything db related for algo",
    packages=setuptools.find_packages(),
    install_requires=[
        'psycopg2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
