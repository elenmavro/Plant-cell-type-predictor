from random import choices  
import streamlit as st
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import base64

# background image code beggining --- doesnt work in the latest version of streamlit
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        picture = f.read()
    return base64.b64encode(picture).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('susan-wilkinson-niupLEsCLew-unsplashD.png')
# background image code end


st.title('Plant cell-type predictor')


# reference datasets
moreno=pd.read_csv('data/moreno_data.csv')
wang=pd.read_csv('data/wang_data.csv')
timmermans=pd.read_csv('data/timmermans_data.csv')
kragler=pd.read_csv('data/kragler_data.csv')
derybel=pd.read_csv('data/derybel_data.csv')
liu_stomata=pd.read_csv('data/liu_leaf_data.csv')
kragler_eden=pd.read_csv('data/kragler_eden_data.csv')
kragler_ed=pd.read_csv('data/kragler_ed_data.csv')
kragler_en=pd.read_csv('data/kragler_en_data.csv')


# urls
url_wang='https://www.cell.com/molecular-plant/fulltext/S1674-2052(19)30133-9?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS1674205219301339%3Fshowall%3Dtrue'
url_timmermans='https://www.cell.com/developmental-cell/fulltext/S1534-5807(19)30145-5?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS1534580719301455%3Fshowall%3Dtrue'
url_moreno='https://www.cell.com/molecular-plant/fulltext/S1674-2052(21)00189-1?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS1674205221001891%3Fshowall%3Dtrue'
url_kragler='https://academic.oup.com/plphys/article/188/2/861/6432046'
url_derybel='https://www.science.org/doi/10.1126/science.aay4970'
url_liu='https://www.sciencedirect.com/science/article/pii/S167420522030188X#mmc2'

# classifier used for the prediction
classifier = KNeighborsClassifier(algorithm='auto', metric='cosine', n_neighbors = 1)

# predict the annotation
def annotate(dataset, query, url):
    y_train= dataset.iloc[:,0]
    X_train_dataset= dataset.iloc[:, 1:]
    X_test= query[query.columns.intersection(X_train_dataset.columns)]
    X_train= X_train_dataset[query.columns.intersection(X_train_dataset.columns)]
    classifier.fit(X_train, y_train)
    prediction= pd.DataFrame(zip(query.iloc[:,0], classifier.predict(X_test)), columns = ['Cluster', 'Predicted cell type'])
    return st.subheader(f'Cell-type prediction according to [{choice}] (%s):' % url), st.dataframe(prediction)

# upload test data = your query
data_file = st.file_uploader('Upload your Data', type=['csv', 'txt', 'xls'])
def data_reshape(data):
    data1 = data[['ID', 'avg_logFC', 'cluster']]
    data2 = data1.pivot(index='cluster', columns='ID', values='avg_logFC' )
    data3 = data2.reset_index(level='cluster')
    data4 = data3.fillna(0)
    return data4



choices= ['Zhang et al., 2019 (Root)', 'Deneyer et al., 2019 (Root)', 'Serrano-Ron et al., 2021 (Lateral roots)', 'Apelt et al., 2022 (Root)', 'Wendrich et al., 2020 (Root tip)', 'Liu et al., 2020 (Cotyledon Stomata)', 'Apelt et al., 2022 (Leaf EDEN)', 'Apelt et al., 2022 (Leaf ED)', 'Apelt et al., 2022 (Leaf EN)']
choice=st.selectbox('Select reference dataset', choices)

if data_file is not None:
    
    data=pd.read_csv(data_file, sep='	')
    query=data_reshape(data)
    

    if choice == 'Zhang et al., 2019 (Root)':
        annotate(dataset=wang, query=query, url=url_wang)

    elif choice == 'Deneyer et al., 2019 (Root)':
        annotate(dataset=timmermans, query=query, url=url_timmermans)
        
    elif choice == 'Serrano-Ron et al., 2021 (Lateral roots)':
        annotate(dataset=moreno, query=query, url=url_moreno)
       
    elif choice == 'Apelt et al., 2022 (Root)':
        annotate(dataset=kragler, query=query, url=url_kragler)

    elif choice == 'Wendrich et al., 2020 (Root tip)':
        annotate(dataset=derybel, query=query, url=url_derybel)

    elif choice == 'Liu et al., 2020 (Cotyledon Stomata)':
        annotate(dataset=liu_stomata, query=query, url=url_liu)

    elif choice == 'Apelt et al., 2022 (Leaf EDEN)':
        annotate(dataset=kragler_eden, query=query, url=url_kragler)

    elif choice == 'Apelt et al., 2022 (Leaf EDE)':
        annotate(dataset=kragler_ed, query=query, url=url_kragler)

    elif choice == 'Apelt et al., 2022 (Leaf EN)':
        annotate(dataset=kragler_en, query=query, url=url_kragler)
        
else:
    pass
