import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dep2pict-gui',
    version='0.7.0',
    packages=setuptools.find_packages(),
    license='LICENSE/Licence_CeCILL_V2-en.txt',
    description="A Qt interface for the dep2pict software",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://dep2pict.loria.fr",
    author="bguil",
    author_email="Bruno.Guillaume@loria.fr",
    install_requires=[
        'PyQt5',
        'json2html',
    ],
    entry_points={
        'gui_scripts': [
            'dep2pict-gui = src.dep2pict:main',
        ],
    }

)
