from setuptools import setup, find_packages

setup(name='rlagent',
      version='0.1.3',
      description='rlagent: Reinforcement learning framework in tensorflow, compatible with OpenAI Gym like environments.',
      url='https://github.com/YunjaeChoi/rlagent',
      author='Yunjae Choi',
      author_email='yunjae.choi1000@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          'numpy>=1.14.0', 'tensorflow>=1.10.1', 'gym>=0.10.3', 'pybullet>=1.9.7',
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
)
