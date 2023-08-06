from setuptools import setup, find_packages

setup(
    name='Bert-Chatbot',
    version='',
    packages=find_packages(),
    url='https://github.com/ETCartman/Bert-Chatbot',
    license='MIT',
    author='Hanjun Liu',
    author_email='liuhanjun369@gmail.com',
    description='Use Google Bert to implement a chatbot with QA pairs and Reading comprehension!',
    install_requires=[
        'numpy',
        'pandas',
        'boto3',
    ],
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
)
