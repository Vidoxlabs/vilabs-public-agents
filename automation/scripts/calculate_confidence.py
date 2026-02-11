#!/usr/bin/env python3
"""
Confidence Rating Calculator

This script calculates and updates confidence ratings for agents based on:
- Usage count
- Success rate
- Context changes
- Feedback scores

Requires Python 3.9+
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict


class ConfidenceCalculator:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)

    def calculate_confidence(self, metadata: Dict) -> float:
        """
        Calculate confidence rating based on multiple factors

        Formula:
        confidence = (success_rate * 0.4) +
                    (min(usage_count/100, 1.0) * 0.3) +
                    (effectiveness_score * 0.3)
        """
        success_rate = metadata.get("success_rate", 0) / 100.0
        usage_count = min(metadata.get("usage_count", 0) / 100.0, 1.0)
        effectiveness = metadata.get("effectiveness_score", 0)

        confidence = (success_rate * 0.4) + (usage_count * 0.3) + (effectiveness * 0.3)
        return round(confidence, 2)

    def update_agent_metadata(self, metadata_file: Path):
        """Update confidence rating in metadata file"""
        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)

            # Calculate new confidence
            old_confidence = metadata.get("confidence_rating", 0)
            new_confidence = self.calculate_confidence(metadata)

            # Update metadata
            metadata["confidence_rating"] = new_confidence
            metadata["updated"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

            # Save updated metadata
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)

            print(f"Updated {metadata_file.name}: {old_confidence:.2f} → {new_confidence:.2f}")

        except Exception as e:
            print(f"Error updating {metadata_file}: {e}")

    def process_all_agents(self):
        """Process all agent metadata files"""
        metadata_files = list(self.repo_root.rglob("metadata.json"))

        print(f"Found {len(metadata_files)} metadata files")

        for metadata_file in metadata_files:
            self.update_agent_metadata(metadata_file)

        print("\nConfidence rating update complete!")

    def generate_confidence_report(self) -> str:
        """Generate a report of all confidence ratings"""
        metadata_files = list(self.repo_root.rglob("metadata.json"))
        agents = []

        for metadata_file in metadata_files:
            try:
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                    agents.append(
                        {
                            "name": metadata.get("name", "Unknown"),
                            "confidence": metadata.get("confidence_rating", 0),
                            "effectiveness": metadata.get("effectiveness_score", 0),
                            "usage": metadata.get("usage_count", 0),
                        }
                    )
            except Exception as e:
                print(f"Error reading {metadata_file}: {e}")

        # Sort by confidence
        agents.sort(key=lambda x: x["confidence"], reverse=True)

        report = ["# Agent Confidence Ratings Report\n\n"]
        report.append("| Agent | Confidence | Effectiveness | Usage Count |\n")
        report.append("|-------|------------|---------------|-------------|\n")

        for agent in agents:
            report.append(
                f"| {agent['name']} | "
                f"{agent['confidence']:.2f} | "
                f"{agent['effectiveness']:.2f} | "
                f"{agent['usage']} |\n"
            )

        return "".join(report)


def main():
    repo_root = os.getenv("REPO_ROOT", ".")
    calculator = ConfidenceCalculator(repo_root)

    # Update all confidence ratings
    calculator.process_all_agents()

    # Generate report
    report = calculator.generate_confidence_report()
    output_file = Path(repo_root) / "docs" / "confidence-ratings.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        f.write(report)

    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()
