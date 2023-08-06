import setuptools

requirements = [
    'ruamel.yaml',
    'click',
]


setuptools.setup(
    name="llps",
    version="0.4.0",
    url="https://github.com/LongTailBio/large_project_specification",
    author="David C. Danko",
    author_email="dev@longtailbio.com",
    description="A simple specification for large bioinformatics projects.",
    packages=setuptools.find_packages(),
    package_dir={'llps': 'llps'},
    entry_points={
        'console_scripts': [
            'llps=llps.cli:main',
        ]
    },
    install_requires=requirements,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
