from setuptools import setup, Extension

module1 = Extension('pynuklearc',
                    sources = ['contrib/nuklear/nuklearGLFWOpenGL3.c'],
                    include_dirs = ['/usr/include',
                                    'contrib/nuklear/'],
                    libraries = ['glfw'],
                    library_dirs = ['/usr/lib'],)

setup (name = 'pyNuklear',
       version = '0.0.6',
       description = 'Bindings to the nuklear immediate mode GUI library',
       author = 'William Emerison Six',
       author_email = 'billsix@gmail.com',
       url = 'https://github.com/billsix/pyNuklear',
       keywords = "nuklear imgui",
       license = "MIT",
       packages=['pynuklear',
                 'pynuklear/demo',
                 'pynuklear/demo/glfw_opengl3'],
       package_dir={'pynuklear': 'src/pynuklear',
                    'pynuklear/demo': 'src/pynuklear/demo/',
                    'pynuklear/demo/glfw_opengl3': 'src/pynuklear/demo/glfw_opengl3'},
       package_data={'pynuklear/demo/glfw_opengl3': ['triangle*'],
                     'contrib/nuklear/': ['gl3w.h'],
       },
       install_requires=[
           'glfw',
           'numpy',
           'pyMatrixStack',
           'PyOpenGL'],
       classifiers=[
           "Development Status :: 3 - Alpha",
           "Topic :: Utilities",
           "License :: OSI Approved :: MIT License",
       ],
       long_description = '''
Bindings to the nuklear immediate mode GUI library.  The only way to GUI.
''',
       ext_modules = [module1]
)
