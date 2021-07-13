from distutils.core import setup

setup(
    name = 'bebackup',
    packages = ['bebackup'],
    version = '1.0',
    license='MIT',
    description = 'Cloud backup script with FTP',
    author = 'valouu',
    author_email = 'pro@valentingoulier.fr',
    url = 'https://github.com/valouugit/BeBackup',
    download_url = 'https://github.com/valouugit/BeBackup/archive/refs/tags/v1.0.tar.gz',
    keywords = ['FTP', 'CLOUD', 'BACKUP'],
    install_requires=[],
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.9',
    ],
)