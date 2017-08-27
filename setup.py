from setuptools import setup, find_packages

setup(
    name="ScreenshotSSH",
    version="0.9",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'screenshotssh = screenshotssh.cli:upload'
        ]
    },
    
    install_requires=['click>=6.0', 'paramiko>=2.2', 'pyperclip>=1.5'],

    author="Aldehir Rojas",
    author_email="hello@aldehir.com",
    description="Transfer screenshots via SSH/SFTP, rename, and copy to cliboard",
    license="MIT",
    keywords="screenshot ssh clipboard",
    url="http://github.com/aldehir/screenshotssh"
)
