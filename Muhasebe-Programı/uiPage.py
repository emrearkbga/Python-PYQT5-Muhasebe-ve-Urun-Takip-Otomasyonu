from PyQt5 import uic

with open('Muhasebe.py', 'w', encoding="utf-8") as fout:
    uic.compileUi('Muhasebe.ui', fout)

# with open('Anasayfa.py', 'w', encoding="utf-8") as fout:
#     uic.compileUi('Anasayfa.ui', fout)