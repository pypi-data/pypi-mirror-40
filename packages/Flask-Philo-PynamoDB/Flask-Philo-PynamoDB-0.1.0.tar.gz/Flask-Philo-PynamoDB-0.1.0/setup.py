from setuptools import setup


long_description = """
Flask-Philo extension that provides Integration with PynamoDB
"""


setup(
    name='Flask-Philo-PynamoDB',
    version='0.1.0',
    description='Flask-Philo plugin that provides support for PynamoDB',
    long_description=long_description,
    packages=[
        'flask_philo_pynamodb'

    ],
    url='https://github.com/Riffstation/Flask-Philo-PynamoDB',
    author='Manuel Ignacio Franco Galeano',
    author_email='maigfrga@gmail.com',
    license='Apache',
    install_requires=[
        'Flask-Philo-Core',
        'pynamodb'

    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Framework :: Flask',
        'Programming Language :: Python :: 3',
    ],
    keywords='FLASK AWS DynamoDB',

)
