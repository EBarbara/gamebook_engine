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