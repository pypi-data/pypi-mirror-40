from setuptools import setup

with open("README.md", "r" ,encoding='UTF-8') as fh:
    long_description = fh.read()

setup(
    name='BaiduFace',
    version='1.3',
    package_dir={'bdface': 'src'},
    packages=['bdface'],
    author='wcy',
    author_email='1208640961@qq.com',
    description='Call baidu face recognition recommendation system',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
