
Motivation
------------------
The impacts of Alzheimer's disease and dementia can be delayed and mitigated with early detection. 
However, there is often no method of detecting neurodegenerative diseases early, as existing
methods are generally intrusive. This project leverages natural language processing (NLP) technology,
present in products such as Alexa, to assess users' speech and alert them to take proactive
steps if they are at risk of a neurodegenerative disorder. 

Design
------------------
A. General Design
Alexa receives input from the user in the form of audio, sends the audio to the bucket, which
sends the audio to a transcriber that provides text and other features such as time stamps and
pace of speech. The transcription occurs and is passed to a machine learning algorithm, written 
in Python, within the gateway. The output is a prediction of whether the user, through their speech,
exhibits early signs of dementia. The models and training data were taken from a github repository:
https://github.com/chirag126/Automatic_Alzheimer_Detection. 


File list
------------------
main.py                File containing the main method, executes prediction
data_process.py        Parses a JSON file with transcribedtext
feature_extract.py     Extracts features from raw text 
model.py               Tests machine learning methods and deploys linear discriminant analysis
feature_set_dem.csv    Training data from subjects with and without dementia and extracted features


1. Inputs
The program takes a JSON file produced by an Amazon Web Services (AWS) voice transcription,
parses it, and passes selected attributes through a machine learning algorithm. 

2. Machine leaning methods
The machine learning model used for this program is based on code from GitHub by chirag126.
Features including the number of pauses, number of repeated words, and number of unintelligible
words in the speech sample are extracted. The model is trained on a .csv file with these 
attributes and an outcome, 0 or 1, indicate whether the subject had dementia. Our model relies 
on fewer features than the original method because transcriptions from AWS provide less information. 
In particular, they lack MMSE test results and demographic data such as age. Our model achieved
highest accuracy with linear discriminant analysis (LDA), which yields a 70% accuracy rate 
on training data. 

3. Natural language processing (NLP) 
The natural language toolkit (nlkt) from Python was used to extract grammatical features from
transcribed speech. The toolkit counts the number of verbs, the number of nouns, and the word-to-sentence
ratio in transcribed sentences, which are inputs into the linear discriminant analysis. 




