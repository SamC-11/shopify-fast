# FALL 2022 SHOPIFY BACKEND DEVELOPER CHALLENGE
This is my submission for the Shopify Backend Developer Challenge. The extra feature I have chosen is the ability to create warehouses/locations and assign inventory to specific locations.

Made with FastAPI and :blue_heart: by Sam


## SETUP
**requirements: python 3.x**

**SETTING THIS UP LOCALLY**

step 1: clone this repository into your computer\
step 2: create a python virtual environment``` python -m venv env_name ```\
step 3: activate your python virtual environment ```env_name/Scripts/activate```\
step 4: install dependencies with ``` pip install -r requirements.txt ``` \
step 5: cd into the shopify-fast/src folder\
step 6: run ```uvicorn main:app --reload```. This command will start the server in debug mode\
step 7: open up your browser and navigate to localhost:8000/docs for a list of all of the endpoints fully documented by openapi\
step 8: have fun!


**SETTING THIS UP ON REPLIT**

step 1: got to my repl link\
step 2: hit run\
step 3: open the website and add /docs to the end of the url

-----

**MY APPROACH TO THIS PROBLEM**

The way I decided to handle this problem is by simplifying the system into three tables: Item, Warehouse, and Inventory.

1. The Item table is meant to keep track of all items that exist in this system. It does not keep track of their quantity or the warehouses which they are stored at.
2. The Warehouse table is meant to keep track of all warehouses that exist in this system. It does not keep track of the items in a warehouse.
3. The Inventory table is what ties everything together. It keeps track of which item and how much of it is stored at which warehouse. It is essentially a master list.

If any of this sounds confusing, maybe this will clear it up. Let's approach this problem in a more human way. We are running this logistics company and we have one purpose: move items in to, out of, and between warehouses. So what do we need for that? 

1. **Warehouses**. We need warehouses in order to store our items; pretty simple. This is where the Warehouse table comes in; the warehouse table represents all of the warehouses that we own. We can make new warehouses, delete existing ones, and even rename our facilities if we feel like it.
2. **Items**. This is how we make our $$$; we store and ship items. The Item table stores a list of the items that our company is handling. Here is an important detail: we can have items in this table which are not currently in any warehouse. The use case of this? Let's say we just talked to a company that agreed to ship us Oranges but the oranges have yet to arrive at any of our facilities.
3. **A master list**. This is a list which will keep track of which items and how much of it, is stored at which warehouse. Although the name Inventory table may sound confusing, all it is, is the master list described here.

I hope that explanation was sufficient, if not then maybe this schema will help:
![image](https://user-images.githubusercontent.com/42423169/169733732-c517c366-56cf-4ab8-a35f-55066fd0e2ba.png)

-----

**HOW TO USE THIS APPLICATION**

Using this application is pretty simple. First, follow the setup section. This will bring you to a page with a list of all of the endpoints provided by this REST API:

![image](https://user-images.githubusercontent.com/42423169/169734841-b0097109-8c0f-4aeb-ae0c-5ebb77280e75.png)

The expected arguments and return statements are all documented on this page so simply click on an endpoint and it will tell you all that you need to know to use it. For example, if we want to create a new warehouse, we simply click on the POST endpoint under WAREHOUSES: 

![image](https://user-images.githubusercontent.com/42423169/169735006-991ae635-2901-433d-b0a6-fa364a257dfb.png)

As we can see, we are shown the expected request body and the possible responses. Now let's submit a request and see the response:

![image](https://user-images.githubusercontent.com/42423169/169735139-9a6b73ca-a6b8-4f68-ab95-4302cc3e3104.png)

There are a two things we have to keep in mind when using this application:
1. You can not store items in a warehouse that does not exist
2. You can not store items which do not exist (i.e., registered in the Item table)

This application relies on these OpenAPI documentations for the UI.

-----

**QUICK DEMO**
This will be a quick demo of the application:

