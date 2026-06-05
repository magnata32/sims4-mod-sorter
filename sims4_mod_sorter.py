#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The Sims 4 Mod Sorter - Automated 50/50 Testing Method
========================================================

A professional CLI tool for organizing and testing The Sims 4 mods using
the 50/50 method to identify corrupted or outdated mods.

Author: Magnata32
License: MIT
Repository: https://github.com/magnata32/sims4-mod-sorter
"""

import os
import sys
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

try:
    from colorama import Fore, Back, Style, init
    COLORAMA_AVAILABLE = True
    init(autoreset=True)
except ImportError:
    COLORAMA_AVAILABLE = False


# ============================================================================
# CONSTANTS
# ============================================================================

APP_VERSION = "1.0.0"
APP_NAME = "The Sims 4 Mod Sorter"
APP_AUTHOR = "Magnata32"
APP_REPO = "https://github.com/magnata32/sims4-mod-sorter"

FOLDER_NAMES = {
    "active": "[0_Ativos_Em_Teste]",
    "safe": "[1_Mods_Seguros]",
    "quarantine": "[2_Mods_Suspeitos_Quarentena]",
    "untested": "[3_Mods_Nao_Testados]",
}


# ============================================================================
# ENUMS & DATA CLASSES
# ============================================================================

class TestResult(Enum):
    """Enum for test result options."""
    SUCCESS = "S"
    FAILURE = "N"


@dataclass
class ModFolder:
    """Data class representing a mod folder configuration."""
    active_test: Path
    safe_mods: Path
    quarantine_mods: Path
    untested_mods: Path


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def colored_text(text: str, color: str = Fore.WHITE, style: str = Style.NORMAL) -> str:
    """
    Apply color to text. Falls back to plain text if colorama unavailable.

    Args:
        text: The text to colorize.
        color: Foreground color (default: WHITE).
        style: Text style (default: NORMAL).

    Returns:
        Colored text string or plain text.
    """
    if COLORAMA_AVAILABLE:
        return f"{style}{color}{text}{Style.RESET_ALL}"
    return text


def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(colored_text(title.center(70), Fore.CYAN, Style.BRIGHT))
    print("=" * 70 + "\n")


def print_success(msg: str) -> None:
    """Print success message."""
    print(colored_text(f"✓ {msg}", Fore.GREEN, Style.BRIGHT))


def print_error(msg: str) -> None:
    """Print error message."""
    print(colored_text(f"✗ {msg}", Fore.RED, Style.BRIGHT))


def print_warning(msg: str) -> None:
    """Print warning message."""
    print(colored_text(f"⚠ {msg}", Fore.YELLOW, Style.BRIGHT))


def print_info(msg: str) -> None:
    """Print informational message."""
    print(colored_text(f"ℹ {msg}", Fore.BLUE, Style.NORMAL))


def clear_screen() -> None:
    """Clear terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def get_user_input(prompt: str, valid_options: Optional[List[str]] = None) -> str:
    """
    Get validated user input from terminal.

    Args:
        prompt: Prompt message to display.
        valid_options: List of valid responses (case-insensitive).

    Returns:
        User input (uppercase).
    """
    while True:
        user_input = input(colored_text(prompt, Fore.CYAN)).strip().upper()

        if valid_options and user_input not in valid_options:
            print_error(f"Opção inválida. Use: {', '.join(valid_options)}")
            continue

        return user_input


def get_folder_path(prompt: str) -> Path:
    """
    Get a valid folder path from user.

    Args:
        prompt: Prompt message to display.

    Returns:
        Valid Path object.
    """
    while True:
        path_input = input(colored_text(prompt, Fore.CYAN)).strip()
        path = Path(path_input).expanduser()

        if path.exists() and path.is_dir():
            return path

        print_error(f"Caminho inválido ou não é uma pasta: {path_input}")


# ============================================================================
# FOLDER MANAGEMENT
# ============================================================================

def create_control_folders(base_path: Path) -> ModFolder:
    """
    Create or verify control folders structure.

    Args:
        base_path: Base path where control folders will be created.

    Returns:
        ModFolder object with all folder paths.
    """
    print_info("Criando estrutura de pastas de controle...")

    active_test = base_path / FOLDER_NAMES["active"]
    safe_mods = base_path / FOLDER_NAMES["safe"]
    quarantine_mods = base_path / FOLDER_NAMES["quarantine"]
    untested_mods = base_path / FOLDER_NAMES["untested"]

    for folder in [active_test, safe_mods, quarantine_mods, untested_mods]:
        folder.mkdir(parents=True, exist_ok=True)

    print_success(f"Pastas criadas em: {base_path}")
    return ModFolder(active_test, safe_mods, quarantine_mods, untested_mods)


