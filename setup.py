from setuptools import setup, find_packages

setup(
    name='pyshould',
    version='0.1.0',
    url='',
    author='Iván -DrSlump- Montes',
    author_email='drslump@pollinimini.net',
    packages = find_packages(),
    include_package_data = True,
    install_requires=['pyhamcrest'],
    zip_safe = False,
    )