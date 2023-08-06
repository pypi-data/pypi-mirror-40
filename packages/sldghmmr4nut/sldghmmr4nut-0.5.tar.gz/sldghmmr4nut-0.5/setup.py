from setuptools import setup, find_packages
setup(
      name="sldghmmr4nut",
      version = "0.5",
      description="txt-spliter wrap of numpy to handle txt",
      author="dapeli",
      url="https://github.com/ihgazni2/sldghmmr4nut",
      author_email='terryinzaghi@163.com', 
      license="MIT",
      long_description = "refer to .md files in https://github.com/ihgazni2/sldghmmr4nut",
      classifiers=[
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Programming Language :: Python',
          ],
      packages= find_packages(),
      py_modules=['sldghmmr4nut'], 
      )


# python3 setup.py bdist --formats=tar
# python3 setup.py sdist

