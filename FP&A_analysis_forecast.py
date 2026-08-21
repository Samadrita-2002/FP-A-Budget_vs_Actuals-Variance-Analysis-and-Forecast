import pandas as pd

df = pd.read_csv("Sample - Superstore_transformed.csv", encoding="latin1")

#UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa0 in position 2969: invalid start byte
#so we needed to encode it to latin1, which can decode 0xA0 byte

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

#print(df['Order Date'].dtype) showed that python is reading as str, so we needed to transform
#dayfirst=True    since we have the date format dd-mm-yyyy

print(df['Order Date'].dtype)

# now it's datetime64[us]

print(df.isna().sum())

# this verified the excel check that there are no blank observations.

df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['YearMonth'] = df['Order Date'].dt.to_period('M').astype (str)

# This created a new column that tells me which Year-Month each transaction belongs to.

print(df.shape)
print(df.head(10))

#Now I gotta create an actuals table

actuals = df.groupby(['YearMonth', 'Year', 'Month', 'Category'], as_index=False).agg(Actual_Sales = ('Sales', 'sum'),
 Actual_Profit = ('Profit', 'sum'))

actuals.to_csv("actuals_monthly_table.csv", index=False)
print(actuals.head(5))

#Now I gotta build the budget

# Since sales can have seasonality and I don't have a company-provided budget, 
# the budget rule following standard FP&A technique is:
# This Month's budget = (Actual Sales of the same month of the prior year) * (1+ Target Growth Rate)
# In the initial version of this project, I assumed management targets 8% YoY growth across all categories.
# However, the results from that showed that a more realistic approach would be to consider 
# category-specific growth rates calculated from historical YoY growth of each category.
# So, I'm revising this following budget calculation accordingly.

annual_sales = (actuals.groupby(['Category', 'Year'], as_index= False)['Actual_Sales'].sum())

annual_sales['YoY_growth'] = (annual_sales.groupby(['Category'])['Actual_Sales'].pct_change())
print(annual_sales.head(10))
category_growth = (annual_sales.groupby('Category')['YoY_growth'].median())
print(category_growth)

# However, we see that historical median growth was 8.5% for Furniture, 33.8% for Office Supplies
# and 20.0% for Technology. Given the volatility and limited historical periods, 
# I would ultimately use moderated category-specific targets rather than directly applying 
# the historical median.

GROWTH_TARGETS = {'Furniture': 0.08,
    'Office Supplies': 0.15,
    'Technology': 0.10}

budget_rows = []
for _, row in actuals.iterrows():
    prior_year = row['Year'] - 1
    match= actuals[
        (actuals['Year'] == prior_year) &
         (actuals ['Month'] == row['Month']) &
         (actuals ['Category'] == row['Category'])]
    if not match.empty:
        growth_rate = GROWTH_TARGETS[row['Category']]
        budget_sales = match['Actual_Sales'].values[0] * (1 + growth_rate)
        budget_rows.append(
            {'YearMonth': row['YearMonth'],
            'Category' : row['Category'],
            'Budget_Sales' : budget_sales})

budget = pd.DataFrame(budget_rows)
print(budget)

#Now we will merge budget and actuals

combined = actuals.merge(budget, on=['YearMonth', 'Category'], how='inner')

#Now we perform variance analysis between actuals and budget sales

combined['Variance_Sales'] = combined['Actual_Sales'] - combined['Budget_Sales']
combined['Variance_pct'] = round((combined['Variance_Sales']/combined['Budget_Sales'])*100, 1)

combined.to_csv("budget_vs_actuals.csv", index=False)
print(combined.head(5))

#since we don't have data from 2013, 2014 doesn't have a prior year, so it dropped out of 
#the combined table. The variance analysis only contains 2015-2017

#Now we focus on forecasting the sales and profit of the next 3 months

from sklearn.linear_model import LinearRegression

monthly_category = actuals.groupby(['YearMonth', 'Category'], as_index=False)['Actual_Sales'].sum()
monthly_category['period_num'] = (monthly_category.groupby('Category').cumcount(0))

forecasts = []

for category, data in monthly_category.groupby('Category'):
    x = data[['period_num']]
    y = data['Actual_Sales']

    model = LinearRegression().fit(x,y)

    last_period = data['period_num'].max()

    for i in range(1,4):

        next_period = last_period + i

        forecast = model.predict(pd.DataFrame({'period_num': [next_period]}))[0]

        forecasts.append({'Category': category,
                          'Period': next_period,
                          'Forecast_Sales': forecast})

forecasts = pd.DataFrame(forecasts)

forecasts.to_csv("Forecast_Sales.csv", index=False)
print(forecasts.shape)
print(forecasts.head(10))


from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:thousand@localhost/fpa_analysis')
combined.to_sql('budget_vs_actuals', engine, if_exists='replace', index=False)