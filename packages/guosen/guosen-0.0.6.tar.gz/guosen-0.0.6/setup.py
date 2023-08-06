import setuptools

setuptools.setup(
    name='guosen',
    version="0.0.6",
    author="zhangkai",
    author_email='474918208@qq.com',
    license='MIT',
    # url='www.worldprice.cn',
    description='A framework for developing Quantitative Trading programmes',
    long_description=__doc__,
    keywords='quant quantitative investment trading algotrading',
    classifiers=["Operating System :: OS Independent",
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Office/Business :: Financial :: Investment',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'License :: OSI Approved :: MIT License'],
    packages=setuptools.find_packages(),
)
