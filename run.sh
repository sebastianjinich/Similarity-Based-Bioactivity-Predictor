docker run -it\
    --mount type=bind,src=./data,dst=/root/similarity_activity_predictor/data\
    --mount type=bind,src=./predictions,dst=/root/similarity_activity_predictor/predictions\
    sebastianjinich/similarity_activity_predictor:04\
        --known_dataset_csv data/train_data_example.csv\
        --predict_csv data/predict_data_example.csv\
        --output_path_csv predictions/prediction_example.csv\
