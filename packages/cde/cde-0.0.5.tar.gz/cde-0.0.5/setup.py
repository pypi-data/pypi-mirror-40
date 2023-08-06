from setuptools import setup


setup(name='cde',
      version='0.0.5',
      description='Framework for conditional density estimation',
      url='https://jonasrothfuss.github.io/Nonparametric_Density_Estimation',
      author='Jonas Rothfuss, Fabio Ferreira',
      author_email='jonas.rothfuss@gmx.de, fabioferreira@mailbox.org',
      license='MIT',
      packages=['cde'],
      install_requires=[
        'Keras',
        'numpy',
        'pandas',
        'tensorflow',
        'matplotlib',
        'edward',
        'seaborn',
        'scipy',
        'pytest',
        'scikit_learn',
        'statsmodels',
        'pypmc',
      ],
      zip_safe=False)
