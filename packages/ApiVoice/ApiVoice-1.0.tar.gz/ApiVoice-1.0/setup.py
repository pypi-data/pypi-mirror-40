from setuptools import setup,find_packages

setup(
    name="ApiVoice",
    version="1.0",
    description="apiApeech sdk",
    long_description=open('README.md').read(),
    license="MIT Licence",
    author="Lucas",
    author_email="767402013@qq.com",
    platforms=["all"],
    packages=find_packages(),
    url="https://github.com/fengxiaoyii/ApiSpeech.git",
    install_requires=[
        "baidu-aip>=2.2.11.0"
    ],
    classifiers=[
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries'
        ],
    zip_safe=False
)