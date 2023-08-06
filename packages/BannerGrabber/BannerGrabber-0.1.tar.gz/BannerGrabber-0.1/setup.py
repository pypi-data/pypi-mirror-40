from distutils.core import setup
setup(
  name = 'BannerGrabber',
  packages = ['BannerGrabber'],   
  version = '0.1',     
  license='MIT',        
  description = ' Simple python project that use sockets to get banner from services and check on local database if services are vulnerable ',   
  author = 'Bardh Krasniqi',                   
  author_email = 'bardh.krasniqi11@gmail.com',      
  url = 'https://github.com/bardhkrasniqi',   
  download_url = 'https://github.com/bardhkrasniqi/BannerGrabber/archive/v_01.tar.gz',    
  keywords = ['Python', 'BannerGrabber'],   
  install_requires=[
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      

    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   # Again, pick a license

    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
