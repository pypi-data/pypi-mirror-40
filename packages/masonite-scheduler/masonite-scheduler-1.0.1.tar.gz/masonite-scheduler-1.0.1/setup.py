from setuptools import setup

setup(
    name="masonite-scheduler",
    version='1.0.1',
    packages=[
        'scheduler',
        'scheduler.commands',
        'scheduler.providers'
    ],
    install_requires=[],
    include_package_data=True,
)
