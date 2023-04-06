import re

# Función para limpiar el título y obtener el autor (entre paréntesis)
def clean_title(title):
    # Buscar paréntesis y obtener todo lo que está dentro
    author_match = re.search(r'\((.*?)\)', title)
    if author_match:
        author = author_match.group(1)
        # Eliminar paréntesis y su contenido del título
        title = re.sub(r'\(.*?\)', '', title).strip()
        return title, author
    else:
        return title, ""


with open("highlights.txt", "r", encoding="utf8") as file:
    lines = file.readlines()

highlights = {}
title = ""
content = ""

for line in lines:
    if line.startswith("- "):
        # si la línea comienza con "- ", significa que es información de ubicación y fecha, así que la ignoramos
        continue
    elif line.startswith("=========="):
        # si la línea es "==========", significa que hemos terminado un libro, así que lo agregamos a los highlights
        if title:
            # Limpiar el título y obtener el autor
            title, author = clean_title(title)
            # Agregar a los highlights
            if title in highlights:
                highlights[title]["content"] += content
            else:
                highlights[title] = {"author": author, "content": content}
        title = ""
        content = ""
    else:
        # si la línea no es información de ubicación, fecha ni "==========", entonces es parte del contenido
        if not title:
            title = line.strip()
        else:
            content += line.strip() + "\n"

# guardamos los highlights en un archivo de texto
with open("highlights_agrupados.txt", "w", encoding="utf8") as file:
    for title, data in highlights.items():
        file.write(title + "\n" + data["author"] + "\n" + data["content"] + "\n===\n")
