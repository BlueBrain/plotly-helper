#!/usr/bin/env python


from setuptools import find_packages, setup

setup(
    name="plotly-helper",
    author="Blue Brain Project, EPFL",
    description="Package that makes plotly easy",
    url="https://github.com/bluebrain/plotly-helper",
    license="LGPLv3",
    install_requires=[
        'plotly>=3.4.2',
        'numpy>=1.15.4',
        # TODO replace it with 'neurom>=3.0.0', when 3.0.0 is released
        'neurom @ git+https://git@github.com/BlueBrain/neurom.git@3.0.0#egg=neurom',
        'click>=6.0',
    ],
    extras_require={
        'docs': ['sphinx', 'sphinx-bluebrain-theme'],
    },
    entry_points={
        'console_scripts': ['viewer=plotly_helper.cli:cli']
    },
    python_requires='>=3.6',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
)
