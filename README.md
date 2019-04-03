# Insight-PurchaseAnalytics
This project is developed in Python. As Instacart has published a [dataset](https://www.instacart.com/datasets/grocery-shopping-2017) containing 3 million Instacart orders, the purpose is to calculate, for each department, the number of times a product was requested, number of times a product was requested for the first time and a ratio of those two numbers.

# Table of Contents
1. [Problem](README.md#problem)
    1. [Input]( README.md#input )
    2. [Output]( README.md#output )
    3. [Heuristics]( README.md#heuristics )
2. [Approach]( README.md#approach )
    1. [Special Case]( README.md#special-case )
3. [Run instructions]( README.md#run-instructions)
4. [Just For Fun: The SQL Solution]( README.md#just-for-fun-the-sql-solution)
5. [Acknowledgement]( README.md#acknowledgement)


# Problem
Design a program to calculate the number of times a product was requested, number of times a product was requested for the first time and a ratio of those two numbers for each department. 
The program requires:
1. The code should be modular and reusable for future without needing to change the code;
2. The code can deal with special case like missing data;
3. Only allowed to use the default data structures that come with that programming language.

## Input
Luckly the input data(order_products.csv, products.csv) is a strict comma separated (",") format. The first row is field names. The description of the field names can be find [here](https://gist.github.com/jeremystan/c3b39d947d9b88b3ccff3147dbcf6c6b). 

## Output
The program must create 1 output file:
* `report.csv`: fieldnames: department_id, number_of_orders, number_of_first_orders, percentage

Requirements:
- It is listed in ascending order by `department_id`
- A `department_id` should be listed only if `number_of_orders` is greater than `0`
- `percentage` should be rounded to the second decimal

## Heuristics
The first thing came up my mind is "why can't I use SQL?" (lol). Imagine that order_products.csv and products.csv are two tables in database. Then we can observe that if there is a table containing four columns: order_id, product_id, reordered, department_id, it could be convenient for us to perform further calculation. Also, we can discover that the number of the record (product_id, department_id) is the number of orders for each department, while the number of the record (product_id, reordered=0, department_id) is the number of the first orders.  

Then I first think about generating a dict that contains these 4 data using two loops in python. However, you must find that this cost is high and it is extremely slow when dealing with larger input files. What's more, as the above observation, order_id is not necessary.     

**The key point is that we must find the department_id for each product_id in order_products.csv.** With this in mind, the following steps come up more clearly. With products.csv we generate a dict: {key: product_id, value: department_id}, which can be reference for the embedded dict containing the desired values: {key:department_id, value: {key: number_of_orders, value:int; key:number_of_first_orders, value:int}}. These steps are similar to the **Where** clause and **Group by** clause in SQL(e.g. `Where a.product_id = b.product_id`, `Group by department_id`).

# Approach
`purchase_analytics.py`: All the methods have been packaged in the `PurchaseAnalytics` Class: process two input files, perform calculations, generate output file. 

## Special Case
It is possible that when products.csv is missing some product_id so that these product_id can't be related to its department_id. In my solution it will generate the report.csv and calculates the unmissing values while showing the error messages for the missing product_id in terminal:
```
chenkechengdeMacBook-Pro:insight_oa kc$ ./run.sh
Cannot be found in products.csv - product_id: "45918"
Cannot be found in products.csv - product_id: "46667"
Cannot be found in products.csv - product_id: "46842"
```
You can have a try using the files in `tests/my_own_test_1` directory.

# Run Instructions
Make sure there are `./input` and `./output` directory in current directory. Pay attention to the order of the two input files, the `./input/order_products.csv` should be the first. Then run `./run.sh` in terminal.

# Just For Fun: The SQL Solution
Suppose table `order`contains `order_products.csv`'s data and table `product` contains `products.csv`'s data, each table has auto increment index as the first column.
```
Select department_id, count(product_id), sum(reordered=0), Round(sum(reordered=0)/count(product_id), 2) As Percentage
From (Select p.department_id, o.order_id, o.product_id, o.reordered
From insight.order o, product p
Where o.product_id = p.product_id) As tmp
Group by (department_id)
Order by department_id Asc;
```
# Acknowledgement
Thanks to the Insight fellowship team, I really enjoy working on this small project.
