# generate_wiki.py
import argparse
import asyncio
from src.generators.wiki_generator import WikiGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Generate GitHub wiki from Power BI PBIX file"
    )
    parser.add_argument(
        "pbix_file",
        help="Path to the PBIX file"
    )
    parser.add_argument(
        "-o", "--output",
        default="./wiki",
        help="Output directory for wiki pages (default: ./wiki)"
    )
    parser.add_argument(
        "-n", "--name",
        help="Model name (default: PBIX filename)"
    )
    
    args = parser.parse_args()
    
    generator = WikiGenerator(args.output)
    asyncio.run(generator.generate(args.pbix_file, args.name))


if __name__ == "__main__":
    main()
