# 📘 Manual do Usuário - The Sims 4 Mod Sorter

## Sumário
1. [Instalação Rápida](#instalação-rápida)
2. [Seu Primeiro Teste](#seu-primeiro-teste)
3. [Navegando o Menu](#navegando-o-menu)
4. [Referência de Funções](#referência-de-funções)
5. [Perguntas Frequentes](#perguntas-frequentes)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Instalação Rápida

### Requisitos Mínimos
- **Python 3.8+** instalado
- Mínimo 1 GB de espaço em disco
- Acesso de leitura/escrita nas pastas

### Passo 1: Preparar Python

#### Windows
1. Baixar em: https://www.python.org/downloads/windows/
2. **✅ Marcar** "Add Python to PATH"
3. Instalar

Verificar:
```bash
python --version
```

#### macOS
```bash
brew install python3
python3 --version
```

#### Linux
```bash
sudo apt-get install python3 python3-pip
python3 --version
```

### Passo 2: Baixar Projeto

**Opção A: Com Git**
```bash
git clone https://github.com/magnata32/sims4-mod-sorter.git
cd sims4-mod-sorter
```

**Opção B: Sem Git**
1. Ir em https://github.com/magnata32/sims4-mod-sorter
2. Clicar em **Code** > **Download ZIP**
3. Descompactar em uma pasta
4. Abrir PowerShell/Terminal nessa pasta

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

ou (macOS/Linux):

```bash
pip3 install -r requirements.txt
```

### Passo 4: Executar

```bash
python sims4_mod_sorter.py
```

ou (macOS/Linux):

```bash
python3 sims4_mod_sorter.py
```

✅ **Pronto!** O menu deve aparecer.

---

## 🎮 Seu Primeiro Teste

### Cenário Exemplo
Você tem 200 mods novos e quer saber se estão todos funcionando.

### Execução Completa

#### 1️⃣ Iniciar Script
```bash
python sims4_mod_sorter.py
```

#### 2️⃣ Escolher Opção 1
```
Escolha uma opção (1-5): 1
```

#### 3️⃣ Configurar Pastas
O script pergunta onde criar as pastas de controle.

⚠️ **Importante**: Use um caminho **simples**, sem caracteres especiais.

#### 4️⃣ Carregar Primeiro Lote
```
Escolha uma opção (1-4): 1
```

O script divide seus 200 mods em 100 + 100 e pergunta qual testar.

#### 5️⃣ Copiar Mods para o Jogo
O script move os 100 mods para `[0_Ativos_Em_Teste]`.

Copie todos os arquivos de lá para a pasta `Mods` do jogo.

#### 6️⃣ Registrar Resultado
```
Escolha uma opção (1-4): 3
```

Responda: **O jogo funcionou normalmente? (S/N)**

#### 7️⃣ Continuar Testando
Repita até que todos os mods sejam testados.

---

## 📋 Navegando o Menu

### Menu Principal

| Opção | Função |
|-------|--------|
| 1 | Iniciar teste 50/50 |
| 2 | Gerenciar pastas |
| 3 | Ver estatísticas |
| 4 | Sobre o projeto |
| 5 | Sair |

### Menu 50/50

| Opção | Função |
|-------|--------|
| 1 | Carregar próximo lote |
| 2 | Validar estrutura |
| 3 | Registrar resultado |
| 4 | Voltar |

---

## 🔧 Referência de Funções

### Carregar Próximo Lote
- Divide mods em 2 metades iguais
- Pergunta qual testar (A ou B)
- Move a metade escolhida para teste

### Registrar Resultado
- Pergunta se jogo funcionou (S/N)
- S → Mods para `[1_Mods_Seguros]` ✓
- N → Mods para `[2_Mods_Suspeitos_Quarentena]` ✗

### Validar Estrutura
- Detecta `.ts4script` aninhado incorretamente
- Encontra arquivos duplicados
- Lista problemas de estrutura

---

## ❓ Perguntas Frequentes

### P: Quantos mods testar por vez?
**R:** 50-100 mods é ideal.

### P: Quanto tempo leva?
**R:** Com 512 mods: apenas 9 testes (logarítmico!)

### P: E se testar a metade errada?
**R:** Sem problema! Você sabe que o erro está na OUTRA metade.

### P: Preciso remover mods após testar?
**R:** Sim! Limpe antes de carregar o próximo lote.

### P: Posso testar múltiplos lotes?
**R:** Não recomendado. Um lote por vez funciona melhor.

### P: Funciona com pasta diferente?
**R:** Sim! Escolha qualquer local durante configuração.

### P: E com Custom Content?
**R:** Sim! Mas CC raramente causa crashes.

---

## 🐛 Troubleshooting

### "Python não é reconhecido"
- Windows: Reinstalar com "Add Python to PATH"
- Linux/macOS: Use `python3` em vez de `python`

### "No module named 'colorama'"
```bash
pip install -r requirements.txt
```

### "Permission denied"
```bash
chmod +x sims4_mod_sorter.py
python3 sims4_mod_sorter.py
```

### "Caminho não encontrado"
- Use caminho simples: `C:\Temp\Sims4_Mods`
- Sem espaços ou caracteres especiais

### Mods não aparecem após mover
1. Fechar jogo completamente
2. Esperar 10 segundos
3. Executar script novamente

### Script fecha sem mensagem
1. Abrir terminal
2. Executar script novamente
3. Anotar mensagem de erro

---

## 📞 Precisa de Ajuda?

- 📖 [README.md](README.md) - Documentação principal
- 🐛 [Issues](https://github.com/magnata32/sims4-mod-sorter/issues) - Reportar bugs
- 💬 [Discussions](https://github.com/magnata32/sims4-mod-sorter/discussions) - Perguntas

---

**Divirta-se testando seus mods! 🎮✨**
