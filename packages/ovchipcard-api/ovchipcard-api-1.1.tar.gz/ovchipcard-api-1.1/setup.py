from distutils.core import setup

setup(
    name='ovchipcard-api',
    version='1.1',
    description='OV Chipkaart API',
    author='Hylco Uding',
    author_email='chipchop@protonmail.com',
    packages=['ovchipcard'],
    install_requires=[
        "requests",
    ],
    url='https://github.com/OVChip/ovchipapi-python',
    download_url='https://github.com/OVChip/ovchipapi-python/tarball/0.1',
    keywords=["OV", "Public Transport", "ov-chipkaart", "chipkaart"]
)
