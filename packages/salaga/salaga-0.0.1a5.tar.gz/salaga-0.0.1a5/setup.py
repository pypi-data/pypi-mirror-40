import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="salaga",
    version="0.0.1a5",
    author="Yashas ND",
    author_email="yashasbharadwaj111@gmail.com",
    description="Simple distributed key-value store",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yashasbharadwaj111/Salaga",
    packages=setuptools.find_packages(),
    install_requires=[
          'python-daemon',
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
