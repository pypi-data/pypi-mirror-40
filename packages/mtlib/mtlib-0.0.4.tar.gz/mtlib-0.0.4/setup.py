import setuptools

setuptools.setup(
    name='mtlib',
    version='0.0.4',
    packages=['mtlib',],
    license='MIT License',
    author="Eric Wilkison",
    author_email="ericw@wilkison.com",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/ericwilkison/mtlib',
    install_requires=[
            "aiocoap == 0.4a1",
            "zeroconf >= 0.21.3"
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
