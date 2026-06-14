import sys

def evaluate_source_score(queries_data,retrieved_data):

    expected_source = []
    for data in queries_data:
        expected_source.append(data["expected_source"])
    
    retrieved_sources = []
    for datas in retrieved_data:
        sources = []
        for data in datas:
            sources.append(data["source"])
        retrieved_sources.append(sources)

    query_score = []
    sum_score = 0
    for exp_sources,ret_source in zip(expected_source,retrieved_sources):
        score = 0
        for source in ret_source:
            if source in exp_sources:
                score+=1
        query_score.append(score/len(ret_source))
        sum_score+=query_score[-1]
    
    print("Average query source score is ",sum_score/len(query_score))

    return  query_score

