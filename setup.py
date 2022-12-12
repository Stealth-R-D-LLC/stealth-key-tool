from setuptools import setup

setup(
  name="stealth-key-tool",
  version="0.1.0",
  author="James Stroud",
  author_email="stealthsend@stealth-coin.com",
  packages=["stealth_key_tool",
            "stealth_key_tool.bip32utils",
            "stealth_key_tool.pbkdf2"],
  scripts=["bin/stealth-key-tool.py", "bin/bip32gen"],
  url="https://github.com/Stealth-R-D-LLC/stealth-key-tool",
  description="A simplified wrapper for working with HD wallets",
  long_description=open('README.md').read(),
  install_requires=[])
