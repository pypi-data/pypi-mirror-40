from setuptools import setup

setup(name='predicts',
      version='0.3',
      description='Predicting Titanic Survivor',
      url='https://github.com/abbiyanaila/predicts',
      author='Desi Ratna Ningsih',
      author_email='abbiyanaila@gmail.com',
      license='MIT',
      packages=['predicts'],
      install_requires=[
            'joblib',
            'scikit-learn'
      ],
      zip_safe=False)


