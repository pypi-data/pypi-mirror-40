from distutils.core import setup

# also update in urlnorm.py
version = '1.1.2.5'

setup(name='Sweepatic-urlnorm',
        version=version,
        long_description=open("./README.txt", "r").read(),
        description="Normalize a URL to a standard unicode encoding",
        py_modules=['urlnorm'],
        license='MIT License',
        install_requires=['six'],
        author='Jehiah Czebotar',
        author_email='jehiah@gmail.com',
        url='http://github.com/jehiah/urlnorm',
        download_url="http://github.com/downloads/jehiah/urlnorm/urlnorm-%s.tar.gz" % version,
        classifiers=[
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
        ],
        )
