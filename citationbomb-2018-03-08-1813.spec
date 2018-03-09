# -*- mode: python -*-

block_cipher = None


a = Analysis(['citationbomb-2018-03-08-1813.py'],
             pathex=['/Users/skeptic/Documents/citations'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='citationbomb-2018-03-08-1813',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='citationbomb-2018-03-08-1813')
app = BUNDLE(coll,
             name='citationbomb-2018-03-08-1813.app',
             icon=None,
             bundle_identifier=None)
