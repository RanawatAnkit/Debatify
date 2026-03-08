import os
from src.retriever import retrieve, load_index
from src.llm import generate_answer


def chat():

    print("🏛 Parliament Debate Chat Ready\n")

    date = input("Enter debate date (example 21-07-2025): ")

    folder = os.path.join("outputs", date)

    index, metadata = load_index(folder)

    while True:

        question = input("Ask: ")

        results = retrieve(question, index, metadata)

        context = ""

        for r in results:

            context += f"""
Asked By: {r['summary']['asked_by']}
Ministry: {r['summary']['ministry']}
Category: {r['summary']['category']}

Question Summary:
{r['summary']['question_summary']}

Answer Summary:
{r['summary']['answer_summary']}

---
"""

        answer = generate_answer(question, context)

        print("\n🧠 Answer:\n")
        print(answer)
        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    chat()