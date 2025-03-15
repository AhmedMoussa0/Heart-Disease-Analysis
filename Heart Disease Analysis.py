import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout = 'wide', page_title = 'Heart Disease Analysis Dashboard')
st.title("Heart Disease Analysis Dashboard")
tab1,tab2,tab3=st.tabs (['Data exploration','Data analysis','Data visualization'])

with tab1:
    st.text(" Here’s a brief explanation of the columns:\n\
                  *   age: Age of the patient (in years).\n\
                  * sex: Gender of the patient (1 = male, 0 = female).\n\
                  * cp: Chest pain type (0 = typical angina, 1 = atypical angina,\n\
                         2 = non-anginal pain, 3 = asymptomatic).\n\
                  * trestbps: Resting blood pressure (in mm Hg).\n\
                  * chol: Serum cholesterol level (in mg/dL).\n\
                  * fbs: Fasting blood sugar > 120 mg/dL (1 = true, 0 = false).\n\
                  * restecg: Resting electrocardiographic results (0 = normal, \n\
                        1 =  ST-T wave abnormality, 2 = left ventricular hypertrophy).\n\
                  * thalach: Maximum heart rate achieved during exercise.\n\
                  * exang: Exercise-induced angina (1 = yes, 0 = no).\n\
                  * oldpeak: ST depression induced by exercise relative to rest.\n\
                  * slope: Slope of the peak exercise ST segment (0 = upsloping, \n\
                  1 = flat, 2 = downsloping).\n\
                  * ca: Number of major vessels (0-3) colored by fluoroscopy.\n\
                  * thal: Thalassemia (1 = normal, 2 = fixed defect, 3 = reversible defect).\n\
                 * target: Presence of heart disease (0 = no disease, 1 = disease)?.")
    df = pd.read_excel('heart_clean.xlsx')
    st.latex(r'''\text{numerical Descriptive Statistics}''')
    basic_statistics_category=df.describe(include='O').T
    st.table(df.describe().T)
    st.latex(r'''\text{Descriptive Statistics for Categorical Columns}''')
    st.table(basic_statistics_category)
      
with tab3:
    col1, col2  = st.columns(2)
    
    with col1:
       target_counts = df['target'].value_counts()
       fig1= px.bar(target_counts, x=target_counts.index, y=target_counts.values,
             labels={'x': 'Target', 'y': 'Count'},
             title='Distribution of Target Variable',
             color=target_counts.index,
             color_discrete_map={0: 'green', 1: 'red'},height=700,width=500)
       st.plotly_chart(fig1, use_container_width=True)
       fig2 = px.scatter(df, x='age', y='chol', color='target',
                 title='Age vs. Cholesterol',
                 labels={'age': 'Age', 'chol': 'Cholesterol'},
                 marginal_x='histogram',marginal_y='box',height=1000,width=1000)
       st.plotly_chart(fig2, use_container_width=True)
       df_sorted_ascending = df.sort_values(by='age', inplace=True)
       age_labels = ['20-30', '30-40', '40-50', '50-60', '60-70', '70-80']  
       bins=[20,30,40,50,60,70,80]
       df['age_group'] = pd.cut(df['age'], bins=bins, labels=age_labels)
       fig3 = px.histogram(df, x='age_group', color='target', barmode='group',
                   title='Age Distribution by Gender',
                   labels={'age_group': 'Age Group', 'sex': 'Gender'})
       st.plotly_chart(fig3, use_container_width=True)
    with col2:
      fig1 = px.histogram(df, x='age', nbins=20,
                   title='Age Distribution',
                   labels={'age': 'Age'},
                   color="sex",height=700,width=700)
      st.plotly_chart(fig1, use_container_width=True)
      fig2=px.imshow(df.select_dtypes(include=np.number).corr().round(2), height=700, width=800,text_auto=True)  
      st.plotly_chart(fig2, use_container_width=True)
      fig3 = px.scatter_matrix(df, dimensions=['age', 'trestbps', 'chol', 'thalach'],
                        color='target',
                        title='Pair Plot of Selected Features')
      st.plotly_chart(fig3, use_container_width=True)
