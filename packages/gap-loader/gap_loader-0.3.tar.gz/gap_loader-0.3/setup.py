from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='gap_loader',
    version='0.3',
    description='Import hook for GAP files in SAGE math.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    url='http://github.com/jorants/gap-loader',
    author='Joran van Apeldoorn (Control-K)',
    author_email='jorants@gmail.com',
    license='MIT',
    packages=['gap_loader'],
    install_requires=[
        'sage',
    ],
    zip_safe=False)
