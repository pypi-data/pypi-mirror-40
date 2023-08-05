from setuptools import setup, find_packages

setup(
    name="ads_api",
    version="0.1.7.4",
    description="major marketing platform python api",
    packages=find_packages(),
    install_requires=[
        'pandas==0.23.4',
        'matplotlib==2.1.2',
        'bingads==11.5.8',
        'googleads==14.1.0',
        'SQLAlchemy==1.2.3',
        'psycopg2==2.7.4',
        'azure-storage==0.36.0'
    ]
)
