from setuptools import setup

setup(
    name='receipt-reader',
    version='0.1',
    packages=[''],
    install_requires=[
        'Flask',
        'craft_text_detector',
        'transformers'
    ],
    url='',
    license='GPLv3',
    author='Diego Renedo Delgado',
    author_email='',
    description='Receipt reader using CRAFT (Character Region Awareness for Text Detection) '
                'and TrOCR (Transformer-based Optical Character Recognition)'
)
