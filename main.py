import argparse
import loaders
import rag
import ux


def main():
    # Basic option parsing for a better UX experience
    parser = argparse.ArgumentParser(
        description="ThE bOoK oF mOrMoN - RAG CLI App",
        allow_abbrev=True,
        add_help=True,
        exit_on_error=True,
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build and persist the data files",
    )

    # Create models and assets.
    options = parser.parse_args()
    if options.build:
        print(ux.status("BOM-RAG running setup..."))
    loaders.load_or_create_models()
    loaders.load_or_create_assets(options.build)

    # When a build is requested, exit before launching repl.
    if options.build:
        print(ux.status("BOM-RAG setup is complete."))
        quit()

    # Start a simple REPL to answer the user's questions.
    print(ux.info("Ready (press Ctrl+D to exit)"))
    while True:
        try:
            print(ux.prompt("wHaT iS wAnTeD?"))
            query = input().strip()
            if not query:
                print(ux.info("Press Ctrl+D to exit."))
                continue

            print(ux.status("sEaRcHiNg FoR aNsWeRs..."))
            results = rag.search_results(query)
            final_answer = rag.generate_summarized_answer(
                query,
                results,
            )
            print(f"!> {final_answer}\n")
        except EOFError:
            break


if __name__ == "__main__":
    main()
