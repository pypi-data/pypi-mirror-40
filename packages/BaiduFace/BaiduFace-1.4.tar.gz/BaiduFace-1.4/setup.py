from setuptools import setup

with open("README.md", "r" ,encoding='UTF-8') as fh:
    long_description = fh.read()

setup(
    name='BaiduFace',
    version='1.4',
    package_dir={'bdface': 'src'},
    packages=['bdface'],
    author='wcy',
    author_email='1208640961@qq.com',
    description='调用百度人脸识别推荐系统',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
