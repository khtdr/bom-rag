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
        print(ux.info("Running BoM-RAG setup..."))
    else:
        print(ux.info("Loading BoM-RAG..."))
    loaders.load_or_create_models()
    loaders.load_or_create_assets(options.build)

    # When a build is requested, exit before launching repl.
    if options.build:
        print(ux.info("BoM-RAG setup is complete."))
        quit()

    # Start a simple REPL to answer the user's questions.
    print(ux.info("Ready (press Ctrl+D to exit)"))
    while True:
        try:
            print(ux.prompt("wHaT iS wAnTeD?"), end="")
            query = input().strip()
            if not query:
                print(ux.info("Press Ctrl+D to exit."))
                continue

            print(ux.status("sEaRcHiNg FoR aNsWeRs..."))

            results = rag.search_results(query)

            for citation in rag.get_citations(results):
                print(ux.cite(citation))

            print(ux.status("bEaRiNg tEsTiMoNy..."))
            answers = rag.generate_answers_with_t5(query, results)
            summary = rag.generate_summarized_answer(answers)
            print(ux.answer(summary))

        except EOFError:
            print(ux.info("\nquit"))
            break


if __name__ == "__main__":
    main()
