from distutils.core import setup
setup(
  name = 'matialvarezs_handlers_easy',
  packages = ['matialvarezs_handlers_easy'], # this must be the same as the name above
  version = '0.1.16',
  install_requires = [
    'django-json-response==1.1.3',
    'celery==4.1.0',
    'django-celery-results==1.0.1'
  ],
  include_package_data = True,
  description = 'Easy handler',
  author = 'Matias Alvarez Sabate',
  author_email = 'matialvarezs@gmail.com',
  classifiers = [
    'Programming Language :: Python :: 3.5',
  ],
)