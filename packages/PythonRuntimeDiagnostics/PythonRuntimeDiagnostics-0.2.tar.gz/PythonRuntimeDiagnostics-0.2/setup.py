from distutils.core import setup
setup(
  name = 'PythonRuntimeDiagnostics',       
  packages = ['PythonRuntimeDiagnostics'],   
  version = '0.2',     
  license='MIT',       
  description = 'This is a small utility to record the same data in cyclic applications',
  author = 'Daniel Racz',                   
  author_email = 'daniel.racz.93@gmail.com',
  url = 'https://github.com/dRacz3/PythonDiagnosticsLogger', 
  keywords = ['Logger', 'Diagnostics', 'Cyclic'], 
  install_requires=[            
          'pandas',
          'bokeh',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',  
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: System :: Logging',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)