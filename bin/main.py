import argparse
import pandas as pd
from rdkit import DataStructs

from predictor import similarity_softmax_bioactivity_predictor
import scorer
import fingerprinter

def similarity_activity_predictor(known_dataset_csv, predict_csv, output_path_csv, fingerprint_type, similarity_function, scoring):
    """
    Predicts bioactivity based on chemical similarity.
    """
    known_df = pd.read_csv(known_dataset_csv)
    predict_df = pd.read_csv(predict_csv)

    scorers = {
        "max": scorer.max_similarity_scorer,
        "mean": scorer.mean_similarity_scorer,
        "upper_cuartile": scorer.upper_cuartile_scorer,
        "upper_decile": scorer.upper_decile_scorer
    }

    fingerprinters = {
        "RDKIT": fingerprinter.fingerprint_generator_rdkit,
        "LSTAR": fingerprinter.fingerprint_generator_LSTAR,
        "ASP": fingerprinter.fingerprint_generator_ASP,
        "RAD2D": fingerprinter.fingerprint_generator_RAD2D
    }

    similarity_functions = {
        "BraunBlanquet": DataStructs.BraunBlanquetSimilarity,
        "Tanimoto": DataStructs.TanimotoSimilarity,
        "Cosine": DataStructs.CosineSimilarity
    }

    if fingerprint_type not in fingerprinters:
        raise ValueError(f"Invalid fingerprint type: {fingerprint_type}. Choose from {list(fingerprinters.keys())}.")
    
    if similarity_function not in similarity_functions:
        raise ValueError(f"Invalid similarity function: {similarity_function}. Choose from {list(similarity_functions.keys())}.")
    
    if scoring not in scorers:
        raise ValueError(f"Invalid scoring method: {scoring}. Choose from {list(scorers.keys())}.")
    
    prediction_result = similarity_softmax_bioactivity_predictor(
        known_df,
        predict_df,
        scorers[scoring],
        fingerprinters[fingerprint_type],
        similarity_functions[similarity_function]
    )
    
    cols = predict_df.columns.to_list()
    cols.append("prediction_score")
    prediction_result = prediction_result[cols].reset_index(drop=True)
    
    prediction_result.to_csv(output_path_csv, index=False)
    print(f"Predictions saved to {output_path_csv}")

def main():
    parser = argparse.ArgumentParser(
        description="Predict bioactivity using chemical similarity measures."
    )
    
    parser.add_argument("--known_dataset_csv", required=True, help="Path to known dataset CSV file.")
    parser.add_argument("--predict_csv", required=True, help="Path to prediction dataset CSV file.")
    parser.add_argument("--output_path_csv", required=True, help="Path to output CSV file.")
    parser.add_argument("--fingerprint_type", default="ASP",choices=["RDKIT", "LSTAR", "ASP", "RAD2D"],
                        help="Type of fingerprint to use.")
    parser.add_argument("--similarity_function", default="BraunBlanquet",choices=["BraunBlanquet", "Tanimoto", "Cosine"],
                        help="Similarity function to use.")
    parser.add_argument("--scoring", default="max",choices=["max", "mean", "upper_cuartile", "upper_decile"],
                        help="Scoring method to use.")
    
    args = parser.parse_args()
    
    similarity_activity_predictor(
        args.known_dataset_csv,
        args.predict_csv,
        args.output_path_csv,
        args.fingerprint_type,
        args.similarity_function,
        args.scoring
    )

if __name__ == "__main__":
    main()
