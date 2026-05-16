import pandas as pd
df=pd.read_csv('C:/Project/Data Analyst/customer_shopping_behavior.csv')

df.head()
print(df)
print(df.info())
#print(df.describe())
print(df.describe(include='all'))
print(df.isnull().sum())

#fill the null value by each product medain value of review rating

df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x:x.fillna(x.median()))
# now check is there any null remaning
print(df.isnull().sum())

#lets change the column name patten for better use in coding change the all letter in snake case(small letter where is apce use underscotre)

df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
print(df.columns)

#create a column age_group
labels={'Young Adult','Adult','Middle-aged','Senior'}
df['age_group']=pd.qcut(df['age'],q=4,labels=labels)
print(df[['age','age_group']].head(10))

# create column purchaes_frequency_days

frequency_mapping={
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Months':90
    }
df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)
print(df[['purchase_frequency_days','frequency_of_purchases']].head(10))
print(df[['discount_applied','promo_code_used']].head(10))
#check both the cloumn are same value so we dont need promo code column because is promo code use then only discount applied
print((df['discount_applied']==df['promo_code_used']).all())

#drop promo code
df=df.drop('promo_code_used',axis=1)
print(df.columns)

#first install pip install psycopg2-binary sqlalchemy
from sqlalchemy import create_engine
#CONNECT TO POSTGRESQL
#replace placeholders with your actual deatils
username="postgres"
password="1234"
host="localhost"
port="5432"
database="customer_behavior"

engine=create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

#load Dataframe into postgresql
table_name="customer"
df.to_sql(table_name,engine,if_exists="replace",index=False)

print(f"Data sucessfully loaded into table'{table_name}' in database '{database}'.")









