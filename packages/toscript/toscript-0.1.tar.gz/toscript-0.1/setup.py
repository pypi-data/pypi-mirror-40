from setuptools import setup

setup(
    name='toscript',
    version='0.1',
    description='Helps with setting up envs quickly',
    url='https://github.com/tklijnsma/toscript.git',
    download_url='https://github.com/tklijnsma/toscript/archive/v0.tar.gz',
    author='Thomas Klijnsma',
    author_email='thomasklijnsma@gmail.com',
    packages=['toscript'],
    zip_safe=False,
    scripts=[
        'bin/toscript-python',
        ],
    )

print 'Add the following lines to your .bashrc'
print '[ -f /Users/thomas/packages/toscript/completion.py ] && complete -C /Users/thomas/packages/toscript/completion.py to'
print 'alias to=". /Users/thomas/packages/toscript/to.sh"'
