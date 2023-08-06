import setuptools

with open('README.md', 'r') as handle:
    long_description = handle.read()

setuptools.setup(
    name='playmafia',
    version='0.0.1',
    author='Nicolas Kogler',
    author_email='nicolas.kogler@hotmail.com',
    description='The SDK for playmafia',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/v7a/playmafia',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
