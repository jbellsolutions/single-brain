#!/usr/bin/env python3
"""
Vault Knowledge Graph Analyzer — InfraNodus-style gap detection for Obsidian vaults.

Reads all .md files in the vault, builds a text co-occurrence network,
detects topic clusters and structural gaps, and outputs a report.

Usage:
    PYTHONPATH=/opt/data/home/.local/lib/python python3 vault_graph_analyzer.py [vault_path] [--output report.md]
"""

import os
import re
import sys
import json
import math
from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations

# Add local lib path
sys.path.insert(0, '/opt/data/home/.local/lib/python')

import networkx as nx
import numpy as np

# ──────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────
VAULT_PATH = os.environ.get('OBSIDIAN_VAULT_PATH', '/opt/data/obsidian-vault')
WINDOW_SIZE = 3  # Co-occurrence window (words)
MIN_WORD_LEN = 3
MIN_WORD_FREQ = 2
TOP_N_NODES = 100
STOPWORDS = set("""
the a an is are was were be been being have has had do does did will would shall should
may might can could of in to for on with at by from as into about between through after
before during without within along across behind below above over under around near upon
this that these those it its he she they them their his her we you i me my our your
not no nor neither either also very too quite rather more most less least much many few
some any all each every both another other such what which who whom where when how why
just only even still already yet again back also well then than so if but and or because
since while though although however therefore furthermore moreover nevertheless meanwhile
here there now before after where been being also very really just about into would could
should might more most other than then when where while with from that this which what
""".split())

# Domain-specific words to keep despite being common
KEEP_WORDS = set("""
api notion smartlead apify campaign leads email content pipeline vault agent
hermes slack telegram notion cron database workflow automation scrape
""".split())


def extract_words(text):
    """Extract meaningful words from text."""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remove markdown syntax
    text = re.sub(r'[#*\[\](){}|`~>_=+\-]', ' ', text)
    # Lowercase and split
    words = re.findall(r'[a-z][a-z0-9]+', text.lower())
    # Filter
    return [w for w in words if (len(w) >= MIN_WORD_LEN and (w not in STOPWORDS or w in KEEP_WORDS))]


def read_vault(vault_path):
    """Read all .md files in vault, return list of (filename, words)."""
    docs = []
    for root, dirs, files in os.walk(vault_path):
        # Skip .git
        dirs[:] = [d for d in dirs if d != '.git']
        for f in files:
            if f.endswith('.md'):
                filepath = os.path.join(root, f)
                relpath = os.path.relpath(filepath, vault_path)
                try:
                    with open(filepath, 'r') as fh:
                        text = fh.read()
                    words = extract_words(text)
                    if words:
                        docs.append((relpath, words))
                except:
                    pass
    return docs


def build_cooccurrence_graph(docs):
    """Build word co-occurrence graph from documents."""
    G = nx.Graph()
    word_freq = Counter()
    edge_freq = Counter()
    word_docs = defaultdict(set)  # Which docs contain each word

    for doc_name, words in docs:
        # Count word frequencies
        for w in words:
            word_freq[w] += 1
            word_docs[w].add(doc_name)

        # Build co-occurrence edges within sliding window
        for i in range(len(words)):
            window = words[i:i + WINDOW_SIZE]
            for w1, w2 in combinations(set(window), 2):
                if w1 != w2:
                    pair = tuple(sorted([w1, w2]))
                    edge_freq[pair] += 1

    # Filter to top words
    top_words = set(w for w, _ in word_freq.most_common(TOP_N_NODES) if word_freq[w] >= MIN_WORD_FREQ)

    # Build graph
    for word in top_words:
        G.add_node(word, freq=word_freq[word], docs=len(word_docs[word]))

    for (w1, w2), count in edge_freq.items():
        if w1 in top_words and w2 in top_words and count >= 2:
            G.add_edge(w1, w2, weight=count)

    return G, word_freq, word_docs


def detect_communities(G):
    """Detect topic communities using greedy modularity."""
    if len(G) == 0:
        return {}
    
    try:
        communities = list(nx.community.greedy_modularity_communities(G))
    except:
        communities = [set(G.nodes())]

    community_map = {}
    for i, comm in enumerate(communities):
        for node in comm:
            community_map[node] = i

    return communities, community_map


