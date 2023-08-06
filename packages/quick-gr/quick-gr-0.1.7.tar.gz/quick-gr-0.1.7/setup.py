from setuptools import setup, find_packages
from quick_gr.command import normal_command

version = normal_command.Worker.version()

setup(
    name="quick-gr",
    version=version,
    keywords=("pip", "tool-gr", "partner", "quick-gr"),
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
            'visit = quick_gr.help:main'
        ]
    }
)
