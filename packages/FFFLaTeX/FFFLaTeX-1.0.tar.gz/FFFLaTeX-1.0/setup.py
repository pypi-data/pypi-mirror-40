from setuptools import setup, find_packages


setup(name='FFFLaTeX', version='1.0', packages=find_packages(),
      install_requires=find_packages(),
      url='https://github.com/helldragger/FactorioFridayFactsLaTeX/releases',
    license='', author='Helldragger',
    entry_points={
            'console_scripts': [
                'FFFLaTeX = FFFLaTeX:main'
            ]
        },
    keywords="Factorio LaTeX",
    author_email='chritopher1223334444@gmail.com',
    description='Small scrapper script generating a basic LaTeX article from any FFF blog post. Includes images, videos and tables in the final pdf upon compilation. Compilation on windows will require to install wget on windows. ')

