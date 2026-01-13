# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec-fil för LIA Rapportgenerator
Säkerställer att alla moduler från src/ inkluderas i exe-filen
"""

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Inkludera alla Python-filer från src/
        ('src/excel_reader.py', 'src'),
        ('src/flexible_excel_reader.py', 'src'),
        ('src/gui.py', 'src'),
        ('src/pdf_generator.py', 'src'),
        # Inkludera templates/
        ('templates/rapport_mall.py', 'templates'),
    ],
    hiddenimports=[
        # Explicit inkludera alla src-moduler
        'src.excel_reader',
        'src.flexible_excel_reader',
        'src.gui',
        'src.pdf_generator',
        'templates.rapport_mall',
        # Viktiga beroenden
        'pandas',
        'openpyxl',
        'reportlab',
        'reportlab.lib.pagesizes',
        'reportlab.lib.styles',
        'reportlab.lib.units',
        'reportlab.lib.colors',
        'reportlab.platypus',
        'reportlab.pdfbase',
        'reportlab.pdfbase.ttfonts',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LIA_Rapportgenerator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Ingen konsol-fönster (GUI-app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Lägg till ikon här om du har en: 'icon.ico'
)
