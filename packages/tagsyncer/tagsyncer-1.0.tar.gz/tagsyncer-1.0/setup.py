from setuptools import setup

setup(name='tagsyncer',
      version='1.0',
      description='Command line tool that syncs up ec2 instance tags with its ASG tags ',
      url='https://github.com/SManral/tagsyncer.git',
      author='Smriti Manral',
      entry_points = {
        'console_scripts': ['tagsyncer=tagsyncer.tag_syncer:main']
      },
      author_email='smriti.manral@gmail.com',
      license='MIT',
      packages=['tagsyncer'],
      install_requires = ['boto3 >= 1.9.75', 'logging >= 0.4.9.6'],
      zip_safe=False)
