import pandas as pd
from scipy.special import softmax
from rdkit import DataStructs


def similarity_softmax_bioactivity_predictor(dataset_train:pd.DataFrame,dataset_predict:pd.DataFrame,similarity_scorer,fps_generator,similarity_function:DataStructs):
    predict_output = dataset_predict.copy()
    predict_output = predict_output.reset_index(drop=True)

    train_positives = dataset_train[dataset_train.bioactivity == 1]
    train_positives = train_positives.reset_index(drop=True)

    train_negatives = dataset_train[dataset_train.bioactivity == 0]
    train_negatives = train_negatives.reset_index(drop=True)

    predict_output["positive_comps_similarity"] = calculate_similiarity_scores(predict_output,train_positives,similarity_scorer,fps_generator,similarity_function)["pred_score"]
    predict_output["negative_comps_similarity"] = calculate_similiarity_scores(predict_output,train_negatives,similarity_scorer,fps_generator,similarity_function)["pred_score"]

    predict_output[["prediction_score","negative_prediction_score"]] = softmax(predict_output[["positive_comps_similarity","negative_comps_similarity"]],axis=1)

    return predict_output

def calculate_similiarity_scores(similarity_of:pd.DataFrame, similarity_to:pd.DataFrame, scorer, fingerprinter, similarity_func, smiles_column = "smiles"):

    similarity_of_internal = similarity_of.copy()
    similarity_of_internal = similarity_of_internal.reset_index(drop=True)
    similarity_of_internal = fingerprinter(similarity_of_internal)
    similarity_of_internal = similarity_of_internal.reset_index(drop=True)


    similarity_to_internal = similarity_to.copy()
    similarity_to_internal = similarity_to_internal.reset_index(drop=True)
    similarity_to_internal = fingerprinter(similarity_to_internal)
    similarity_to_internal = similarity_to_internal.reset_index(drop=True)


    similarity_of_internal.loc[:,"pred_score"] = similarity_of_internal.loc[:,"fps"].apply(lambda x: scorer(x,similarity_to_internal["fps"],labels=similarity_to_internal["bioactivity"], similarity = similarity_func))
    
    return similarity_of_internal[similarity_of.columns.to_list()+["pred_score"]]