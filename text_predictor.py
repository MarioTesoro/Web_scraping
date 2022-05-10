import re
import json
from Model.statistics import Statistics
from scipy.special import softmax

from simpletransformers.classification import ClassificationModel, ClassificationArgs
from scipy.special import softmax
import pandas as pd

def loadModel(path, num_labels = 15, use_cuda = False):
    # Load a ClassificationModel
    model = ClassificationModel('xlnet', path, num_labels=num_labels, use_cuda=use_cuda)

    return model


def analyzeFileDebug(report_filename): # Load the result from a local file
    with open("text_prediction_results.json",encoding="utf-8") as f:
        string_prediction_array = json.load(f)
    total_strings_count = 20
    positive_strings_count = 13

    # Order the array by the value, that is the confidence index
    dict(sorted(string_prediction_array.items(), key=lambda item: item[1]))

    final_stats = Statistics()
    final_stats.writeTextOutputsToDoc(report_filename, total_strings_count, positive_strings_count, string_prediction_array)


def analyzeFile(path, model):
    # Load the test file
    new_df = pd.read_csv(path, header=0)
        # Concatenate title and description into column 'text'
        #new_df['text'] = new_df.iloc[:, 1] + " " + new_df.iloc[:, 2]
    # Take only description column
    new_df['text'] = new_df.iloc[:, 2]
    # Removed all unused columns
    new_df = new_df.drop(new_df.columns[[0, 2, 3, 4]], axis=1)
    # Convert text column to unicode
    new_df["text"] = new_df["text"].astype('unicode')
    # Remove escaped backlashes
    new_df['text'] = new_df['text'].apply(lambda x: x.replace('\\', ' '))
    # Remove extensions
    new_df['text'] = new_df['text'].apply(lambda x: x.replace(".jpg", ""))
    new_df['text'] = new_df['text'].apply(lambda x: x.replace(".JPG", ""))
    new_df['text'] = new_df['text'].apply(lambda x: x.replace(".png", ""))
    new_df['text'] = new_df['text'].apply(lambda x: x.replace(".PNG", ""))
    new_df['text'] = new_df['text'].apply(lambda x: x.replace(".jpeg", ""))
    new_df['text'] = new_df['text'].apply(lambda x: x.replace(".JPEG", ""))
    new_df['text'] = new_df['text'].apply(lambda x: x.replace(".tif", ""))
    new_df['text'] = new_df['text'].apply(lambda x: x.replace(".TIF", ""))
    new_df['text'] = new_df['text'].apply(lambda x: x.replace(".bmp", ""))
    new_df['text'] = new_df['text'].apply(lambda x: x.replace(".BMP", ""))
    new_df['text'] = new_df['text'].apply(lambda x: x.replace(".js", ""))
    new_df['text'] = new_df['text'].apply(lambda x: x.replace(".JS", ""))
    # Remove special chars
    new_df['text'] = new_df['text'].apply(lambda x: re.sub('[^A-Za-z0-9 ]+', '', x))

    # Start prediction
    string_prediction_array = dict()
    total_strings_count = 0
    positive_strings_count = 0
    current_host = new_df.iloc[0]['HOSTNAME'] #Takes the first hostname from the dataframe
    # iterate over each row
    for index, row in new_df.iterrows():
        # There is a new hostname in the file
        if row['HOSTNAME'] != current_host:
            # Export the resulting dict into a json file
            file_name = 'text_prediction_results_' + current_host + '.json'
            with open(file_name, "w",encoding="utf-8") as outfile:
                json.dump(string_prediction_array, outfile)
            # Order the array by the values, that is the confidence index
            dict(sorted(string_prediction_array.items(), key=lambda item: item[1]))
            # Print on screen the average confidence
            print('Average confidence for ' + current_host + ' = ' + str(positive_strings_count/total_strings_count))
            # Prints result into the docx report
            final_stats = Statistics()
            report_filename = current_host
            final_stats.writeTextOutputsToDoc(report_filename, total_strings_count, positive_strings_count,
                                              string_prediction_array)
            # Clears all variables related to the previous host
            string_prediction_array = dict()
            total_strings_count = 0
            positive_strings_count = 0
            current_host = row['HOSTNAME']  # updates the current hostname
        # String analysis
        string_prediction, raw_outputs = model.predict([row['text']])
        if string_prediction[0] == 14: # if the row has been classified as 14 (porn)
            # Calculate confidence
            predictions_probabilities = softmax(raw_outputs, axis=1)
            # Insert the couple string-confidence into the dict
            string_prediction_array[row['text']] = predictions_probabilities[0][14]
            positive_strings_count += 1 # Increment the positive strings count
        total_strings_count += 1 # Increment the total strings count

    # Writes the files for the last hostname
    # Export the resulting dict into a json file
    file_name = 'text_prediction_results_' + current_host + '.json'
    with open(file_name, "w",encoding="utf-8") as outfile:
        json.dump(string_prediction_array, outfile)
    # Order the array by the values, that is the confidence index
    dict(sorted(string_prediction_array.items(), key=lambda item: item[1]))
    # Print on screen the average confidence
    print('Average confidence for ' + current_host + ' = ' + str(positive_strings_count / total_strings_count))
    # Prints result into the docx report
    final_stats = Statistics()
    report_filename = current_host
    final_stats.writeTextOutputsToDoc(report_filename, total_strings_count, positive_strings_count,
                                          string_prediction_array)






        
            
            
        
        
        
        
        
