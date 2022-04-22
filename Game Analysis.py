from operator import index
import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("/Users/henryrichard/Documents/python/Project/vgsales.csv")

hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

region_name = {
    "NA": "North America",
    "EU": "European Union",
    "JP": "Japan",
    "Other": "Other",
    "Global": "Global"
}

def get_region_avg(region):
    north_america_sales = df['NA_Sales'].mean() * 100000
    european_union_sales = df['EU_Sales'].mean() * 100000
    japan_sales = df['JP_Sales'].mean() * 100000
    other_sales = df['Other_Sales'].mean() * 100000
    Global_Sales = df['Global_Sales'].mean() * 100000

    if region == "NA":
        
        return f"The Avg sales made in North America Region is ₹{north_america_sales:,.3f}"

    elif region == "EU":
        
        return f"The Avg sales made in North European Union Region is ₹{european_union_sales:,.3f}"

    elif region == "JP":
        
        return f"The Avg sales made in Japan is ₹{japan_sales:,.3f}"

    elif region == "Other":
        
        return f"The Avg sales made in Other Region is ₹{other_sales:,.3f}"

    elif region == "Global":
        
        return f"The Avg sales made in Global Region is ₹{Global_Sales:,.3f}"


# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.title("Video Game Sales")
st.markdown("This application is a Streamlit dashboard that can be used to analyze video game sales data")

# Fixing NULL Values
df["Year"].fillna(df["Year"].quantile(0.50),inplace = True)
df["Publisher"].fillna("Others",inplace = True)

# Selecting the Region and Finding the Avg Sales
st.subheader("Avg. Sales by Regions")
st.markdown("The following chart shows the Avg Sales by Region")
option = st.selectbox("Select a Region",["NA","EU","JP","Other","Global"])
st.info(get_region_avg(option))


# Region with Highest Avg Sales
st.subheader("Highest Avg. Sales by Regions")
st.markdown("The following chart shows the Highest Avg Sales by Region")
fig = px.bar(df,
            x=[df["Global_Sales"].mean()*100000,df["NA_Sales"].mean()*100000,df["EU_Sales"].mean()*100000,df["JP_Sales"].mean()*100000,df["Other_Sales"].mean()*100000],
            y=['Global','North America', 'Europe', 'Japan',
       'Other'], orientation='h')
fig.update_xaxes(title='Average Sales')
fig.update_yaxes(title='Region')
st.write(fig)

avg_NA = df['NA_Sales'].mean() * 100000
avg_EU = df['EU_Sales'].mean() * 100000
avg_JP = df['JP_Sales'].mean() * 100000
avg_Other = df['Other_Sales'].mean() * 100000
avg_Global = df['Global_Sales'].mean() * 100000

# write greatest avg sales
rr = [df["EU_Sales"].mean()*100000,df["NA_Sales"].mean()*100000,df["JP_Sales"].mean()*100000,df["Other_Sales"].mean()*100000,df["Global_Sales"].mean()*100000]
rr_= max(rr)
if rr.index(rr_) == 0:
    st.write("The Highest Sales is made in Europe With An Avg Of ₹" + str(round(rr_,3)))
elif rr.index(rr_) == 1:
    st.info("The Highest Sales is made in North America With An Avg Of ₹" + str(round(rr_,3)))
elif rr.index(rr_) == 2:
    st.info("The Highest Sales is made in Japan With An Avg Of ₹" + str(round(rr_,3)))
elif rr.index(rr_) == 3:
    st.info("The Highest Sales is made in Other Region With An Avg Of ₹" + str(round(rr_,3)))
elif rr.index(rr_) == 4:
    st.info("The Highest Sales is made in Global Region With An Avg Of ₹" + str(round(rr_,3)))




# Lising games by Year
st.subheader("Games list by year")
st.markdown("The following chart shows the list of games by year")
st.caption("Select a year to see the list of games")
year_selected = st.slider("Year",1980,2017)
filtered_games = pd.DataFrame(df.query(f'Year=={year_selected}', inplace=False))
filtered_games['Year'] = filtered_games['Year'].astype(int)
st.table(filtered_games[['Name','Platform','Year']])

