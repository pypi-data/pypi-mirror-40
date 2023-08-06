from setuptools import setup, find_packages
setup(
    name="Codemao",
    version="0.0.4",
    packages=find_packages(),
    install_requires=[
        'easygui',
        'opencv-python',
        'matplotlib',
        'keras',
        'dlib',
        'tensorflow'
        'pillow',
    ],
    exclude_package_data = {
       'codemao': ['data/*.hdf5',],
    },
    author="haiguibainjiqi",
    author_email="wood@codemao.cn",
    url="https://python.codemao.cn/"
)
