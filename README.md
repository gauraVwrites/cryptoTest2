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
1. Understanding the API
- Drawing requirements(for e.g., in this case I'm working with only top 10 cryptocurrencies)
- Findig a cloud solution, for hosting my postgres database.(Neon.Tech in this case)
- After analysing the API endpoints populate my dimension table with information related to Top10 cryptocurrencies.
- This marks the end of all the steps that will lead to automation part of code. Now I'll query my dimension table fetch the IDs of cryptocurrencies, store them temporarily and using another endpoint I'll populate my fact table with latest data.
- After this I'll initiate a CRON job such that this whole ETL process will occur every hour.(You can check all my actions for yourself too)
- Next I've loaded all this data to my Power BI in local machine.

