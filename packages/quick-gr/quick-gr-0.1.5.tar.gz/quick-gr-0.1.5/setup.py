from setuptools import setup, find_packages

setup(
    name="quick-gr",
    version="0.1.5",
    keywords=("pip",  "tool-gr", "partner", "quick-gr"),
    description="tool-gr",
    long_description="make api doc quickly by python script",
    license="MIT Licence",

    url="http://sealbaby.cn",
    author="partner",
    author_email="partnerhanxiao_i@didiglobal.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['requests'],

    scripts=[],
    entry_points={
        'console_scripts': [
            'visit = visit.help:main'
        ]
    }
)
