import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='yikai-tools',
    version='1.0.1',
    description='python modules.',
    long_description=long_description,
    url='https://github.com/happyshi0402/yikai_tools.git',
        
    author='Wang Shifeng',
    author_email='wsf121116@163.com',
    license='MIT',

    install_requires=["pytz"
    ],

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=setuptools.find_packages(),
    
)