def find_structural_gaps(G, communities):
    """Find structural gaps — pairs of communities with weak connections."""
    gaps = []
    
    if len(communities) < 2:
        return gaps

    for i, comm_a in enumerate(communities):
        for j, comm_b in enumerate(communities):
            if j <= i:
                continue
            
            # Count cross-community edges
            cross_edges = 0
            possible_edges = len(comm_a) * len(comm_b)
            
            for a in comm_a:
                for b in comm_b:
                    if G.has_edge(a, b):
                        cross_edges += G[a][b].get('weight', 1)
            
            density = cross_edges / max(possible_edges, 1)
            
            if density < 0.05:  # Weak connection threshold
                # Get top words from each community by betweenness
                bc = nx.betweenness_centrality(G)
                top_a = sorted(comm_a, key=lambda x: bc.get(x, 0), reverse=True)[:5]
                top_b = sorted(comm_b, key=lambda x: bc.get(x, 0), reverse=True)[:5]
                
                gaps.append({
                    'community_a': i,
                    'community_b': j,
                    'top_a': top_a,
                    'top_b': top_b,
                    'cross_edges': cross_edges,
                    'density': density,
                    'size_a': len(comm_a),
                    'size_b': len(comm_b),
                })
    
    # Sort by weakest connection
    gaps.sort(key=lambda x: x['density'])
    return gaps


def find_bridge_nodes(G, community_map):
    """Find nodes that bridge between communities (high betweenness, cross-community edges)."""
    bc = nx.betweenness_centrality(G, weight='weight')
    bridges = []
    
    for node in G.nodes():
        if bc.get(node, 0) < 0.01:
            continue
        
        # Check if it connects to multiple communities
        neighbor_communities = set()
        for neighbor in G.neighbors(node):
            if neighbor in community_map:
                neighbor_communities.add(community_map[neighbor])
        
        if len(neighbor_communities) > 1:
            bridges.append({
                'word': node,
                'betweenness': bc[node],
                'communities': list(neighbor_communities),
                'degree': G.degree(node),
            })
    
    bridges.sort(key=lambda x: x['betweenness'], reverse=True)
    return bridges


def find_orphan_topics(docs, word_freq, word_docs):
    """Find topics that appear in only one document (potential knowledge gaps)."""
    orphans = []
    for word, doc_set in word_docs.items():
        if len(doc_set) == 1 and word_freq[word] >= 3:
            orphans.append({
                'word': word,
                'freq': word_freq[word],
                'doc': list(doc_set)[0],
            })
    orphans.sort(key=lambda x: x['freq'], reverse=True)
    return orphans[:20]


