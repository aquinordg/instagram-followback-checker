#!/usr/bin/env python3
"""
Script para gerar o executável .exe do Instagram Followback Checker
Executar: python build_exe.py
"""

import os
import sys
import shutil
import subprocess
import glob

def check_pyinstaller():
    """Verifica se o PyInstaller está instalado"""
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller não está instalado")
        print("\n📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado com sucesso!")
        return True

def clean_old_build():
    """Limpa builds anteriores"""
    print("\n🧹 Limpando builds anteriores...")
    
    folders_to_remove = ['build', 'dist', '__pycache__']
    for folder in folders_to_remove:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   Removido: {folder}")
    
    files_to_remove = glob.glob('*.spec')
    for file in files_to_remove:
        os.remove(file)
        print(f"   Removido: {file}")

def build_executable():
    """Gera o executável"""
    print("\n🔨 Gerando executável...")
    print("   Isso pode levar alguns minutos...")
    
    # Comando do PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",           # Único arquivo
        "--console",           # Janela do terminal
        "--name", "instagram_followback",
        "--clean",             # Limpa cache
        "--noconfirm",         # Não perguntar confirmações
        "instagram_followback.py"
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=False)
        print("\n✅ Executável gerado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao gerar executável: {e}")
        return False

def show_result():
    """Mostra onde o executável foi gerado"""
    exe_path = os.path.join("dist", "instagram_followback.exe")
    
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path) / (1024 * 1024)  # Tamanho em MB
        print("\n" + "="*50)
        print("✅ BUILD CONCLUÍDO COM SUCESSO!")
        print("="*50)
        print(f"\n📁 Executável gerado em: {exe_path}")
        print(f"📦 Tamanho: {size:.2f} MB")
        print("\n💡 Para distribuir:")
        print("   1. Copie o arquivo .exe para onde quiser")
        print("   2. O usuário só precisa dar duplo clique!")
        print("\n📝 Lembrete: Adicione este .exe nas releases do GitHub")
    else:
        print("\n❌ Erro: Executável não foi encontrado!")

def main():
    """Função principal"""
    print("="*60)
    print("   GERADOR DE EXECUTÁVEL - INSTAGRAM FOLLOWBACK")
    print("="*60)
    
    # Verificar PyInstaller
    if not check_pyinstaller():
        print("❌ Não foi possível continuar sem o PyInstaller")
        sys.exit(1)
    
    # Limpar builds antigos
    clean_old_build()
    
    # Gerar executável
    if build_executable():
        show_result()
    else:
        print("\n❌ Falha na geração do executável")
        sys.exit(1)

if __name__ == "__main__":
    main()