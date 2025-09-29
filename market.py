

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# set page layout
st.set_page_config(
    layout='wide',
    page_title="Supermarket Sales Dashboard",
    page_icon="🛒")
# add title
st.markdown(
    """<h1 style="color:#f39c12; text-align:center;"> 🛒 Supermarket Sales Dashboard </h1>""",
     unsafe_allow_html=True)
# add image 
st.image('supermarket.png')

# load dataset
df = pd.read_csv('cleaned_Supermarket.csv', index_col = 0)
st.dataframe(df.head(5))

# create sidebar

page = (st.sidebar.radio('#_Pages_:-', ['Dataset Overview', 'Uni-Variate Analysis', 'Bi-Variate Analysis', 'Multi-Variate Analysis']))

if page == 'Dataset Overview':

    """  
        📄 Dataset Overview:
        
    This dataset records transactional data from a supermarket, capturing sales, customer demographics, product details, and financial metrics.

        🔢 Size & Structure
    Rows: ~1,000 transactions
    Columns: 17 features including IDs, categories, prices, quantities, dates, times, and ratings

        📌 Key Columns & Descriptions
    Column	Description
    * Invoice ID	: Unique identifier for each transaction
    * Branch, City	: Store branch and its corresponding city
    * Customer type	: Indicates if a customer is a "Member" or "Normal"
    * Gender	: Male or Female
    * Product line	: One of 6 product categories (e.g., Food, Fashion)
    * Unit price, Quantity	: Price per item and number of items bought
    * Sales	: Total amount paid including tax
    * Tax 5%, cogs	: Calculated fields based on sales
    * gross income	: Profit from the transaction
    * Payment	: Payment method (Cash, Credit card, Ewallet)
    * Date, Time	: Date and time of purchase
    * Rating	: Customer feedback (scale 1–10)

        📊 General Insights
        🏬 Branches & Cities
    There are 3 branches in 3 cities: Yangon, Naypyitaw, and Mandalay

    Naypyitaw (Giza branch) shows the highest total and average sales

        👥 Customer Demographics
    Balanced distribution across Gender and Customer Type

    Both genders and customer types contribute evenly to revenue

        🛒 Product Line Analysis
    Six distinct product lines

    Product lines vary significantly in average sales and ratings

        💵 Sales & Revenue
    Sales = Unit Price × Quantity + 5% Tax

    Most transactions fall within moderate price and quantity ranges

    Gross income is directly tied to the size of each transaction

        ⏰ Time & Date
    Sales happen throughout the day; peak times can be explored

    Transactions cover multiple months — useful for trend analysis

        🔀 Strengths for Analysis
    Good variety of categorical and numerical variables

    Perfect for univariate, bivariate, and multivariate analysis

    Ideal for use cases such as:

    * Sales forecasting

    * Customer segmentation

    * Product line profitability

    * Branch performance comparisons
    """
    # About Me Section
    st.markdown("---")
    st.markdown("### 👨‍💻 About the Developer")
    st.markdown("""
                - **Name:** Ahmed Saif 
                - **GitHub:** [github.com/Saif900121](https://github.com/Saif900121)  
                - **LinkedIn:** [linkedin.com/in/aahmed-saif-1bb820192](https://www.linkedin.com/in/ahmed-saif-1bb820192/)  
                - **Email:** [drahmed.saif90@gmail.com](mailto:drahmed.saif90@gmail.com)
                """)
elif page == 'Uni-Variate Analysis':

    tab_1, tab_2 = st.tabs(['Numerical Univariat Analysis', 'Categorical Univariate Analysis'])

    col_num = tab_1.selectbox('Select Numerical Column', df.select_dtypes(include= 'number').columns)
    col_cat = tab_2.selectbox('Select Categorical Column', df.select_dtypes(include= 'object').columns)
    chart_num = tab_1.selectbox('Select Chart', ['Histogram', 'Box'])
    chart_cat = tab_2.selectbox('Select Chart', ['Histogram', 'Pie'])

    if chart_num == 'Histogram':
        tab_1.plotly_chart(px.histogram(data_frame= df, x= col_num, title= col_num))

    elif chart_num == 'Box':
        tab_1.plotly_chart(px.box(data_frame= df, y= col_num, title= col_num))

    if chart_cat == 'Histogram':
        tab_2.plotly_chart(px.histogram(data_frame= df, x= col_cat, title= col_cat))

    elif chart_cat == 'Pie':
        tab_2.plotly_chart(px.pie(data_frame= df, names= col_cat, title= col_cat))
    
    start_date = st.sidebar.date_input('Start Date', value= df.date.min(), min_value= df.date.min(), max_value= df.date.max())
    end_date = st.sidebar.date_input('End Date', value= df.date.max(), min_value= df.date.min(), max_value= df.date.max())
    city = st.sidebar.multiselect('City', df.city.unique())
    top_n = st.sidebar.slider('Top N', min_value = 1, max_value = 10)

    df_filtered = df[(df.date >= str(start_date)) & (df.date <= str(end_date))] 
    df_filtered = df_filtered[(df_filtered.city.isin(city))]
    
    st.dataframe(df_filtered)
    product_count = df_filtered.product_line.value_counts().head(top_n).reset_index()

    st.markdown(
    f"""<h1 style="color:#f39c12; text-align:center;"> Top {top_n} Popular Products </h1>""",
     unsafe_allow_html=True)
    st.plotly_chart(px.bar(product_count, x = 'product line', y = 'count'))

elif page == 'Bi-Variate Analysis':
    st.header('Does customer type (Member vs. Normal) affect total sales or gross income?')
    sales_per_type = df.groupby('customer type')['sales'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame= sales_per_type, x = 'customer type', y= 'sales', text_auto= True,
       labels= {'sales': 'Total sales', }))
    income_per_type = df.groupby('customer type')['gross income'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame= income_per_type, x = 'customer type', y= 'gross income', text_auto= True,
       labels= {'gross income': 'Total gross income', }))
    
    st.header('Is there a difference in sales between male and female customers?')
    sales_per_gender = df.groupby('gender')['sales'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame= sales_per_gender, x = 'gender', y= 'sales', text_auto= True,
       labels= {'sales': 'Total sales', 'gender':'Gender'}))
    st.header('Which product line has the highest Total gross income?')
    total_income_per_product = df.groupby('product line')['gross income'].sum().sort_values(ascending=False).reset_index()
    st.plotly_chart(px.bar(data_frame= total_income_per_product, x= 'product line', y= 'gross income', text_auto= True))

elif page == 'Multi-Variate Analysis':
    st.header('What combination of Month, payment method, and product line leads to the total gross income?')
    income_per_month = df.groupby(['month', 'payment', 'product line'])['gross income'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame= income_per_month, x= 'month', y= 'gross income', color= 'product line',facet_col= 'payment', 
       barmode= 'group'))

    st.header('What combination of city, payment method, and product line leads to the total gross income?')
    income_per_line = df.groupby(['city', 'payment', 'product line'])['gross income'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame= income_per_line, x= 'product line', y= 'gross income', color= 'payment',facet_col= 'city', 
       barmode= 'group'))
