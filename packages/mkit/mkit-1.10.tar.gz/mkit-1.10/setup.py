from setuptools import setup, find_packages

from mizlicai.mkit import version

setup(
    name="mkit",
    version=version(),
    keywords=("test", "xxx"),
    description="米庄理财小工具",
    long_description="米庄理财消息爬取和通知",
    license="MIT Licence",

    url="http://test.com",
    author="qinchao",
    author_email="qinchao@gmail.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[],

    scripts=[],
    entry_points={
        'console_scripts': [
            'mizlicai = mizlicai.mkit:main'
            'credit = kit.credit_pay:main'
        ]
    }
)