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
    was_empty = False
    while True:
        try:
            print(ux.prompt("wHaT iS wAnTeD?"), end="")
            query = input().strip()
            if not query:
                if was_empty:
                    break
                was_empty = True
                print(ux.info("Press Ctrl+D or Enter again to exit."))
                continue
            else:
                was_empty = False

            print(ux.status("sEaRcHiNg FoR aNsWeRs..."))
            results = rag.search_results(query)
            for citation in rag.results_citations(results):
                print(ux.cite(citation))

            print(ux.status("rEcEiViNg iNsPiRaTiOn..."))
            answers = rag.generate_answers(query, results)

            print(ux.status("bEaRiNg tEsTiMoNy..."))
            summary = rag.summarize_answers(answers, query, results)
            print(ux.cite(query), end="")
            print(ux.answer(summary))

        except EOFError:
            break
    print(ux.info("\nquit"))


if __name__ == "__main__":
    main()
