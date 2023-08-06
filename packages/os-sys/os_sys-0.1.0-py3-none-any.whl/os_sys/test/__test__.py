index = 0
try:
    from os_sys import os_sys
except Exception:
    import os_sys
lijst = list(os_sys.__all_names__)
lijst_module
while index < len(lijst):
    print('module: ' + lijst_module[index] + 'ready to import: ' + hasattr(os_sys, lijst[index]))
    index = index + 1
