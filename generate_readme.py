import os
import re

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
    ".php": "PHP",
    ".sql": "SQL"
}

def scan_solutions(base_dir="."):
    problems = {}
    used_languages = set()
    
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
                used_languages.add(lang)
                
                match = re.search(r"(\d+)", file) or (re.search(r"(\d+)", parts[1]) if len(parts) > 1 else None)
                prob_id = match.group(1) if match else name
                
                full_rel_path = os.path.join(rel_dir, file).replace("\\", "/")
                
                key = (prob_id, category)
                if key not in problems:
                    problems[key] = {}
                problems[key][lang] = full_rel_path
                
    return problems, sorted(list(used_languages))

def generate_readme(problems, used_languages, output_file="README.md"):
    solved_by_cat = {}
    for (prob_id, cat) in problems.keys():
        solved_by_cat[cat] = solved_by_cat.get(cat, 0) + 1

    content = []
    content.append("# Beecrowd Solutions\n")
    content.append("> Repositório pessoal com soluções dos exercícios da plataforma [beecrowd](https://judge.beecrowd.com/).\n")
    
    content.append("## Progresso por Categoria\n")
    all_categories = sorted(list(set(list(CATEGORY_TOTALS.keys()) + list(solved_by_cat.keys()))))
    
    for cat in all_categories:
        solved = solved_by_cat.get(cat, 0)
        total = CATEGORY_TOTALS.get(cat, "?")
        cat_name = cat.split("-", 1)[1] if "-" in cat else cat
        
        if isinstance(total, int) and total > 0:
            content.append(f"- **{cat_name}:** `{solved}/{total}`")
        else:
            content.append(f"- **{cat_name}:** `{solved}` resolvidos")
            
    content.append("\n## Tabela de Soluções\n")
    
    # Se não tiver linguagens ainda, define padrão
    cols = used_languages if used_languages else ["Linguagem"]
    
    header = "| Problema | Categoria | " + " | ".join(cols) + " |"
    divider = "|:--------:|:----------|" + "|:---:" * len(cols) + "|"
    content.append(header)
    content.append(divider)
    
    def sort_key(item):
        prob_id, cat = item[0]
        try:
            return (int(prob_id), cat)
        except ValueError:
            return (999999, prob_id)

    for (prob_id, category), langs_dict in sorted(problems.items(), key=sort_key):
        cat_name = category.split("-", 1)[1] if "-" in category else category
        
        lang_cells = []
        for lang in cols:
            if lang in langs_dict:
                lang_cells.append(f"[{lang}]({langs_dict[lang]})")
            else:
                lang_cells.append(" ")
                
        row = f"| [{prob_id}](https://judge.beecrowd.com/pt/problems/view/{prob_id}) | {cat_name} | " + " | ".join(lang_cells) + " |"
        content.append(row)
        
    content.append("\n---")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
        
    print(f"Sucesso: README.md atualizado com {len(problems)} exercicios!")

if __name__ == "__main__":
    problems, used_languages = scan_solutions()
    generate_readme(problems, used_languages)