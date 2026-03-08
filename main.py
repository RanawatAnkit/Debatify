import os
from extractor.extractor import main as run_extractor
from summarizer.summarizer import main as run_summarizer
from vector.indexing import build_index


def main():

    print("\n==============================")
    print("🚀 FULL PARLIAMENT PIPELINE")
    print("==============================\n")

    pdf_path = input("Enter PDF path: ").strip()
    date = input("Enter debate date (example 21-07-2025): ").strip()

    # create output folder
    output_folder = os.path.join("outputs", date)
    os.makedirs(output_folder, exist_ok=True)

    print(f"\n📁 Output Folder Created → {output_folder}\n")

    # STEP 1
    print("🔹 STEP 1: EXTRACTION STARTING...\n")
    run_extractor(pdf_path, output_folder)

    # STEP 2
    print("\n🔹 STEP 2: SUMMARIZATION STARTING...\n")
    run_summarizer(output_folder)

    # STEP 3 Vector Index
    print("\n🔹 STEP 3: VECTOR INDEXING\n")
    build_index(output_folder)

    print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()