def generate_report(G, communities, community_map, gaps, bridges, orphans, docs, word_freq):
    """Generate markdown analysis report."""
    bc = nx.betweenness_centrality(G, weight='weight')
    
    report = "# Vault Knowledge Graph Analysis\n\n"
    report += f"**Generated:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M ET')}\n"
    report += f"**Vault:** `{VAULT_PATH}`\n\n"
    
    # Summary stats
    report += "## Summary\n\n"
    report += f"- **Documents analyzed:** {len(docs)}\n"
    report += f"- **Unique concepts:** {len(G.nodes())}\n"
    report += f"- **Connections:** {len(G.edges())}\n"
    report += f"- **Topic clusters:** {len(communities)}\n"
    report += f"- **Structural gaps:** {len(gaps)}\n"
    report += f"- **Bridge concepts:** {len(bridges)}\n\n"
    
    # Top concepts by influence
    report += "## Most Influential Concepts (Betweenness Centrality)\n\n"
    report += "| Concept | Centrality | Frequency | Documents |\n|---|---|---|---|\n"
    top_bc = sorted(bc.items(), key=lambda x: x[1], reverse=True)[:15]
    for word, centrality in top_bc:
        freq = word_freq.get(word, 0)
        doc_count = G.nodes[word].get('docs', 0) if word in G.nodes else 0
        report += f"| {word} | {centrality:.3f} | {freq} | {doc_count} |\n"
    report += "\n"
    
    # Topic clusters
    report += "## Topic Clusters\n\n"
    for i, comm in enumerate(communities):
        top_words = sorted(comm, key=lambda x: bc.get(x, 0), reverse=True)[:8]
        report += f"### Cluster {i+1} ({len(comm)} concepts)\n"
        report += f"**Top concepts:** {', '.join(top_words)}\n\n"
    
    # Structural gaps
    if gaps:
        report += "## 🔴 Structural Gaps (Blind Spots)\n\n"
        report += "These topic clusters are poorly connected — potential missing knowledge or unwritten SOPs.\n\n"
        for gap in gaps[:5]:
            report += f"### Gap: Cluster {gap['community_a']+1} ↔ Cluster {gap['community_b']+1}\n\n"
            report += f"- **Cluster {gap['community_a']+1} topics:** {', '.join(gap['top_a'])}\n"
            report += f"- **Cluster {gap['community_b']+1} topics:** {', '.join(gap['top_b'])}\n"
            report += f"- **Connection strength:** {gap['density']:.3f} (very weak)\n"
            report += f"- **Suggestion:** Write content connecting *{gap['top_a'][0]}* with *{gap['top_b'][0]}*\n\n"
    
    # Bridge concepts
    if bridges:
        report += "## 🌉 Bridge Concepts\n\n"
        report += "These concepts connect different topic clusters — they're your most integrative ideas.\n\n"
        report += "| Concept | Betweenness | Clusters Connected | Connections |\n|---|---|---|---|\n"
        for b in bridges[:10]:
            report += f"| {b['word']} | {b['betweenness']:.3f} | {len(b['communities'])} | {b['degree']} |\n"
        report += "\n"
    
    # Orphan topics
    if orphans:
        report += "## 🏝️ Orphan Topics (Single-Document Concepts)\n\n"
        report += "These concepts only appear in one document — consider cross-referencing them.\n\n"
        report += "| Concept | Frequency | Only In |\n|---|---|---|\n"
        for o in orphans[:15]:
            report += f"| {o['word']} | {o['freq']} | {o['doc']} |\n"
        report += "\n"
    
    # Suggestions
    report += "## 💡 Suggestions\n\n"
    if gaps:
        report += "### Missing Connections to Write\n\n"
        for i, gap in enumerate(gaps[:3], 1):
            report += f"{i}. **Connect {gap['top_a'][0]} ↔ {gap['top_b'][0]}** — "
            report += f"These {gap['size_a']}+{gap['size_b']} concepts are disconnected. "
            report += f"Consider writing an SOP or note that bridges them.\n"
        report += "\n"
    
    if orphans:
        report += "### Concepts to Cross-Reference\n\n"
        for o in orphans[:5]:
            report += f"- **{o['word']}** (in `{o['doc']}`) — mention this in at least one other document\n"
        report += "\n"
    
    return report


def main():
    vault_path = sys.argv[1] if len(sys.argv) > 1 else VAULT_PATH
    output_path = None
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        output_path = sys.argv[idx + 1]
    
    print(f"Analyzing vault: {vault_path}")
    
    # Read vault
    docs = read_vault(vault_path)
    print(f"Read {len(docs)} documents")
    
    # Build graph
    G, word_freq, word_docs = build_cooccurrence_graph(docs)
    print(f"Graph: {len(G.nodes())} nodes, {len(G.edges())} edges")
    
    # Detect communities
    communities, community_map = detect_communities(G)
    print(f"Communities: {len(communities)}")
    
    # Find gaps
    gaps = find_structural_gaps(G, communities)
    print(f"Structural gaps: {len(gaps)}")
    
    # Find bridges
    bridges = find_bridge_nodes(G, community_map)
    print(f"Bridge nodes: {len(bridges)}")
    
    # Find orphans
    orphans = find_orphan_topics(docs, word_freq, word_docs)
    print(f"Orphan topics: {len(orphans)}")
    
    # Generate report
    report = generate_report(G, communities, community_map, gaps, bridges, orphans, docs, word_freq)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"Report written to: {output_path}")
    else:
        print(report)


if __name__ == '__main__':
    main()
