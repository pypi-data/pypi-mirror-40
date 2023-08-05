from setuptools import setup
version = "0.0.13"
setup(name='planblick',
      version=version,
      description='',
      url='https://www.planblick.com',
      author='Florian Kröber @ Planblick',
      author_email='fk@planblick.com',
      license='MIT',
      packages=['planblick.httpserver', 'planblick.autorun'],
      install_requires=[
          'cherrypy',
          'requests'
      ],
      zip_safe=False)
