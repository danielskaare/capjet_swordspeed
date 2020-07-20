# -*- mode: python -*-

block_cipher = None


a = Analysis(['Capjet Data Extractor.py'],
             pathex=['C:\\Users\\dags\\PycharmProjects\\capjet_swordspeed'],
             binaries=[],
             datas=[('Config_Main_Setup.ini', '.'), ('Instructions_v0.91.pdf', '.'), ('dependencies/mkl_vml_def.dll', '.'), ('dependencies/libiomp5md.dll', '.')],
             hiddenimports=['pandas._libs.tslibs.timedeltas', 'pandas._libs.tslibs.nattype', 'pandas._libs.tslibs.np_datetime', 'pandas._libs.skiplist', 'sqlite3', 'libiomp5md.dll'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Capjet Data Extractor_v1.21',
		  icon='icon.ico',
          debug=False,
          strip=False,
          upx=True,
          console=True)