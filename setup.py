import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cbsencrypt",
    version="0.0.2",
    author="Conor J. Wild",
    author_email="conor.wild@cambridgebrainsciences.com",
    description="A library of for generating keys, encrypting and uncrypting files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="TBD",
    packages=['cbsencrypt'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'cryptography', 'argparse'
    ],
    entry_points={
        'console_scripts': [
            'cbs_encrypt=cbsencrypt.cbsencrypt:encrypt_files_cmdline',
            'cbs_decrypt=cbsencrypt.cbsencrypt:decrypt_files_cmdline',
            'cbs_genkey=cbsencrypt.generate_passkey:main',
        ]
    }
)