# Lising games by Platform
st.subheader("Games list by Platform")
st.markdown("The following chart shows the list of games by Platform")
st.caption("Select a Platform to see the list of games")
platform_selected = st.selectbox("Platform",df.Platform.unique().tolist())
year_selected_platform = st.slider("Year",1980,2017,key = "year_selected_platform")
filtered_games = pd.DataFrame(df.query(f'Platform=="{platform_selected}" and Year=={year_selected_platform}', inplace=False))
filtered_games['Year'] = filtered_games['Year'].astype(int)
st.table(filtered_games[['Name','Platform','Year']])

# Lising games by Publisher
st.subheader("Games list by Publisher")
st.markdown("The following chart shows the list of games by Publisher")
st.caption("Select a Publisher to see the list of games")
publisher_selected = st.selectbox("Publisher",df.Publisher.unique().tolist())
year_selected_publisher = st.slider("Year",1980,2017,key = "year_selected_publisher")
filtered_games = pd.DataFrame(df.query(f'Publisher=="{publisher_selected}" and Year=={year_selected_publisher}', inplace=False))
filtered_games['Year'] = filtered_games['Year'].astype(int)
st.table(filtered_games[['Name','Platform','Year']])

# List top gaming consoles based on region
st.subheader("Top gaming consoles by Region")
st.markdown("The following chart shows the list of gaming consoles by Region")
st.caption("Select a Region to see the list of gaming consoles")
region_selected = st.selectbox("Region",["NA","EU","JP","Other","Global"])
consoles_na = pd.DataFrame((df.groupby("Platform")[[f"{region_selected}_Sales"]].sum()*100000).sort_values(by=[f'{region_selected}_Sales'],ascending=[False]).reset_index())

fig2 = px.bar(consoles_na,x = consoles_na[f'{region_selected}_Sales'],y = consoles_na['Platform'],orientation='h')
fig2.update_xaxes(title='Sales')
fig2.update_yaxes(title='Platform')
st.write(fig2)
st.info(f"The top gaming consoles in {region_name[region_selected]} is {consoles_na['Platform'].iloc[0]}")

# Top games based on region
st.subheader("Top 10 games by Region")
st.markdown("The following chart shows the list of games by Region")
st.caption("Select a Region to see the list of games")
region_selected = st.selectbox("Region",["NA","EU","JP","Other","Global"],key = "region_selected_games")
games_na = pd.DataFrame((df.groupby("Name")[[f"{region_selected}_Sales"]].sum()*100000).sort_values(by=[f'{region_selected}_Sales'],ascending=[False]).reset_index())
st.table(games_na.head(10))
st.info(f"The top game in {region_name[region_selected]} is {games_na['Name'].iloc[0]}")

# top gaming genres that are making high sales
st.subheader("Top gaming genres that are making high sales")
st.markdown("The following chart shows the list of genres that are making high sales")
st.caption("Select a Region to see the list of genres")
region_selected = st.selectbox("Region",["NA","EU","JP","Other","Global"],key = "region_selected_genres")
genres_na = pd.DataFrame((df.groupby("Genre")[[f"{region_selected}_Sales"]].sum()*100000).sort_values(by=[f'{region_selected}_Sales'],ascending=[False]).reset_index())
fig3 = px.bar(genres_na,x = genres_na[f'{region_selected}_Sales'],y = genres_na['Genre'],orientation='h')
fig3.update_xaxes(title='Sales')
fig3.update_yaxes(title='Genre')
st.write(fig3)
st.info(f"The top genres in {region_name[region_selected]} is {genres_na['Genre'].iloc[0]}")

# Top game publishers that are making high sales
st.subheader("Top game publishers that are making high sales")
st.markdown("The following chart shows the list of game publishers that are making high sales")
st.caption("Select a Region to see the list of game publishers")
region_selected = st.selectbox("Region",["NA","EU","JP","Other","Global"],key = "region_selected_publishers")
publishers_na = pd.DataFrame((df.groupby("Publisher")[[f"{region_selected}_Sales"]].sum()*100000).sort_values(by=[f'{region_selected}_Sales'],ascending=[False]).reset_index())
st.table(publishers_na.head(10))
st.info(f"The top publishers in {region_name[region_selected]} is {publishers_na['Publisher'].iloc[0]}")

