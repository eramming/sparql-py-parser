from queue import Queue
import argparse
from tokens import Tokenizer, Token
from . import QueryParser, Query

def main():
    parser = argparse.ArgumentParser(prog="Sparql Py Parser",
                                     description="Builds a class-based representation of a sparql query.")
    parser.add_argument("--filepath", type=str, default="../resources/select_alerts.rq")
    parsed_args: argparse.Namespace = parser.parse_args()
    query_str: str = ""
    with open(parsed_args.filepath, "r") as f:
        query_str = f.read()
    tokenizer: Tokenizer = Tokenizer()
    tokens: Queue[Token] = tokenizer.tokenize(query_str)
    query_parser: QueryParser = QueryParser()
    sparql_query: Query = query_parser.parse(tokens)

    print(sparql_query)
    return sparql_query


if __name__ == "__main__":
    main()
