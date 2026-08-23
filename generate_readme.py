import os
import re

# Total aproximado de exercícios existentes por categoria no Beecrowd
# (Você pode ajustar os valores totais conforme desejar)
CATEGORY_TOTALS = {
    "1-Iniciante": 334,
    "2-Ad-Hoc": 750,
    "3-Strings": 280,
    "4-Estruturas-e-Bibliotecas": 210,
    "5-Matematica": 270,
    "6-Paradigmas": 220,
    "7-Grafos": 290,
    "8-Geometria-Computacional": 160,
    "9-SQL": 50
}

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
    # Estrutura: { (prob_id, category): { "Linguagem": "caminho/arquivo" } }
    problems = {}
    
    for root, dirs, files in os.walk(base_dir):
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
                lang = EXTENSIONS[ext.lower()]
                
                # Pega o ID pelo nome do arquivo ou pelo nome da subpasta
                match = re.search(r"(\d+)", file) or (re.search(r"(\d+)", parts[1]) if len(parts) > 1 else None)
                prob_id = match.group(1) if match else name
                
                full_rel_path = os.path.join(rel_dir, file).replace("\\", "/")
                
                key = (prob_id, category)
                if key not in problems:
                    problems[key] = {}
                problems[key][lang] = full_rel_path
                
    return problems

def generate_readme(problems, output_file="README.md"):
    # Contagem de problemas únicos por categoria
    solved_by_cat = {}
    for (prob_id, cat) in problems.keys():
        solved_by_cat[cat] = solved_by_cat.get(cat, 0) + 1

    total_unique_solved = len(problems)
    total_beecrowd = sum(CATEGORY_TOTALS.values())

    content = []
    content.append("# 🐝 Beecrowd Solutions\n")
    content.append("> Repositório pessoal com soluções dos exercícios da plataforma [beecrowd](https://judge.beecrowd.com/).\n")
    
    # Seção de Estatísticas por Tipo
    content.append("## 📊 Progresso por Categoria\n")
    content.append(f"**Total Geral Resolvido:** `{total_unique_solved} / {total_beecrowd}`\n")
    
    # Ordem das categorias
    all_categories = sorted(list(set(list(CATEGORY_TOTALS.keys()) + list(solved_by_cat.keys()))))
    
    for cat in all_categories:
        solved = solved_by_cat.get(cat, 0)
        total = CATEGORY_TOTALS.get(cat, "?")
        
        # Nome amigável removendo o prefixo numérico (ex: "1-Iniciante" -> "Iniciante")
        cat_name = cat.split("-", 1)[1] if "-" in cat else cat
        
        if isinstance(total, int) and total > 0:
            porcentagem = (solved / total) * 100
            content.append(f"- **{cat_name}:** `{solved}/{total}` ({porcentagem:.1f}%)")
        else:
            content.append(f"- **{cat_name}:** `{solved}` resolvidos")
            
    content.append("\n## 📝 Tabela de Soluções\n")
    content.append("| Problema | Categoria | Soluções por Linguagem | Link Beecrowd |")
    content.append("|:--------:|:----------|:-----------------------|:-------------:|")
    
    # Ordena os problemas por ID
    def sort_key(item):
        prob_id, cat = item[0]
        try:
            return (int(prob_id), cat)
        except ValueError:
            return (999999, prob_id)

    for (prob_id, category), langs_dict in sorted(problems.items(), key=sort_key):
        cat_name = category.split("-", 1)[1] if "-" in category else category
        
        # Monta os links das linguagens: [C](caminho/1000.c) | [Java](caminho/HelloWorld.java)
        lang_links = " \\| ".join([f"[{lang}]({path})" for lang, path in sorted(langs_dict.items())])
        
        beecrowd_link = f"[Problema {prob_id}](https://judge.beecrowd.com/pt/problems/view/{prob_id})" if prob_id.isdigit() else "-"
        
        content.append(f"| {prob_id} | {cat_name} | {lang_links} | {beecrowd_link} |")
        
    content.append("\n---")
    content.append("*README gerado automaticamente via script Python.*")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
        
    print(f"Sucesso: README.md atualizado com {total_unique_solved} exercicios!")

if __name__ == "__main__":
    problems = scan_solutions()
    generate_readme(problems)