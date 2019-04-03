# Insight-PurchaseAnalytics
This project is developed in Python. As Instacart has published a [dataset](https://www.instacart.com/datasets/grocery-shopping-2017) containing 3 million Instacart orders, the purpose is to calculate, for each department, the number of times a product was requested, number of times a product was requested for the first time and a ratio of those two numbers.

# Table of Contents
1. [Problem](README.md#problem)
    1. [Input]( README.md#input )
    2. [Output]( README.md#output )
    3. [Heuristics]( README.md#challenge )
2. [Approach]( README.md#approach )
    1. [Data information]( README.md#data-information )
    2. [Data prerpocessing]( README.md#data-preprocessing )
    3. [Data analysis]( README.md#data-analysis )
    4. [Performance and trade-offs]( README.md#performance-and-trade-offs )
3. [Run instructions]( README.md#run-instructions)


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
The first thing came up my mind is "why can't I use SQL?" (lol). Imagine that order_products.csv and products.csv are two tables in database. Then we can observe that if there is a table containing four columns: order_id, product_id, reordered, department_id, it could be convenient for us to perform further calculation. Also, we can discover that the number of the record (product_id, department_id) is the number of orders for each department, while the number of the record (product_id, reordered, department_id) is the number of the first orders.  

Then I first think about generating a dict that contains these 4 data using two loops in python. However, you must find that this cost is high and it is extremely slow when dealing with larger input files. What's more, as the above observation, order_id is not necessary.     

**The key point is that we must find the department_id for each product_id in order_products.csv.** With this in mind, the following steps come up more clearly. With products.csv we generate a dict: {key: product_id, value: department_id}, which can be reference for the embedded dict containing the desired values: {key:department_id, value: {key: number_of_orders, value:int; key:number_of_first_orders, value:int}}. These steps are similar to the **Where** clause and **Group by** clause in SQL(e.g. `Where a.product_id = b.product_id`, `Group by department_id`).

# Approach
`purchase_analytics.py`: All the methods have been packaged in the `PurchaseAnalytics` Class: process two input files, perform calculations, generate output file. 

## Special Case
It is possible that when products.csv is missing some product_id so that these product_id can't be related to its department_id. In my code it will generate the report.csv and calculates the unmissing values while showing the error messages for the missing product_id in terminal:
```
chenkechengdeMacBook-Pro:insight_oa kc$ ./run.sh
Cannot be found in products.csv - product_id: "45918"
Cannot be found in products.csv - product_id: "46667"
Cannot be found in products.csv - product_id: "46842"
```



## Performance and trade-offs

### Disk complexity
The program pre-processes data and save the processed data to disk. The processed data cost about 1/10 space of the raw data. The soc_map file is much small than the processed data. 
The advantages are:
1. Save time and memory: to infer the occupation name, using the processed data can help speed up x10. 
2. For further distributed analysis: both the soc_code_map and preprocessed data can be extended in distributed system safely.

### Memory complexity
The input file is read and processed line-by-line. So the largest memory consuming is the hash tables. There are about ~1k occupations, the memory cost is ~100k. And this memory cost will not increase dramatically with the statistic of input.

### Time complexity
In preprocessor, the most time consuming part is to split a line with semicolon. So the total time is O(n), n denotes the number of letters in the input file. Other operations are based on hash table with O(1) time. 

In analysis code, the time to loop all events is O(m), here m denotes the number of letters, which is about 1/10 of n. 

And sorting time is O(klogk), k is the number of states/occupation. Since k ~ 1000, no need to use heap (with O(klog10) time complexity).

# Run instructions
Make sure there are 1)`./output` directory and `./input/h1b_input.csv` in current directory. 

`sh run.sh`

# Acknowledgement
Thanks to the Insight fellowship team, this small project gave me a meaningful and happy weekend.
