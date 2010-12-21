from setuptools import setup, find_packages

setup(
        name='flights-notifier',
        version='0.0.0',
        author='Karen Chan',
        author_email='cee.wing@gmail.com',
        description='A script to email you status of your flights',
        license='BSD',
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'flights-notifier = travel.scripts.notifier:main',
                ],
            },
        )
