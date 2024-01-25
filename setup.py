from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'keyboard==0.13.5',
    'loguru==0.7.2',
    'matplotlib==3.8.2',
    'PyAutoGUI==0.9.54',
    'pyserial==3.5',
    'pystray==0.19.5',
    'pyTelegramBotAPI==4.15.2',
    'python-dotenv==1.0.1',
    'opencv-python==4.9.0.80'
    
]

setup(
    name="dota2_arduino",
    version="0.0.1",
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES
)
