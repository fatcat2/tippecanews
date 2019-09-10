from setuptools import find_packages, setup

setup(
    name='Tippecanews',
    version='1.0.0',
    url='http://flask.pocoo.org/docs/tutorial/',
    description='The basic blog app built in the Flask tutorial.',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
