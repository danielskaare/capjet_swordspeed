# -*- mode: python -*-

block_cipher = None


a = Analysis(['Capjet_Sword_Speed_v1.08.py'],
             pathex=[],
             binaries=None,
             datas=[('Config_Main_Setup.ini', '.'),('Config_Sword_Speed_CapjetB_TEST.ini', '.'), ('Batch_Script_VideoLogger_B_TEST.bat', '.'), ('Batch_Script_VideoLogger_A_TEST.bat', '.'), ('Config_Sword_Speed_CapjetA_TEST.ini', '.'), ('dependencies/Instructions_v0.91.pdf', '.'), ('dependencies/mkl_avx2.dll', '.'), ('dependencies/mkl_def.dll', './dep'), ('dependencies/mkl_vml_avx2.dll', '.'), ('dependencies/mkl_vml_def.dll', '.'), ('InputData/.', 'InputData/'), ('OutputData/', 'OutputData/')],
             hiddenimports=['pandas._libs.tslibs.timedeltas', 'pandas._libs.tslibs.nattype', 'pandas._libs.tslibs.np_datetime', 'pandas._libs.skiplist'],
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
          name='Capjet_Sword_Speed_v1.08',
          debug=False,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Capjet_Sword_Speed_v1.08')
