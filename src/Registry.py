import winreg

def read_registry(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
            r"SOFTWARE\Hewlett-Packard\HP Touchpoint Manager\Agent", 
            0, 
            winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        print(value)
        return value
    except WindowsError:
        return None