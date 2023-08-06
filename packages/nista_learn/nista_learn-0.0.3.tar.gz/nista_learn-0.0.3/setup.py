import setuptools

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setuptools.setup(
    name="nista_learn",
    version="0.0.3",
    author="Cheikh Tidjane Konteye",
    author_email="cheikh@cheikhkonteye.com",
    description="A small machine learning package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wariored/nista_learn",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
