import setuptools


setuptools.setup(
    name="webutils-wechat",
    version="0.0.3",
    author="SimonQ",
    author_email="simonq.mq@gmail.com",
    description="Simple utils for Restful-web-wechat",
    long_description="Simple utils for Restful-web-wechat",
    long_description_content_type="text/markdown",
    url="https://gitee.com/xxmeng/webutils-wechat",
    packages=setuptools.find_packages(),
    install_requires=[
        'flask==1.0.2',
        'flask_restplus==0.12.1',
        'requests==2.21.0',
        'redis==2.10.6',
        'msgpack==0.5.6',
        'cryptography==2.3.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
