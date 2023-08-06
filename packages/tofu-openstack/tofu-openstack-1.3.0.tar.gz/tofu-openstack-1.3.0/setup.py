from setuptools import setup

# pip install -e ./  # requires the following
# pip install setuptools wheel

setup(name='tofu-openstack',
      version='v1.3.0',
      description="A terraform openstack dynamic inventory for ansible",
      url='https://github.com/shalomb/tofu',
      author='Shalom Bhooshi',
      author_email='s.bhooshi@gmail.com',
      license='Apache License 2.0',
      packages=['tofu'],
      zip_safe=False,
      scripts=['tofu/tofu.py'],
      install_requires=[
        'pyyaml'
      ],
    )
