import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

top_level_typed_packages = {k: ['py.typed'] for k in set([k.split(".", 1)[0] for k in setuptools.find_packages()])}

setuptools.setup(
    name="telegram-envelope",
    version="0.1.3",
    author="Dani Sancas",
    author_email="lord.sancas@gmail.com",
    description="Micro-helper for AWS Telegram Bots written in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DaniSancas/telegram-envelope",
    package_data=top_level_typed_packages,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
