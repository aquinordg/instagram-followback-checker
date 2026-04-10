from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="instagram-followback-checker",
    version="1.0.0",
    author="Seu Nome",
    author_email="seu@email.com",
    description="Check who doesn't follow you back on Instagram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SEU_USUARIO/instagram-followback-checker",
    py_modules=["instagram_followback"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "instaloader>=4.10",
    ],
    entry_points={
        "console_scripts": [
            "instagram-followback=instagram_followback:main",
        ],
    },
)