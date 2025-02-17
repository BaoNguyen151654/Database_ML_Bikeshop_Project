# PROJECT OUTLINE

## Building a Relational Database for a Bike Shop

**Project Executive:** [Gia Bao Nguyen (Data Scientist)](https://www.linkedin.com/in/gia-bao-nguyen-7b3aaa223/)

---

## I/ DATABASE BUILDING

### 1/ DEFINE THE GOALS

**Problem:**  
Many years ago, Bao is a dedicated bike seller, he opened his first store with a passion to become a millionaire. Because of his dedication, many customers around the world have come and experienced his bikes. At first, everything seemed easy for him, however, after opening more than 3 stores and having more than 100 loyal customers, Bao soon realizes that he cannot manage these customers just by putting all of their information into a CSV file.

- **Then he starts building a relational database, with the intention of managing his customers effectively.**
- **With this relational database, Bao also realizes that he can put everything online to create an online bike shopping platform.**

### 2/ CREATE A DATABASE WITH MYSQL

![image](https://github.com/user-attachments/assets/e4084619-9630-44a8-8000-14a6eebad35b)

*(Image: Data Model of the Database)*

- Based on the provided data model, we can create the database with available CSV files by the following DDL on MySQL (Note: DDL needs to be executed in a specific order to run successfully).

#### Step 1: Create tables that do not have foreign keys: brands, categories, stores

![Image](https://github.com/user-attachments/assets/0d29aae8-8f50-4000-8fcc-b996e5971c8f)

![Image](https://github.com/user-attachments/assets/0c839738-d196-465d-bba4-291e0f804069)

![Image](https://github.com/user-attachments/assets/92bb09fc-6501-415c-80f8-fc435fa54bd5)

#### Step 2: Create table which has foreign keys that depend on the above tables: products

![Image](https://github.com/user-attachments/assets/3f76ea03-3d98-4914-a7d4-25b071613936)

#### Step 3: Create tables that have a relationship with stores: staffs

![Image](https://github.com/user-attachments/assets/93a93379-a2a5-42a1-aac2-672c8bfaa88b)

#### Step 4: Create table that relates to orders: orders

![Image](https://github.com/user-attachments/assets/63cf307c-2124-4d45-a203-637c8ada14f1)

#### Step 5: Create tables to connect order_items and stocks: order_items, stocks

![Image](https://github.com/user-attachments/assets/56831b7b-132d-4210-adab-433e41043d73)

![Image](https://github.com/user-attachments/assets/9a4a9f93-af5a-40f6-8760-be8035fa0c5c)

- Input the CSV files into each table following this order:

  + **brands**  
  + **categories**  
  + **stores**  
  + **customers**  
  + **products**  
  + **staffs**  
  + **orders**  
  + **order_items**  
  + **stocks**

### 3/ DATA PIPELINES

![Image](https://github.com/user-attachments/assets/ac845cc7-feac-4b12-80ed-a9305b22607c)

*(Image: Data Pipelines)*

1. **Database Connection Setup**:
   - The application connects to a MySQL database named `bike_shop` using the `flask_mysqldb` extension.
   - Configuration details such as host, user, password, and port are specified to establish the connection.

2. **Data Retrieval for Display**:
   - The `index` route fetches product information from the database to display on the homepage.
   - It executes a SQL query that joins multiple tables (`products`, `brands`, `categories`, and `stocks`) to retrieve product details like name, brand, category, price, and available quantity for a specific store (`store_id = 1`).
   - The fetched data is then passed to the `index.html` template for rendering.

3. **Order Processing Pipeline**:
   - The `buy_product` route handles the purchase of a product.
   - It receives product details via a POST request in JSON format.
   - The pipeline performs several steps:
     - **Stock Availability Check**: It checks if the product is in stock by querying the `stocks` table.
     - **Price Retrieval**: It retrieves the product's price from the `products` table.
     - **Order Creation**: It inserts a new order into the `orders` table with a status of 'Pending' and the current timestamp.
     - **Order Item Addition**: It calculates the next `item_id` for the new order and inserts the product into the `order_items` table.
     - **Stock Update**: It decrements the product quantity in the `stocks` table to reflect the sale.
   - If any step fails, an error is returned. Otherwise, a success message is sent back.

4. **Data Flow**:
   - The data flows from the client (browser) to the Flask application via HTTP requests.
   - The application processes the data by interacting with the MySQL database, performing CRUD (Create, Read, Update, Delete) operations as needed.
   - The results are then sent back to the client, either as a rendered HTML page or a JSON response.

5. **Error Handling**:
   - When the quantity in the stocks table reaches 0 but the user still clicks on buy, an error message will pop up.

### 4/ DEPLOY THE DATABASE ON LOCAL SERVER WITH FLASK

- Using Flask, we can create a website that simulates the operation of an online shopping platform. It can connect to MySQL, retrieve product information, and update the database accordingly when the user clicks on buy.
- This simulation platform can only run on a local server.

---

## II/ MACHINE LEARNING

### 1/ DEFINE THE GOALS

- **Problem:** Once again, a new problem arises. Bao continuously brought in various bicycle brands, but then realized the seriousness of not understanding customer behavior. Some bike models were almost impossible to sell, causing him to struggle not knowing how to handle it. Then, Bao suddenly realized that he could leverage information from the database to understand the trends of individual customers.

**=> He decided to categorize the bike brands into 3 segments:**
- **High**: for brands with an average price greater than 1000.
- **Mid**: for brands with an average price between 500-1000.
- **Low**: for brands with an average price below 500.

**=> With machine learning, Bao can now predict which brand a customer in his list will buy next. This helps him avoid stocking items indiscriminately and anticipate customer demand.**

### 2/ QUERY THE DATABASE TO EXTRACT NEEDED FEATURES

- **Needed features:**
  + **customer_id**: Id of each customer.
  + **total_spent**: Total amount spent by a customer.
  + **latest_purchased_brand**: The brand of the bike that the customer bought in their most recent purchase.
  + **latest_brand_tier**: The tier of the bike brand the customer recently purchased.
  + **most_purchased_brand**: The brand the customer has bought the most over all purchases.
  + **latest_brand_name**: The name of the bike brand the customer recently purchased.
  + **most_purchased_brand_name**: The name of the bike brand the customer has bought the most over all purchases.

- Using the SQL script attached on **the machine learning folder on GitHub**, you can query all these features from the `bike_shop` database.

### 3/ MODEL BUILDING AND EVALUATION

- **Define features:** `latest_brand_tier` will be our target feature, others will be used as independent features.
- **Oversampling:** The data is imbalanced with only 241 tier 1 samples, we will use SMOTE to oversample class 1 to 1200 samples.

![Image](https://github.com/user-attachments/assets/6e634f38-eb80-4194-8c40-3f7c8128d361)

- **Train-test split:** 30% of the data will be used for testing.
- **Algorithm:** We will use logistic regression because our independent features all have a good correlation with the target features (based on the correlation matrix). This algorithm is also very computationally effective. Because we have a large dataset that will be updated frequently, using other algorithms such as XGBoost or Neural Networks may provide more accurate results, but they will cost us a lot of CPU.

![image](https://github.com/user-attachments/assets/660329d3-21ff-4eb8-8525-08dee54f4293)

- **Model evaluation:**

![image](https://github.com/user-attachments/assets/e3de7403-6098-4021-8760-e18c1ef50037)

  + The model has an overall accuracy of 83%.
  + The model does not perform so well with tier-1 samples, however, its performance on the other class is not that bad. To handle a large amount of data from the database, we prioritize a model that can solve the problem fast.
