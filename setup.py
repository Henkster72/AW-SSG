from setuptools import setup, find_packages

setup(
    name='aw_ssg',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'Jinja2',
        'python-dotenv',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'aw-ssg-init=scripts.init_project:main',
        ],
    },
)
