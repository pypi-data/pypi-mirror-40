import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='Amzkill',  

     version='0.2',

     author="Amzker",
     scripts=['Amzkill'] ,
     author_email="amzker@protonmail.com",

     description="ARP Spoof/cut Unauthorized WiFi User",

     long_description='This Module use as Prevent Hacker/Unauthorized WIFI User . which my possible harm ',

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 2.7",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

 )
