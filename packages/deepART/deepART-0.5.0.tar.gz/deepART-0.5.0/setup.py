from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
        name='deepART',
        version='0.5.0',
        description='A library for family of adaptive resonance theory neural networks',
        url='',
        author='Chun Ping Lim',
        author_email='chunplim@deloitte.com',
        license='MIT',
        packages=find_packages(exclude=['*.tests']),
        install_requires=[
            'numpy==1.15.1',
            'joblib==0.13.0',
            'nltk==3.4'
        ],
        include_package_data=True,
        test_suite='nose.collector',
        tests_require=['nose'],
        zip_safe=False,
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    )