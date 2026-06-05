#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The Sims 4 Mod Sorter - Versão com Interface Gráfica
======================================================

A professional GUI tool for organizing and testing The Sims 4 mods using
the 50/50 method to identify corrupted or outdated mods.

Author: Magnata32
License: MIT
Repository: https://github.com/magnata32/sims4-mod-sorter
"""

import os
import sys
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading

class ModSorterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("The Sims 4 Mod Sorter - Método 50/50")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        self.folders = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Menu principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text="The Sims 4 Mod Sorter", 
                font=("Arial", 20, "bold")).pack(pady=10)
        
        tk.Label(main_frame, text="Método 50/50 para testar mods",
                font=("Arial", 12)).pack(pady=5)
        
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Iniciar Configuração", 
                 command=self.start_setup, width=30, height=2,
                 font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=5)
        
        tk.Button(button_frame, text="Sobre", 
                 command=self.show_about, width=30, height=2,
                 font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=5)
        
        tk.Button(button_frame, text="Sair", 
                 command=self.root.quit, width=30, height=2,
                 font=("Arial", 12), bg="#f44336", fg="white").pack(pady=5)
        
        # Área de log
        log_frame = tk.LabelFrame(main_frame, text="Log de Atividades", font=("Arial", 10))
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, bg="#f5f5f5")
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def show_about(self):
        messagebox.showinfo("Sobre", 
            "The Sims 4 Mod Sorter v1.0.0\n\n"
            "Método 50/50 Automatizado\n\n"
            "GitHub: https://github.com/magnata32/sims4-mod-sorter\n\n"
            "Author: Magnata32\n"
            "License: MIT")
    
    def start_setup(self):
        folder = filedialog.askdirectory(title="Selecione a pasta para armazenar os mods")
        if not folder:
            return
        
        self.setup_folders(Path(folder))
        self.show_main_menu()
    
    def setup_folders(self, base_path):
        self.log("🔧 Criando estrutura de pastas...")
        
        active_test = base_path / "[0_Ativos_Em_Teste]"
        safe_mods = base_path / "[1_Mods_Seguros]"
        quarantine_mods = base_path / "[2_Mods_Suspeitos_Quarentena]"
        untested_mods = base_path / "[3_Mods_Nao_Testados]"
        
        for folder in [active_test, safe_mods, quarantine_mods, untested_mods]:
            folder.mkdir(parents=True, exist_ok=True)
        
        self.folders = {
            'active': active_test,
            'safe': safe_mods,
            'quarantine': quarantine_mods,
            'untested': untested_mods
        }
        
        self.log(f"✅ Pastas criadas em: {base_path}")
        self.log("\n📝 Próximas instruções:")
        self.log("1. Copie seus mods para a pasta '[3_Mods_Nao_Testados]'")
        self.log("2. Clique em 'Carregar Próximo Lote' para começar o teste")
        self.log("3. Após testar, clique em 'Registrar Resultado'")
    
    def show_main_menu(self):
        if not self.folders:
            messagebox.showerror("Erro", "Configure as pastas primeiro!")
            return
        
        # Cria nova janela
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Menu Principal")
        menu_window.geometry("700x500")
        menu_window.minsize(600, 400)
        
        tk.Label(menu_window, text="Menu do Teste 50/50",
                font=("Arial", 16, "bold")).pack(pady=10)
        
        # Status
        status_text = self.get_status()
        status_label = tk.Label(menu_window, text=status_text,
                font=("Arial", 11), justify=tk.LEFT, bg="#e3f2fd", padx=10, pady=10)
        status_label.pack(pady=10, padx=10, fill=tk.BOTH)
        
        # Botões
        button_frame = tk.Frame(menu_window)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="📦 Carregar Próximo Lote (50/50)",
                 command=self.load_batch, width=40, height=2,
                 font=("Arial", 11), bg="#4CAF50", fg="white").pack(pady=5)
        
        tk.Button(button_frame, text="✅ Registrar Resultado do Teste",
                 command=self.record_result, width=40, height=2,
                 font=("Arial", 11), bg="#2196F3", fg="white").pack(pady=5)
        
        tk.Button(button_frame, text="🔄 Atualizar Status",
                 command=lambda: self.update_status(status_label), width=40, height=2,
                 font=("Arial", 11), bg="#FF9800", fg="white").pack(pady=5)
        
        tk.Button(button_frame, text="❌ Voltar",
                 command=menu_window.destroy, width=40, height=2,
                 font=("Arial", 11), bg="#f44336", fg="white").pack(pady=5)
    
    def update_status(self, label):
        label.config(text=self.get_status())
    
    def get_status(self):
        untested = len(self.get_mod_files(self.folders['untested']))
        active = len(self.get_mod_files(self.folders['active']))
        safe = len(self.get_mod_files(self.folders['safe']))
        quarantine = len(self.get_mod_files(self.folders['quarantine']))
        
        return (f"📊 Status Atual:\n"
                f"  📁 Mods não testados: {untested}\n"
                f"  🧪 Mods em teste: {active}\n"
                f"  ✅ Mods seguros: {safe}\n"
                f"  ⚠️  Mods em quarentena: {quarantine}")
    
    def get_mod_files(self, folder):
        if not folder.exists():
            return []
        return sorted([f for f in folder.rglob("*") if f.is_file() and not f.name.startswith(".")])
    
    def load_batch(self):
        self.log("\n🔧 Carregando próximo lote...")
        
        untested = self.get_mod_files(self.folders['untested'])
        
        if not untested:
            messagebox.showerror("Erro", "❌ Nenhum mod não testado disponível!\n\n"
                                        "Copie seus mods para a pasta:\n"
                                        "[3_Mods_Nao_Testados]")
            return
        
        mid = len(untested) // 2
        batch_a = untested[:mid]
        batch_b = untested[mid:]
        
        # Dialog para escolher lote
        result = messagebox.askquestion("Escolher Lote",
            f"📦 Lote A: {len(batch_a)} mods\n"
            f"📦 Lote B: {len(batch_b)} mods\n\n"
            f"Clique SIM para Lote A, NÃO para Lote B")
        
        batch = batch_a if result == "yes" else batch_b
        
        # Move arquivos
        self.folders['active'].mkdir(exist_ok=True)
        moved = 0
        for f in batch:
            try:
                shutil.move(str(f), str(self.folders['active'] / f.name))
                moved += 1
            except Exception as e:
                self.log(f"⚠️  Erro ao mover {f.name}: {e}")
        
        self.log(f"✅ {moved} mods carregados para teste!")
        messagebox.showinfo("Sucesso", 
            f"✅ Lote de {moved} mods pronto para teste!\n\n"
            f"📋 Instruções:\n"
            f"1. Copie os mods da pasta '[0_Ativos_Em_Teste]'\n"
            f"2. Cole no seu Mods do Sims 4\n"
            f"3. Teste o jogo\n"
            f"4. Volte e registre o resultado")
    
    def record_result(self):
        active = self.get_mod_files(self.folders['active'])
        
        if not active:
            messagebox.showerror("Erro", "❌ Nenhum mod em teste!\n\n"
                                        "Carregue um lote primeiro.")
            return
        
        result = messagebox.askquestion("Resultado do Teste",
            f"🧪 Você testou {len(active)} mods.\n\n"
            f"❓ O jogo funcionou corretamente?")
        
        dest = self.folders['safe'] if result == "yes" else self.folders['quarantine']
        dest_name = "✅ Mods Seguros" if result == "yes" else "⚠️  Quarentena"
        
        dest.mkdir(exist_ok=True)
        moved = 0
        for f in active:
            try:
                shutil.move(str(f), str(dest / f.name))
                moved += 1
            except Exception as e:
                self.log(f"⚠️  Erro ao mover {f.name}: {e}")
        
        self.log(f"✅ {moved} mods movidos para {dest_name}")
        messagebox.showinfo("Sucesso", 
            f"✅ {moved} mods registrados como {dest_name}!\n\n"
            f"Carregue o próximo lote para continuar.")

def main():
    root = tk.Tk()
    app = ModSorterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
