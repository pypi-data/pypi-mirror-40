from distutils.core import setup

import setuptools


setup(
    name='dnslookup',
    version='0.7.31',
    author='Joubin Jabbari',
    author_email='joubin.j@gmail.com',
    url="https://github.com/joubin/DNSPython",
    license='LICENSE.txt',
      entry_points={
          'console_scripts':
              ['dnslookup= dnslookup.main:main']},
    description='Check dns entries across the world. In short, if you move your server from one IP to another, you can check to see when most of the dns servers in the world have update their results.',
    long_description="""### DNSPython 

DNSPython is a simple command line interface to check on the status of your world wide resolutions. 

##### Installation:
<pre>
pip install dnspython-lookup
</pre>
##### Usage:

<pre>
dnspython-lookup facebook.com
Result for facebook.com
Country 	DNS IP 		Result
BD 	203.112.202.195 	 173.252.110.27
BE 	   195.35.110.4 	 173.252.110.27
BG 	  213.169.55.10 	 173.252.110.27
BM 	   206.53.177.3 	 173.252.110.27
BO 	  200.58.161.25 	 173.252.110.27
JP 	221.186.252.130 	 173.252.110.27
JM 	    200.9.115.2 	 173.252.110.27
</pre>

<pre>
dnspython-lookup --help
usage: main.py [-h] [--level LEVEL] [--file FILE] domain

positional arguments:
  domain                The domain that you would like to use.

optional arguments:
  -h, --help            show this help message and exit
  --level LEVEL, -l LEVEL
                        This option allows you to: (1) use a large database of
                        DNS Servers. (2) Use just the google DNS Servers. (3)
                        Use your own server list. <Requires properly formatted
                        file>
  --file FILE           Name of the file to use with option (3) of level
</pre>


Please let me know if there are other features you'd like
""",
    long_description_content_type="text/markdown",
    packages=['dnslookup'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], install_requires=['future']
)
