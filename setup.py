from setuptools import setup

setup(
    name='knn_anomaly_detector',
    version='0.1.0',
    packages=['knn_anomaly_detector'],
    url='https://dynamite.ai',
    license='',
    author='Dynamite Analytics',
    author_email='jamin@dynamite.ai',
    description='Detect anomalies in events using K-Nearest-Neighbor',
    install_requires=[
        'dynamite_analyzer_framework',
        'pyod',
    ],
)
