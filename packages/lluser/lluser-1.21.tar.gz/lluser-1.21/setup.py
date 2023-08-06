from setuptools import setup
setup(
        name='lluser',
        version='1.21',
        author='oyy', 
        author_email='oyy284688@gmail.com', 
        url='http://dadadakeai.com/lluser/index.html',
        license='GUN',
        summary='记录登录',
        description='上次登录的用户，last login user',
        packages=['lluser'],
        install_requires=['requests>=2'],
        )
