#!/usr/bin/env python3
"""
Cross-Reference Analyzer for Agent Prompts

This script analyzes agent configurations and prompts to identify:
- Overlapping functionality
- Complementary agents
- Potential conflicts
- Optimization opportunities
"""

import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import yaml


class AgentAnalyzer:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.agents = []
        self.prompts = []

    def load_agents(self):
        """Load all agent configurations"""
        agent_dirs = [self.repo_root / "agents"]

        for agent_dir in agent_dirs:
            if not agent_dir.exists():
                continue

            for agent_file in agent_dir.rglob("*.yml"):
                try:
                    with open(agent_file, "r") as f:
                        data = yaml.safe_load(f)
                        data["_path"] = str(agent_file)
                        self.agents.append(data)
                except Exception as e:
                    print(f"Error loading {agent_file}: {e}")

            for metadata_file in agent_dir.rglob("metadata.json"):
                try:
                    with open(metadata_file, "r") as f:
                        data = json.load(f)
                        data["_path"] = str(metadata_file)
                        self.agents.append(data)
                except Exception as e:
                    print(f"Error loading {metadata_file}: {e}")

    def analyze_overlaps(self) -> Dict:
        """Analyze overlapping capabilities and contexts"""
        capability_map = defaultdict(list)
        context_map = defaultdict(list)

        for agent in self.agents:
            agent_name = agent.get("name", agent.get("_path"))

            # Map capabilities
            capabilities = agent.get("capabilities", [])
            for cap in capabilities:
                capability_map[cap].append(agent_name)

            # Map contexts
            contexts = agent.get("context_compatibility", [])
            for ctx in contexts:
                context_map[ctx].append(agent_name)

        return {
            "capability_overlaps": {
                cap: agents for cap, agents in capability_map.items() if len(agents) > 1
            },
            "context_overlaps": {
                ctx: agents for ctx, agents in context_map.items() if len(agents) > 1
            },
        }

    def calculate_similarity(self, agent1: Dict, agent2: Dict) -> float:
        """Calculate similarity score between two agents"""
        score = 0.0

        # Compare capabilities
        caps1 = set(agent1.get("capabilities", []))
        caps2 = set(agent2.get("capabilities", []))
        if caps1 and caps2:
            score += len(caps1 & caps2) / len(caps1 | caps2) * 0.4

        # Compare contexts
        ctx1 = set(agent1.get("context_compatibility", []))
        ctx2 = set(agent2.get("context_compatibility", []))
        if ctx1 and ctx2:
            score += len(ctx1 & ctx2) / len(ctx1 | ctx2) * 0.3

        # Compare tags
        tags1 = set(agent1.get("tags", []))
        tags2 = set(agent2.get("tags", []))
        if tags1 and tags2:
            score += len(tags1 & tags2) / len(tags1 | tags2) * 0.3

        return score

    def find_related_agents(self, threshold: float = 0.3) -> List[tuple]:
        """Find pairs of related agents based on similarity"""
        related = []

        for i, agent1 in enumerate(self.agents):
            for agent2 in self.agents[i + 1 :]:
                similarity = self.calculate_similarity(agent1, agent2)
                if similarity >= threshold:
                    related.append(
                        (
                            agent1.get("name", agent1.get("_path")),
                            agent2.get("name", agent2.get("_path")),
                            similarity,
                        )
                    )

        return sorted(related, key=lambda x: x[2], reverse=True)

    def generate_report(self) -> str:
        """Generate a comprehensive analysis report"""
        self.load_agents()

        overlaps = self.analyze_overlaps()
        related = self.find_related_agents()

        report = ["# Agent Cross-Reference Analysis Report\n"]
        report.append(f"Total agents analyzed: {len(self.agents)}\n")

        report.append("\n## Capability Overlaps\n")
        for cap, agents in overlaps["capability_overlaps"].items():
            report.append(f"- **{cap}**: {', '.join(agents)}\n")

        report.append("\n## Context Overlaps\n")
        for ctx, agents in overlaps["context_overlaps"].items():
            report.append(f"- **{ctx}**: {', '.join(agents)}\n")

        report.append("\n## Related Agents\n")
        for agent1, agent2, similarity in related[:10]:  # Top 10
            report.append(f"- {agent1} ↔ {agent2} (similarity: {similarity:.2f})\n")

        return "".join(report)


def main():
    repo_root = os.getenv("REPO_ROOT", ".")
    analyzer = AgentAnalyzer(repo_root)

    report = analyzer.generate_report()
    print(report)

    # Save report
    output_file = Path(repo_root) / "docs" / "cross-reference-analysis.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(report)
    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()
