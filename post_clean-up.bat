cd %~dp0

cd lib
del _hashlib.pyd
del _elementtree.pyd
del _decimal.pyd
del _lzma.pyd
del _queue.pyd
del _ssl.pyd
del _uuid.pyd
del libcrypto-1_1.dll
del libssl-1_1.dll

cd ..
del python3.dll
del vcruntime140.dll
del post_clean-up.bat