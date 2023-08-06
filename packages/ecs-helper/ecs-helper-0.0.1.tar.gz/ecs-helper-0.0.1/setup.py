from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='ecs-helper',
    version='0.0.1',
    description='Scriptable tool for managing ECS deployments',
    long_description=README,
    long_description_content_type="text/markdown",

    url='https://github.com/fibertide/ecs-helper',
    author='Fibertide',
    author_email='team@fibertide.com',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
    ],
    keywords='aws ecs cli',

    python_requires='>=3.6',
    install_requires=[],

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ecs-helper = ecshelper.main:main',
        ],
    },
)
