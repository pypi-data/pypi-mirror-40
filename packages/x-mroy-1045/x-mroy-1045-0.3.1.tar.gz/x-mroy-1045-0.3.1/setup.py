from setuptools import setup, find_packages


setup(name='x-mroy-1045',
    version='0.3.1',
    description='a anayzer package',
    url='https://github.com/Qingluan/.git',
    author='Qing luan',
    author_email='darkhackdevil@gmail.com',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=['mroylib-min','async_timeout','aiofiles','aioredis','aiosocks==0.2.6','aiohttp==2.3.10'],
    entry_points={
        'console_scripts': ['m-async=asynctools.servers:start_socket_service', 'm-asyncs=asynctools.servers:run_local_async']
    },

)
