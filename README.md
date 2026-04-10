# 📸 Instagram Followback Checker

Um script Python para identificar quem você segue no Instagram mas não segue de volta.

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![Windows](https://img.shields.io/badge/Windows-0078D6?logo=windows&logoColor=white)](https://github.com)
[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://github.com)
[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Funcionalidades

- ✅ Detecta contas que você segue mas não te seguem de volta
- ✅ Suporte a autenticação de dois fatores (2FA)
- ✅ Gera relatório HTML com links clicáveis
- ✅ Separa contas verificadas das não verificadas
- ✅ Interface simples no terminal
- ✅ Nenhuma senha é salva (seguro)

## 🚀 Como usar - Escolha sua opção

### Opção 1: Para usuários comuns (SEM necessidade de Python) 🎯

**Windows apenas** - Baixe o executável pronto:

1. Acesse a [página de Releases](https://github.com/SEU_USUARIO/instagram-followback-checker/releases)
2. Baixe o arquivo `instagram_followback.exe`
3. Dê **duplo clique** no arquivo baixado
4. Siga as instruções no terminal

> ⚠️ **Nota**: O Windows pode mostrar um aviso de segurança. Clique em "Executar mesmo assim" - é seguro!

### Opção 2: Para usuários que preferem o código fonte 🐍

**Requer Python 3.7+ instalado**

#### Instalação rápida:

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/instagram-followback-checker.git
cd instagram-followback-checker

# Instale a dependência
pip install -r requirements.txt

# Execute
python instagram_followback.py
```

### Ou usando os scripts automáticos:

- **Windows**: Dê duplo clique em `run.bat`
- **Mac/Linux**: Execute `./run.sh` (use `chmod +x run.sh` primeiro)

## 📊 Como funciona

1. O script pede seu **usuário** e **senha** do Instagram
2. Se tiver 2FA ativado, pedirá o código de verificação
3. O script analisa sua lista de "seguindo" e "seguidores"
4. Gera um relatório HTML com quem não te segue de volta
5. O relatório abre automaticamente no seu navegador

## 🔒 Segurança

- **Nenhuma credencial é salva** em arquivos
- As senhas são inseridas via `getpass` (não ficam visíveis)
- Todo processo é local no seu computador
- **Suporte total ao 2FA** - não precisa desativar!

## 📸 Exemplo do relatório gerado

O relatório HTML inclui:

- Total de contas que não seguem de volta
- Lista completa com links diretos para os perfis
- Separação entre contas comuns e verificadas
- Design moderno e responsivo
- Links clicáveis que abrem em nova aba

## 📦 Para desenvolvedores: Gerando seu próprio .EXE

Se quiser gerar o executável você mesmo:

```bash
# Instale o PyInstaller
pip install pyinstaller

# Execute o script de build
python build_exe.py

# Ou use o PyInstaller diretamente
pyinstaller --onefile --console --name "instagram_followback" instagram_followback.py
```
O executável será gerado na pasta `dist/`

## 🖥️ Compatibilidade

| Sistema Operacional | Código Fonte (.py) | Executável (.exe) |
|-------------------|-------------------|-------------------|
| Windows 10/11     | ✅ Sim            | ✅ Sim (baixe o .exe) |
| macOS             | ✅ Sim            | ❌ Não (use código fonte) |
| Linux             | ✅ Sim            | ❌ Não (use código fonte) |

## ⚠️ Avisos importantes

- **Limites do Instagram**: Evite executar muitas vezes seguidas
- **Contas grandes**: Se você segue muitas pessoas (+2000), o processo pode levar alguns minutos
- **Conexão estável**: Necessária para coletar os dados

## 🐛 Problemas comuns e soluções

### "O Windows protegeu seu PC" ao executar o .exe

1. Clique em **"Mais informações"**
2. Clique em **"Executar mesmo assim"**
3. Isso ocorre porque o executável é novo, mas é seguro

### Erro de login

- Verifique usuário/senha
- Se tiver 2FA, aguarde o código ser solicitado
- Considere criar uma [senha de aplicativo](https://help.instagram.com/113833587843245) no Instagram

### O script está demorando muito

- Normal para contas com muitos seguidores (5-10 minutos)
- O Instagram limita requisições, então há pausas automáticas

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## ⭐ Agradecimentos

- [Instaloader](https://instaloader.github.io/) - Biblioteca incrível para interagir com o Instagram
- [PyInstaller](https://pyinstaller.org/) - Para gerar o executável
