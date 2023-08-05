from setuptools import setup, find_packages

setup(
    name='memcache_lock',
    version='0.0.2',
    description='Locking mechanism for Python 2.7 GAE, using memcache',
    url='https://github.com/linuxpi/memcache_lock',
    author='Varun Bansal',
    author_email='varunb94@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2'
    )
)