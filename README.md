# Plant cell-type-predictor
Prediciton of the annotation of plant single-cell RNAseq clusters using the markers (avlogFC) of published datasets.
Upload the text file with all marker counts and get the predicted cell type for each of your clusters according to the selected dataset.

-	Script to import the dataset of choice
-	Data preprocessing to filter the entries that are present in the reference database and pivot the table
-	Calculation of the Euclidian distance of the published clusters and the clusters of interest and assign predicted labels
-	Deploy with Streamlit
