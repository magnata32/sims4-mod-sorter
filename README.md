# The Sims 4 Mod Sorter 🎮

**Método 50/50 Automatizado para Identificar Mods Corrompidos**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)

## 📋 Sobre o Projeto

**The Sims 4 Mod Sorter** é uma ferramenta CLI profissional para automatizar o processo de organização e teste de mods usando o **Método 50/50**.

### O Problema
Mods corrompidos causam crashes no jogo. Identificá-los testando um por um é tedioso.

### A Solução
Este script divide seus mods em **duas metades**, testa uma, e move os resultados:
- ✅ **Funciona?** Metade segura
- ❌ **Erro?** Subdivida e repita

Com ~512 mods: apenas **9 testes** em vez de 512!

## ⚡ Funcionalidades

- ✅ Divisão automática 50/50
- ✅ Gerenciamento de pastas inteligente
- ✅ Detecção de aninhamento incorreto
- ✅ Busca de arquivos duplicados
- ✅ Interface CLI colorida e intuitiva

## 📦 Instalação Rápida

### Requisitos
- Python 3.8+
- 1 GB espaço em disco

### Passos

```bash
# 1. Clonar repositório
git clone https://github.com/magnata32/sims4-mod-sorter.git
cd sims4-mod-sorter

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar
python sims4_mod_sorter.py
```

## 🎮 Como Usar

1. **Iniciar script** → `python sims4_mod_sorter.py`
2. **Configurar pastas** → Escolha um local para armazenar
3. **Carregar lote** → Script divide 50/50
4. **Testar no jogo** → Copie mods para `Mods` do jogo
5. **Registrar resultado** → Digite S/N
6. **Repetir** → Até isolar mods problemáticos

## 📖 Documentação

- **README.md** - Este arquivo
- **MANUAL_DO_USUARIO.md** - Guia passo-a-passo completo

## 🛠️ Estrutura de Pastas

```
Caminho Base (sua escolha)/
├── [0_Ativos_Em_Teste]      ← Testando agora
├── [1_Mods_Seguros]          ← Aprovados ✓
├── [2_Mods_Suspeitos_Quarentena] ← Com erro ✗
└── [3_Mods_Nao_Testados]    ← Fila
```

## 📋 Validações Automáticas

- ⚠️ Detecta `.ts4script` em subpastas muito profundas
- ⚠️ Identifica arquivos duplicados
- ✓ Cria pastas automaticamente

## 📄 Licença

MIT - Veja [LICENSE](LICENSE)

## 🤝 Contribuindo

Encontrou um bug? Tem sugestão? Abra uma [Issue](https://github.com/magnata32/sims4-mod-sorter/issues)!

---

**Desenvolvido com ❤️ para a comunidade The Sims 4**
