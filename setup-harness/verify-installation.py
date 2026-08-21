#!/usr/bin/env python3
"""
Script de verificação - Ferramentas para Harness Bibliográfico
Verifica se todas as ferramentas foram instaladas corretamente
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(title):
    """Imprime cabeçalho com formatação"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}\n")

def check_command(command, name):
    """Verifica se um comando está disponível"""
    try:
        subprocess.run(
            [command, "--version"],
            capture_output=True,
            check=False,
            timeout=5
        )
        print(f"✓ {name} encontrado")
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(f"✗ {name} não encontrado")
        return False

def check_zotero():
    """Verifica instalação do Zotero"""
    zotero_paths = [
        Path("C:/Program Files/Zotero/zotero.exe"),
        Path("C:/Program Files (x86)/Zotero/zotero.exe"),
        Path(os.path.expanduser("~/.wine/drive_c/Program Files/Zotero/zotero.exe"))
    ]
    
    for path in zotero_paths:
        if path.exists():
            print(f"✓ Zotero encontrado em: {path}")
            return True
    
    print("✗ Zotero não encontrado")
    print("  Instale em: https://www.zotero.org/download/")
    return False

def check_docling():
    """Verifica instalação do Docling"""
    try:
        import docling
        version = docling.__version__
        print(f"✓ Docling {version} encontrado")
        return True
    except ImportError:
        print("✗ Docling não encontrado")
        print("  Instale com: pip install docling")
        return False

def check_obsidian():
    """Verifica instalação do Obsidian"""
    obsidian_paths = [
        Path("C:/Program Files/Obsidian/Obsidian.exe"),
        Path("C:/Program Files (x86)/Obsidian/Obsidian.exe"),
        Path(os.path.expanduser("~/AppData/Local/Programs/Obsidian/Obsidian.exe"))
    ]
    
    for path in obsidian_paths:
        if path.exists():
            print(f"✓ Obsidian encontrado em: {path}")
            return True
    
    # Instalações customizadas (ex.: outro drive) ficam registradas no Windows,
    # sob uma subchave com nome de GUID, então é preciso varrer e checar o DisplayName
    if sys.platform == "win32":
        try:
            import winreg
            uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            hives = (
                (winreg.HKEY_CURRENT_USER, uninstall_key),
                (winreg.HKEY_LOCAL_MACHINE, uninstall_key),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            )
            for hive, subkey_path in hives:
                try:
                    with winreg.OpenKey(hive, subkey_path) as uninstall_root:
                        for i in range(winreg.QueryInfoKey(uninstall_root)[0]):
                            subkey_name = winreg.EnumKey(uninstall_root, i)
                            with winreg.OpenKey(uninstall_root, subkey_name) as entry:
                                try:
                                    display_name = winreg.QueryValueEx(entry, "DisplayName")[0]
                                except FileNotFoundError:
                                    continue
                                if "Obsidian" not in display_name:
                                    continue
                                exe_path = None
                                try:
                                    install_location = winreg.QueryValueEx(entry, "InstallLocation")[0]
                                    if install_location:
                                        exe_path = Path(install_location) / "Obsidian.exe"
                                except FileNotFoundError:
                                    pass
                                if not exe_path or not exe_path.exists():
                                    try:
                                        display_icon = winreg.QueryValueEx(entry, "DisplayIcon")[0]
                                        exe_path = Path(display_icon.split(",")[0])
                                    except FileNotFoundError:
                                        continue
                                if exe_path.exists():
                                    print(f"✓ Obsidian encontrado em: {exe_path}")
                                    return True
                except FileNotFoundError:
                    continue
        except ImportError:
            pass
    
    print("✗ Obsidian não encontrado")
    print("  Instale em: https://obsidian.md/download")
    return False

def check_obsidian_plugin():
    """Verifica instalação do plugin Local REST API"""
    plugin_path = Path(os.path.expanduser("~/.Obsidian/plugins/obsidian-local-rest-api"))
    appdata_plugin = Path(os.path.expanduser("~/AppData/Roaming/Obsidian/plugins/obsidian-local-rest-api"))
    
    actual_path = None
    if plugin_path.exists():
        actual_path = plugin_path
    elif appdata_plugin.exists():
        actual_path = appdata_plugin
    
    if actual_path:
        manifest = actual_path / "manifest.json"
        if manifest.exists():
            print(f"✓ Plugin Local REST API encontrado em: {actual_path}")
            with open(manifest, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"  Versão: {data.get('version', 'desconhecida')}")
            return True
        else:
            print(f"✗ Pasta do plugin encontrada em {actual_path}, mas manifest.json ausente")
            print("  Reinstale o plugin: execute setup-tools.ps1 novamente")
            return False
    
    print("✗ Plugin Local REST API não encontrado")
    print("  Local esperado: %APPDATA%/Obsidian/plugins/obsidian-local-rest-api")
    print("  Instale em Obsidian: Configurações > Plugins Instalados > 'Local REST API'")
    return False

def check_python():
    """Verifica instalação do Python"""
    try:
        result = subprocess.run(
            ["python", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        version = result.stdout.strip() or result.stderr.strip()
        print(f"✓ Python {version}")
        return True
    except FileNotFoundError:
        print("✗ Python não encontrado")
        print("  Instale em: https://www.python.org/downloads/")
        return False

def main():
    """Função principal"""
    print_header("Verificação de Ferramentas - Harness Bibliográfico")
    
    results = {}
    
    print("1. VERIFICANDO PYTHON")
    print("-" * 50)
    results["python"] = check_python()
    
    print("\n2. VERIFICANDO ZOTERO 7+")
    print("-" * 50)
    results["zotero"] = check_zotero()
    
    print("\n3. VERIFICANDO DOCLING (IBM)")
    print("-" * 50)
    results["docling"] = check_docling()
    
    print("\n4. VERIFICANDO OBSIDIAN")
    print("-" * 50)
    results["obsidian"] = check_obsidian()
    
    print("\n5. VERIFICANDO OBSIDIAN LOCAL REST API PLUGIN")
    print("-" * 50)
    results["obsidian_plugin"] = check_obsidian_plugin()
    
    # Resumo
    print_header("RESUMO")
    
    installed = sum(results.values())
    total = len(results)
    
    status_map = {
        "python": "Python",
        "zotero": "Zotero",
        "docling": "Docling",
        "obsidian": "Obsidian",
        "obsidian_plugin": "Local REST API Plugin"
    }
    
    for key, name in status_map.items():
        status = "✓" if results[key] else "✗"
        print(f"{status} {name}")
    
    print(f"\n{installed}/{total} ferramentas instaladas")
    
    if installed == total:
        print("\n✓ Todas as ferramentas estão instaladas e prontas!")
        return 0
    else:
        print(f"\n✗ {total - installed} ferramentas ainda precisam ser instaladas")
        print("\nExecute: .\\setup-tools.ps1 (PowerShell) ou setup-tools.bat (CMD)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
