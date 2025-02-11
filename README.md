# CRYPTO_INFO_ETL
## Runs every hour<br>
#
**Purpose**
- To strengthen my ETL skills using some real world data, creating a pipeline that is fully automatic and hosted in cloud environments.
- To enhance or challenge my skillset through trying new things.
#
**Dataset**
- In this project I've not worked on any kind of pre-existing dataset.
- In fact I've created my own database, and structure my tables accordingly, that suits my needs and are future proof.
- I've only considered top 10 cryptocurrencies that too on 1st Feb. There are two tables in my database.
- The Top 10 Table acts as a Dimension Table and the other table works as Main Table.
#
### **Methodology**
#
**Tools, Languages and Libraries used**
- Python
- Requests
- sqlalchemy
- psycopg2
- postgresql
- github Actions
- Power BI
#
**Workflow**
#
![](https://github.com/gauraVwrites/cryptoTest2_ETL/blob/main/images/Screenshot%202025-02-11%20163021.png)<br>
#
To have a successful automation for our ETL pipeline, I had to perform few things beforehand so that automation runs without any fail. These tasks were:
1. Understanding the API<br>
In this particular project I've used only 2 endpoints to complete my requirements.<br>
The first one would be to get the top 10 cryptocurrencies. For that I've used CoinMarketCap ID Map and in my query I've sorted results on the basis of CMC rank and set my result to the limit of 10.<br>
This particular endpoint goes like this https://pro-api.coinmarketcap.com/v1/cryptocurrency/map<br>
Now from here I'll store my results that is basically the sorted IDs of top 10 cryptocurrencies on the basis of CMC rank.<br>
Now my first requirement is to fill up my dimension table for that I'll use the retureived IDs on some other endpoint to fetch data around those cryptocurrencies.<br>
For successful creation of my dimension table I'll use this particular endpoint: https://pro-api.coinmarketcap.com/v2/cryptocurrency/info<br>
This will require an ID parameter and for each ID this will return data like:<br>
Logo, Name, Symbol, Category, Tags, etc.<br>
Later on I'll convert all of this into a postgres table.<br>
Now I'll use some other endpoint that will help me fetch data like the current price, current market valuation, and the timestamp when the data was refreshed for this cryptocurrency.<br>
This particular endpoint is used to achieve the desired result. https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest<br>
2. Setting up the Cloud Environment<br>
Now that I've my code ready it's time to setup my postgres table in a cloud environment so that it can run irrespective of my local machine status.<br>
For that purpose I'll be using Neon.Tech. This cloud service provides free cloud hosting of Postgres database upto some limited amount.<br>
3. Creating tables<br>
After setting up my database on cloud, I'll use the credentials of my cloud server, to establish a connection between database and my local machine frome where I'll be running my python code.<br>
For the creation purpose, and populating my tables, I've mostly used sqlalchemy's ORM feature, but in order to query my database I've used psycopg2. More of that in code part.<br>
4. Code workflow<br>
After setting up my cloud and creating and populating my dimension table with top 10 cryptocurrencies.<br>
I'll comment out that particular part from my code, and query my dim. table to fetch the IDs of these cryptocurrencies and then these IDs will be used to make further API calls in to my last endpoint to fetch latest price etc.<br>
After that I'll insert this data into the new fact table. Because I want to compare the price of cryptocurrencies during different times I'll keep stacking my Fact table.<br>
Both of my table will have an incrementing column, in case we encounter some kind of problem with my tables.<br>
5. Automation<br>
I'll use GitHub actions for scheduling my CRON jobs, which will run my Python code at start of each hour. Making it a total of 24 workflows in a day.<br>
Now my whole process is automated as of now I've crossed the mark of 100 successful workflows, without running into any kind of error so far. You can check my total actions for yourself.<br>


