'''
used to compile the .c module
once run this command, a build is produced in the build folder and a module is created in the root folder. 
this module must be imported as a python module using "import moduleName" where moduleName is the part before the dot. 
in this case would be "hello" => "import hello"
'''


from distutils.core import setup, Extension
import sys 

module = Extension('hello',
                    sources=['lib/PythonC/hello_world.c'])

if __name__ == "__main__":
    sys.argv += ["build_ext", "--inplace"]  # Aggiunge i comandi alla lista argv


setup(name='HelloWorld',
      version='1.0',
      description='Python Package with Hello, World in C',
      ext_modules=[module])

