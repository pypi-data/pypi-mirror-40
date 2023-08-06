from setuptools import find_packages, setup


print(find_packages())
setup(name='FFFLaTeX', version='1.5', packages=[
    "FFFLaTeX"],
      install_requires=[
    "beautifulsoup4", "urllib3", "html5lib"],
      url='https://github.com/helldragger/FactorioFridayFactsLaTeX',
      license='lGPL v3', author='Helldragger',
      entry_points={
            'console_scripts': [
                'FFFLaTeX = FFFLaTeX:main'
            ]
        },
      keywords="Factorio LaTeX",
      author_email='chritopher1223334444@gmail.com',
      description='Small scrapper script generating a basic LaTeX article from any FFF blog post. Includes images, videos and tables in the final pdf upon compilation. Compilation on windows will require to install wget on windows. ')

