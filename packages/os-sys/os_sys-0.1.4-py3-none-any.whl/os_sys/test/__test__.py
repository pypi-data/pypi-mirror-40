index = 0
try:
    from os_sys import os_sys
except Exception:
    import os_sys
lijst = list(os_sys.__all_names__)
lijst_mod = list(os_sys.__all_names__)
while index < len(lijst):
    print('module: ' + str(lijst_mod[index]) + ' ready to import: ' + str(hasattr(os_sys, str(lijst[index]))))
    index = index + 1

