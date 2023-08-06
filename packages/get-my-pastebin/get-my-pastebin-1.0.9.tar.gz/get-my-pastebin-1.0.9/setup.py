from setuptools import setup
setup(
  name = 'get-my-pastebin',
  py_modules=['get-my-pastebin'],
  version = '1.0.9',
  python_requires='>3.6',
  description = 'Terminal application to find and copy your own Paste for Pastebin.',
  author = 'Andros Fenollosa',
  author_email = 'andros@fenollosa.email',
  url = 'https://github.com/tanrax/get-my-pastebin',
  keywords = ['pastebin', 'terminal', 'console', 'copy', 'search', 'notes'],
  classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
  ),
  install_requires=[
      'Click>=7.0',
      'pick>=0.6.4'
  ],
  entry_points='''
      [console_scripts]
      getmypastebin=get_my_pastebin:main
  '''
)
