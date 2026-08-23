import os
import re

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

def scan_solutions(base_dir="."):
    solutions = []
    
    # Percorre todas as pastas e subpastas recursivamente
    for root, dirs, files in os.walk(base_dir):
        # Ignora a pasta oculta do git
        if ".git" in root:
            continue
            
        rel_dir = os.path.relpath(root, base_dir)
        if rel_dir == ".":
            continue
            
        parts = rel_dir.split(os.sep)
        category = parts[0]
        
        for file in sorted(files):
            if file.startswith("."):
                continue
            name, ext = os.path.splitext(file)
            if ext.lower() in EXTENSIONS:
                # Tenta pegar o ID numérico pelo nome do arquivo ou pelo nome da subpasta
                match = re.search(r"(\d+)", file) or (re.search(r"(\d+)", parts[1]) if len(parts) > 1 else None)
                prob_id = match.group(1) if match else name
                
                full_rel_path = os.path.join(rel_dir, file).replace("\\", "/")
                
                solutions.append({
                    "id": prob_id,
                    "category": category,
                    "language": EXTENSIONS[ext.lower()],
                    "filename": file,
                    "rel_path": full_rel_path
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
    content.append("> Repositório contendo soluções dos problemas da plataforma [beecrowd](https://judge.beecrowd.com/).\n")
    
    content.append("## 📊 Estatísticas Gerais\n")
    content.append(f"- **Total de Problemas Resolvidos:** `{total}`\n")
    
    if lang_count:
        content.append("### 💻 Linguagens")
        for lang, count in sorted(lang_count.items(), key=lambda x: x[1], reverse=True):
            content.append(f"- **{lang}:** `{count}`")
        content.append("")
    
    if cat_count:
        content.append("### 📁 Categorias")
        for cat in sorted(cat_count.keys()):
            content.append(f"- **{cat}:** `{cat_count[cat]}`")
        content.append("")

    content.append("## 📝 Tabela de Soluções\n")
    content.append("| ID | Categoria | Linguagem | Solução | Link Beecrowd |")
    content.append("|:--:|:----------|:---------:|:-------:|:-------------:|")
    
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
    print(f"Sucesso: README.md atualizado com {total} solucoes!")

if __name__ == "__main__":
    sols = scan_solutions()
    generate_readme(sols)