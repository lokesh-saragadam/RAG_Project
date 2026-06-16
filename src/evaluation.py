import sys

Failures = ["Retrieval Failure","Generation Failure","Metadata Failure","Success"]

def evaluate_scores(queries_data,retrieved_data):

    expected_source = []
    expected_pages = []
    for data in queries_data:
        expected_source.append(data["expected_source"])
        expected_pages.append(data["expected_page"])
    
    retrieved_sources = []
    retrieved_pages = []
    for datas in retrieved_data:
        sources = []
        pages = []
        for data in datas:
            sources.append(data["source"])
            pages.append(data["page"])
        retrieved_sources.append(sources)
        retrieved_pages.append(pages)

    source_score = []
    citation_score = []
    for exp_sources,ret_sources,exp_pages,ret_pages in zip(expected_source,retrieved_sources,expected_pages,retrieved_pages):
        score_s = 0
        score_c = 0
        for source,page in zip(ret_sources,ret_pages):
            if source in exp_sources:
                score_s+=1
            if (page <= exp_pages[0]+2 and page >= exp_pages[0]-2):
                score_c+=1
            
        source_score.append(score_s/len(ret_sources))
        citation_score.append(round(score_c/len(ret_pages),3))

    return  source_score,citation_score

def decision_tree(sim_scores,source_scores,cit_scores):

    Decisions = ["" for x in sim_scores]
    for idx,score in enumerate(cit_scores):
        if(score==0):
            Decisions[idx] = Failures[0]
    for idx,score in enumerate(sim_scores):
        if(score<0.5 and Decisions[idx]==""):
            Decisions[idx] = Failures[1]
    for idx,score in enumerate(source_scores):
        if ((score < 0.5 or cit_scores[idx] < 0.2) and Decisions[idx]==""):
            Decisions[idx] = Failures[2]
    for idx,deci in enumerate(Decisions):
        if(deci == ""):
            Decisions[idx] = Failures[3]

    return Decisions