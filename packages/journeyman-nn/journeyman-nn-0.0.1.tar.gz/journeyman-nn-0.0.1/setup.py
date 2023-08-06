from setuptools import setup, find_packages


REQUIREMENTS = [
    'keras==2.2.4',
    'tensorflow==1.12.0',
    'scikit-learn==0.20.2',
]

setup(
    name='journeyman-nn',
    version='0.0.1',
    description='Character-level bidirectional recurrent neural network for short sentences categorization',
    url='https://github.com/bureaucratic-labs/journeyman',
    author='Bureaucratic Labs',
    author_email='hello@b-labs.pro',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='natural language processing',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
)
