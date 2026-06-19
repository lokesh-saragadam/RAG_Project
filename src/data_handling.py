import json

def load_queries(query_path):
    with open(query_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["queries"]

def query_extraction(data):
    questions = []
    for query in data:
        questions.append(query["question"])
    return questions

def save_chunks(chunks, path):
    with open(path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False))
            f.write("\n")

def load_chunks(path):
    chunks = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))

    return chunks

def print_answers(answers,sources):
    for idx,ans in enumerate(answers):
        print(f"Answer {idx+1} : {ans}")
        for id,source in enumerate(sources[idx]):
            print(f"    Source {id+1} {source[0]}.pdf Page {source[1]}")
