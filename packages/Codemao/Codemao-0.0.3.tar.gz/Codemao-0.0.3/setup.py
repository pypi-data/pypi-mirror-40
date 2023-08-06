from setuptools import setup, find_packages
setup(
    name="Codemao",
    version="0.0.3",
    packages=find_packages(),
    install_requires=['easygui','opencv-python','matplotlib','keras','dlib','tensorflow','pillow'],
    exclude_package_data = {
       'codemao': ['data'],
    }
)