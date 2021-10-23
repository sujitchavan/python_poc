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
    except:
        return None

def write_registry(path, key, value):
    try:
        reg_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
        winreg.SetValueEx(reg_key, key, 0, winreg.REG_SZ, value)
        winreg.CloseKey(reg_key)
    except:
        return None
    

def delete_registry(Path):
    try:
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, path)
    except:
        return None