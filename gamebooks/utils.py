# gamebooks/utils.py
import re
from collections import defaultdict


def build_paragraph_graph(gamebook):
    """
    Gera um grafo com informações de conectividade entre parágrafos de um gamebook.
    """
    link_pattern = re.compile(r'\[\[paragraph:(\d+)\]\]')

    paragraphs = list(gamebook.paragraphs.all())
    existing_numbers = set(p.number for p in paragraphs)

    edges = defaultdict(list)
    all_targets = set()

    for paragraph in paragraphs:
        targets = [int(match) for match in link_pattern.findall(paragraph.text)]
        edges[paragraph.number].extend(targets)
        all_targets.update(targets)

    dead_ends = [p.number for p in paragraphs if not edges[p.number]]

    incoming_links = defaultdict(list)
    for src, targets in edges.items():
        for target in targets:
            incoming_links[target].append(src)

    orphans = [p.number for p in paragraphs if p.number not in incoming_links]

    missing_targets = sorted(all_targets - existing_numbers)

    return {
        "nodes": sorted(existing_numbers),
        "edges": {k: v for k, v in edges.items()},
        "dead_ends": sorted(dead_ends),
        "orphans": sorted(orphans),
        "missing_targets": missing_targets,
    }

def graph_to_dot(graph):
    lines = ["digraph G {"]

    # Definição de estilos por categoria
    dead_end_style = 'shape=box style=filled fillcolor="#FFDDDD"'  # Dead ends = caixa vermelha clara
    orphan_style = 'shape=ellipse style=filled fillcolor="#FFFFAA"'  # Orphans = oval amarelo claro
    missing_style = 'shape=diamond style=filled fillcolor="#CCCCCC"'  # Not yet written = losango cinza claro
    normal_style = 'shape=circle style=filled fillcolor="#DDFFDD"'  # Normal = verde claro (ajustável)

    # Primeiro, define os nós já existentes
    for node in graph["nodes"]:
        if node in graph["dead_ends"]:
            style = dead_end_style
        elif node in graph["orphans"]:
            style = orphan_style
        else:
            style = normal_style

        lines.append(f'  {node} [{style} label="{node}"];')

    # Agora os nós "missing_targets" (referenciados mas não existentes ainda)
    for missing in graph["missing_targets"]:
        lines.append(f'  missing_{missing} [{missing_style} label="{missing}"];')

    # Agora, as arestas
    for src, targets in graph["edges"].items():
        for tgt in targets:
            if tgt in graph["nodes"]:
                lines.append(f'  {src} -> {tgt};')
            else:
                lines.append(f'  {src} -> missing_{tgt};')

    lines.append("}")
    return "\n".join(lines).strip()
