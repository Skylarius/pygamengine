# -*- coding: utf-8 -*-

import os
import sys
import inspect

# Aggiungo questo sennó non funziona un cazzo NEI file della cartella demo
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print("->" + current_dir)
parent_dir = os.path.dirname(current_dir)
print("->" + parent_dir)
src_dir = os.path.join(parent_dir, "src")
print("->" + src_dir)
sys.path.insert(0, src_dir)