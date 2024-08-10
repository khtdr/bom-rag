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
    loaders.load_or_create_models()
    loaders.load_or_create_assets(options.build)

    # When a build is requested, exit before launching repl.
    if options.build:
        ux.status("BOM-RAG setup is complete")
        quit()

    # Start a simple REPL to answer the user's questions.
    ux.info("Ready (press Ctrl+D to exit)")
    while True:
        try:
            query = ux.prompt("wHaT iS wAnTeD?")
            if not query:
                ux.info("Press Ctrl+D to exit.")
                continue

            ux.status("sEaRcHiNg FoR aNsWeRs...")
            results = rag.search_results(query)
            final_answer = rag.generate_summarized_answer(
                query,
                results,
            )
            print(f"!> {final_answer}\n")
        except EOFError:
            ux.info("uNtIl We mEeT aGaIn")
            break


if __name__ == "__main__":
    main()