def get_mod_files(folder: Path, recursive: bool = True) -> List[Path]:
    """
    Get all mod files from a folder (excluding directories).

    Args:
        folder: Folder path to scan.
        recursive: Whether to search recursively.

    Returns:
        List of mod file paths.
    """
    if not folder.exists():
        return []

    pattern = "**/*" if recursive else "*"
    mod_files = [
        f for f in folder.glob(pattern)
        if f.is_file() and not f.name.startswith(".")
    ]

    return sorted(mod_files)


def get_mod_size(file_path: Path) -> int:
    """Get file size in bytes."""
    try:
        return file_path.stat().st_size
    except OSError:
        return 0


def count_mods_in_folder(folder: Path) -> int:
    """Count total mod files in a folder."""
    return len(get_mod_files(folder))


def format_file_size(size_bytes: int) -> str:
    """Format bytes to human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


# ============================================================================
# VALIDATION & CHECKS
# ============================================================================

def check_nested_ts4scripts(folder: Path) -> List[Tuple[Path, int]]:
    """
    Check for .ts4script files in nested subfolders (more than 1 level deep).

    Args:
        folder: Folder path to scan.

    Returns:
        List of tuples (file_path, depth_level) for problematic files.
    """
    problematic_files = []

    for file_path in folder.rglob("*.ts4script"):
        relative_path = file_path.relative_to(folder)
        depth = len(relative_path.parts)

        if depth > 2:  # Root level is 1, one subfolder is 2
            problematic_files.append((file_path, depth))

    return problematic_files


def find_duplicate_files(folder: Path) -> dict:
    """
    Find duplicate files by name in a folder.

    Args:
        folder: Folder path to scan.

    Returns:
        Dictionary with filename as key and list of paths as value.
    """
    files_dict = {}

    for file_path in get_mod_files(folder):
        filename = file_path.name
        if filename not in files_dict:
            files_dict[filename] = []
        files_dict[filename].append(file_path)

    duplicates = {k: v for k, v in files_dict.items() if len(v) > 1}
    return duplicates


def validate_mod_structure(folder: Path) -> None:
    """
    Run all validation checks on a folder.

    Args:
        folder: Folder path to validate.
    """
    print_header("VALIDAÇÃO DE ESTRUTURA DE MODS")
    
    print_info("Executando validações de estrutura...")

    # Check nested .ts4script files
    nested_scripts = check_nested_ts4scripts(folder)
    if nested_scripts:
        print_warning("Arquivos .ts4script encontrados em subpastas aninhadas:")
        for file_path, depth in nested_scripts:
            print_warning(f"  └─ {file_path.relative_to(folder)} (profundidade: {depth})")
        print_warning("Esses arquivos podem não funcionar corretamente no jogo!")
    else:
        print_success("Nenhum arquivo .ts4script aninhado incorretamente encontrado!")

    # Check duplicates
    duplicates = find_duplicate_files(folder)
    if duplicates:
        print_warning("\nArquivos duplicados encontrados:")
        for filename, paths in duplicates.items():
            print_warning(f"  └─ {filename} ({len(paths)} cópias)")
            for path in paths:
                size_kb = format_file_size(get_mod_size(path))
                print_warning(f"     - {path.relative_to(folder)} ({size_kb})")
    else:
        print_success("Nenhum arquivo duplicado encontrado!")

    print("\n")
    input(colored_text("Pressione ENTER para continuar...", Fore.CYAN))


# ============================================================================
# CORE LOGIC: 50/50 METHOD
# ============================================================================

def split_mods_50_50(mods: List[Path]) -> Tuple[List[Path], List[Path]]:
    """
    Split mod list into two equal halves for 50/50 testing.

    Args:
        mods: List of mod file paths.

    Returns:
        Tuple of (first_half, second_half).
    """
    mid_point = len(mods) // 2
    return mods[:mid_point], mods[mid_point:]


def move_files_to_folder(files: List[Path], destination: Path, operation: str = "move") -> None:
    """
    Move or copy files to destination folder.

    Args:
        files: List of file paths to move/copy.
        destination: Destination folder path.
        operation: "move" or "copy".
    """
    destination.mkdir(parents=True, exist_ok=True)

    for file_path in files:
        try:
            dest_file = destination / file_path.name

            if operation == "move":
                shutil.move(str(file_path), str(dest_file))
            elif operation == "copy":
                shutil.copy2(str(file_path), str(dest_file))

        except Exception as e:
            print_error(f"Erro ao processar {file_path.name}: {e}")


def empty_folder(folder: Path) -> int:
    """
    Remove all files from a folder.

    Args:
        folder: Folder path to empty.

    Returns:
        Number of files removed.
    """
    count = 0
    for file_path in get_mod_files(folder):
        try:
            file_path.unlink()
            count += 1
        except Exception as e:
            print_error(f"Erro ao remover {file_path.name}: {e}")

    return count


def run_50_50_test(mod_folders: ModFolder) -> None:
    """
    Main 50/50 testing workflow.

    Args:
        mod_folders: ModFolder object with all folder paths.
    """
    while True:
        print_header("MÉTODO 50/50 - TESTE DE MODS")

        # Count untested mods
        untested_mods = get_mod_files(mod_folders.untested_mods)
        active_mods = get_mod_files(mod_folders.active_test)

        print(colored_text("Status Atual:", Fore.CYAN, Style.BRIGHT))
        print(f"  Mods não testados: {len(untested_mods)}")
        print(f"  Mods em teste ativo: {len(active_mods)}")
        print(f"  Mods seguros: {count_mods_in_folder(mod_folders.safe_mods)}")
        print(f"  Mods em quarentena: {count_mods_in_folder(mod_folders.quarantine_mods)}\n")

        # Menu options
        print("Opções:")
        print("  1 - Carregar próximo lote (50/50)")
        print("  2 - Validar estrutura de mods")
        print("  3 - Registrar resultado do teste")
        print("  4 - Voltar ao menu principal")

        choice = get_user_input("Escolha uma opção (1-4): ", ["1", "2", "3", "4"])

        if choice == "1":
            load_next_batch(mod_folders)
        elif choice == "2":
            validate_mod_structure(mod_folders.untested_mods)
        elif choice == "3":
            record_test_result(mod_folders)
        elif choice == "4":
            break


def load_next_batch(mod_folders: ModFolder) -> None:
    """
    Load the next 50/50 batch for testing.

    Args:
        mod_folders: ModFolder object with all folder paths.
    """
    print_header("CARREGANDO PRÓXIMO LOTE")

    # Clear active test folder
    if get_mod_files(mod_folders.active_test):
        print_warning("Pasta de teste ativo não está vazia!")
        response = get_user_input("Deseja limpar e continuar? (S/N): ", ["S", "N"])
        if response == "N":
            return
        removed = empty_folder(mod_folders.active_test)
        print_success(f"{removed} arquivo(s) removido(s).")

    # Get untested mods
    untested_mods = get_mod_files(mod_folders.untested_mods)

    if not untested_mods:
        print_error("Nenhum mod não testado disponível!")
        input(colored_text("Pressione ENTER para continuar...", Fore.CYAN))
        return

    # Split 50/50
    batch_a, batch_b = split_mods_50_50(untested_mods)

    print(f"Total de mods não testados: {len(untested_mods)}")
    print(f"\nLote A: {len(batch_a)} mods")
    print(f"Lote B: {len(batch_b)} mods\n")

    print("Qual lote deseja testar?")
    print("  A - Primeira metade (Lote A)")
    print("  B - Segunda metade (Lote B)")

    choice = get_user_input("Escolha (A/B): ", ["A", "B"])
    selected_batch = batch_a if choice == "A" else batch_b

    # Move batch to active test folder
    move_files_to_folder(selected_batch, mod_folders.active_test, operation="move")

    print_success(f"Lote {choice} ({len(selected_batch)} mods) movido para teste!")
    print_info(f"Localização: {mod_folders.active_test}")
    print_info("Abra o jogo e teste normalmente. Quando terminar, retorne ao script.")

    input(colored_text("\nPressione ENTER para continuar...", Fore.CYAN))


def record_test_result(mod_folders: ModFolder) -> None:
    """
    Record the test result and move mods accordingly.

    Args:
        mod_folders: ModFolder object with all folder paths.
    """
    print_header("REGISTRANDO RESULTADO DO TESTE")

    active_mods = get_mod_files(mod_folders.active_test)

    if not active_mods:
        print_error("Nenhum mod em teste ativo!")
        input(colored_text("Pressione ENTER para continuar...", Fore.CYAN))
        return

    print(f"Mods em teste: {len(active_mods)}\n")

    result = get_user_input(
        "O jogo funcionou normalmente? (S/N): ",
        [TestResult.SUCCESS.value, TestResult.FAILURE.value]
    )

    if result == TestResult.SUCCESS.value:
        destination = mod_folders.safe_mods
        destination_name = "Mods Seguros"
    else:
        destination = mod_folders.quarantine_mods
        destination_name = "Quarentena"

    move_files_to_folder(active_mods, destination, operation="move")
    print_success(f"Todos os {len(active_mods)} mods movidos para: {destination_name}")

    input(colored_text("Pressione ENTER para continuar...", Fore.CYAN))


# ============================================================================
# MAIN MENU & INITIALIZATION
# ============================================================================

def show_main_menu() -> None:
    """Display main menu and handle options."""
    while True:
        clear_screen()
        print_header("THE SIMS 4 MOD SORTER - MÉTODO 50/50")

        print("Menu Principal:")
        print("  1 - Iniciar teste de mods (50/50)")
        print("  2 - Gerenciar pastas de mods")
        print("  3 - Ver estatísticas")
        print("  4 - Sobre o projeto")
        print("  5 - Sair")

        choice = get_user_input("Escolha uma opção (1-5): ", ["1", "2", "3", "4", "5"])

        if choice == "1":
            mod_folders = setup_mod_folders()
            run_50_50_test(mod_folders)
        elif choice == "2":
            manage_folders_menu()
        elif choice == "3":
            show_statistics()
        elif choice == "4":
            show_about()
        elif choice == "5":
            print_success("Até logo!")
            sys.exit(0)


def setup_mod_folders() -> ModFolder:
    """Setup and verify mod folders configuration."""
    print_header("CONFIGURAÇÃO DE PASTAS")

    # Ask for base path
    print("Indique onde deseja armazenar as pastas de controle:")
    print("(Por padrão, use um local FORA da pasta 'Mods' do jogo)")
    print("(Ex: C:\\Desktop\\Sims4_ModControl)\n")
    
    base_path = get_folder_path("Caminho base: ")

    # Verify structure
    mod_folders = create_control_folders(base_path)

    print_success("Configuração concluída!")
    print_info(f"Base: {base_path}\n")

    input(colored_text("Pressione ENTER para continuar...", Fore.CYAN))
    return mod_folders


def manage_folders_menu() -> None:
    """Menu for folder management."""
    print_header("GERENCIADOR DE PASTAS")

    print("Opções:")
    print("  1 - Ver localizações das pastas")
    print("  2 - Abrir pasta [0_Ativos_Em_Teste] no explorador")
    print("  3 - Limpar pasta de teste ativo")
    print("  4 - Voltar")

    choice = get_user_input("Escolha uma opção (1-4): ", ["1", "2", "3", "4"])

    if choice == "1":
        print_info("As pastas estão localizadas no caminho base que você configurou.")
        print_info("Procure por pastas começando com [0_], [1_], [2_] e [3_].")
    elif choice == "2":
        print_info("Funcionalidade disponível em breve.")
    elif choice == "3":
        print_warning("Funcionalidade em desenvolvimento.")
    elif choice == "4":
        return

    input(colored_text("Pressione ENTER para continuar...", Fore.CYAN))


def show_statistics() -> None:
    """Display statistics about mod sorting progress."""
    print_header("ESTATÍSTICAS")
    print_info("Esta seção exibiria estatísticas de progresso em futuras versões.")
    print_info("Por enquanto, use o 'Status Atual' no menu 50/50.")
    input(colored_text("Pressione ENTER para continuar...", Fore.CYAN))


def show_about() -> None:
    """Display about information."""
    print_header("SOBRE O PROJETO")

    about_text = f"""
{APP_NAME} - Método 50/50 Automatizado
{'=' * 55}

Versão: {APP_VERSION}
Autor: {APP_AUTHOR}
Licença: MIT
GitHub: {APP_REPO}

SOBRE O PROJETO:
Este é um projeto open-source criado para automatizar o
processo de identificação de mods corrompidos ou
desatualizados utilizando o método 50/50.

FUNCIONALIDADES:
  • Divisão automática de mods em lotes 50/50
  • Organização inteligente em categorias
  • Validação de estrutura de mods
  • Detecção de arquivos duplicados
  • Interface CLI intuitiva e colorida

COMO USAR:
1. Configure o local das pastas de controle
2. Importe seus mods para [3_Mods_Nao_Testados]
3. Use o método 50/50 para testar
4. Organize automaticamente resultados

CONTRIBUINDO:
Se deseja contribuir para o projeto, visite:
{APP_REPO}/blob/main/CONTRIBUTING.md

Aproveite o ferramental! 🎮
    """

    print(about_text)
    input(colored_text("Pressione ENTER para voltar...", Fore.CYAN))


def main() -> None:
    """Main entry point of the application."""
    try:
        show_main_menu()
    except KeyboardInterrupt:
        print_warning("\nPrograma interrompido pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
