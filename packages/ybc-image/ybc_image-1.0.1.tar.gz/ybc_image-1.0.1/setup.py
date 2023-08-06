#!/usr/bin/env python

from distutils.core import setup

setup(
  name='ybc_image',
  version='1.0.1',
  description='Synthetic expression pack',
  long_description='Synthetic expression pack',
  author='zhangyun',
  author_email='zhangyun@fenbi.com',
  keywords=['pip3', 'python3', 'python', 'Synthetic expression pack'],
  url='http://pip.zhenguanyu.com/',
  packages=['ybc_image'],
  package_data={'ybc_image': ['*.py', 'NotoSansCJK-Bold.ttc', 'test.jpg']},
  license='MIT',
  install_requires=['pillow', 'ybc_exception']
)
