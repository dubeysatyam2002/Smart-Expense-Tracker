from nlp.parser import NLPParser


def test_sentence(text: str) -> None:
    print(f"\nInput: {text}")
    parser = NLPParser()
    try:
        result = parser.parse(text)
        print("Parsed result:")
        print(f"  Type       : {result.trans_type}")
        print(f"  Amount     : {result.amount}")
        print(f"  Description: {result.description}")
        print(f"  Category   : {result.category}")
        print(f"  Date       : {result.transaction_date}")
    except Exception as e:
        print(f"  ERROR: {e}")


def main() -> None:
    samples = [
        "bought pen for 5 rupees",
        "pen 5",
        "spent 50 on milk on Dec 5",
        "got 2000 rupees salary today",
        "added Rs 500 to home account yesterday",
        "received 1000 as refund 2 days ago",
    ]

    for s in samples:
        test_sentence(s)


if __name__ == '__main__':
    main()
