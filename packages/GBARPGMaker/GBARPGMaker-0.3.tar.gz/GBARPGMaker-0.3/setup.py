import setuptools

setuptools.setup(
    name="GBARPGMaker",
    version="0.3",
    description="A small example package",
    packages=setuptools.find_packages(),
    url="https://gitlab.com/kockahonza/gbarpgmaker",
    package_data={'': ['*.c', '*.h']},
    include_package_data=True,
)
