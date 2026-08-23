"""
generate_readme.py
Varre as pastas de categorias do Beecrowd, identifica os arquivos de código
e regera o README.md com estatísticas e uma tabela organizada.
"""

import os
import re

# Mapeamento de extensões para Linguagens e Badges/Nomes formatados
EXTENSIONS = {
    ".c": "C",
    ".cpp": "C++",
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".cs": "C#",
    ".asm": "x86 Assembly",
    ".go": "Go",
    ".rs": "Rust",
    ".sql": "SQL"
}

# Categorias na ordem padrão do Beecrowd
CATEGORIES = [
    "1-Iniciante",
    "2-Ad-Hoc",
    "3-Strings",
    "4-Estruturas-e-Bibliotecas",
    "5-Matematica",
    "6-Paradigmas",
    "7-Grafos",
    "8-Geometria-Computacional",
    "9-SQL"
]

def scan_solutions(base_dir="."):
    solutions = []
    
    for item in os.listdir(base_dir):
        cat_path = os.path.join(base_dir, item)
        if os.path.isdir(cat_path) and not item.startswith("."):
            for file in sorted(os.listdir(cat_path)):
                if file.startswith("."):
                    continue
                name, ext = os.path.splitext(file)
                if ext.lower() in EXTENSIONS:
                    match = re.match(r"(\d+)", name)
                    prob_id = match.group(1) if match else name
                    solutions.append({
                        "id": prob_id,
                        "category": item,
                        "language": EXTENSIONS[ext.lower()],
                        "filename": file,
                        "rel_path": f"{item}/{file}"
                    })
    return solutions

def generate_readme(solutions, output_file="README.md"):
    total = len(solutions)
    lang_count = {}
    cat_count = {}
    
    for s in solutions:
        lang_count[s["language"]] = lang_count.get(s["language"], 0) + 1
        cat_count[s["category"]] = cat_count.get(s["category"], 0) + 1

    content = []
    content.append("# 🐝 Beecrowd Solutions\n")
    content.append("> Repositório automatizado contendo soluções dos problemas da plataforma [beecrowd](https://www.beecrowd.com.br/).\n")
    
    # Resumo
    content.append("## 📊 Estatísticas Gerais\n")
    content.append(f"- **Total de Problemas Resolvidos:** `{total}`\n")
    
    content.append("### 💻 Linguagens")
    for lang, count in sorted(lang_count.items(), key=lambda x: x[1], reverse=True):
        content.append(f"- **{lang}:** `{count}`")
    content.append("")
    
    content.append("### 📁 Categorias")
    for cat in sorted(cat_count.keys()):
        content.append(f"- **{cat}:** `{cat_count[cat]}`")
    content.append("")

    # Tabela
    content.append("## 📝 Tabela de Soluções\n")
    content.append("| ID | Categoria | Linguagem | Solução | Link Beecrowd |")
    content.append("|:--:|:----------|:---------:|:-------:|:-------------:|")
    
    # Ordenar por ID numérico se possível
    def sort_key(s):
        try:
            return (int(s["id"]), s["language"])
        except ValueError:
            return (999999, s["id"])

    for s in sorted(solutions, key=sort_key):
        prob_id = s["id"]
        beecrowd_link = f"[Problema {prob_id}](https://judge.beecrowd.com/pt/problems/view/{prob_id})" if prob_id.isdigit() else "-"
        sol_link = f"[{s['filename']}]({s['rel_path']})"
        content.append(f"| {prob_id} | {s['category']} | {s['language']} | {sol_link} | {beecrowd_link} |")
        
    content.append("\n---")
    content.append("*README gerado automaticamente via script Python.*")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    print(f"Sucesso: {output_file} gerado com {total} soluções encontradas!")

if __name__ == "__main__":
    sols = scan_solutions()
    generate_readme(sols)
