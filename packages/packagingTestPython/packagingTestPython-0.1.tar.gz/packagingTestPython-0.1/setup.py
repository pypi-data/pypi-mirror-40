from setuptools import setup, find_packages

setup(name='packagingTestPython',
      version='0.1',
      description='The funniest joke in the world',
      long_description='Really, the funniest around.',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      url='https://bitbucket.org/pervacio/wrdandroid/src/master/',
      author='Siva Ramavajjala',
      author_email='siva.ramavajjala@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'selenium',
      ],
      codeFiles=['drag-and-drop.py','mouse-hovering.py','slider.py'],
      include_package_data=True,
      zip_safe=False)