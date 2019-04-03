import sys
import csv

class PurchaseAnalytics:
    '''
    Analyze 3 million instacart orders.
    Calculate for each department: 1)the number of times a product was requested - number_of_orders
                                   2)the number of times a product was requested for the first time - number_of_first_orders
                                   3)percentage = 1) / 2)
    @input1: product orders
    @input2: product information
    @output: department_id, number_of_orders, number_of_first_orders, percentage

    Author and Maintainer: Kecheng Chen (chenkechengkc@gmail.com)
    '''
    def __init__(self, order_products, products):
        self.order_products = order_products
        self.products = products
        self.product_department_mapping = {}
        self.result = {}

    def create_department_mapping(self):
        '''
        Use the two input files to create a dict whose key is department_id, value is 1) & 2)
        Consider the case when product_id is not enough in products.csv
        @type name: OrderedDict
        @rtype: dict
        '''
        for dic in self.products:
            product_id = int(dic["product_id"])
            department_id = int(dic["department_id"])
            if product_id not in self.product_department_mapping:
                self.product_department_mapping[product_id] = department_id

        for d in self.order_products:
            try:
                product_id = int(d["product_id"])
                dept_id = self.product_department_mapping[product_id]
                if dept_id not in self.result:
                    self.result[dept_id] = {"number_of_orders": 0, "number_of_first_orders": 0}
                self.result[dept_id]["number_of_orders"] += 1
                if int(d["reordered"]) == 0:
                    self.result[dept_id]["number_of_first_orders"] += 1
            except KeyError as e:
                print('Cannot be found in products.csv - product_id: "%s"' % str(e))
        return self.result

def calculate_report(result, report_file):
    '''
    Calculate the percentage and output report.csv in required directory
    @param result: the dict containing required data
    @param report_file: output file path
    '''
    dept_list = sorted(list(result.keys()))
    with open(report_file, mode="w") as csv_file:
        fieldnames = ["department_id", "number_of_orders", "number_of_first_orders", "percentage"]
        report_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        report_writer.writeheader()
        for dept_id in dept_list:
            number_of_orders = result[dept_id]["number_of_orders"]
            number_of_first_orders = result[dept_id]["number_of_first_orders"]
            percentage = format(float(number_of_first_orders)/float(number_of_orders),'.2f')
            report_writer.writerow({"department_id": dept_id, "number_of_orders": number_of_orders,
                                    "number_of_first_orders": number_of_first_orders, "percentage": percentage})


if __name__ == "__main__":
    '''
    @argv[1]: ./input/order_products.csv or similar files' filepath
    @argv[2]: ./input/products.csv or similar files' filenpath
    @argv[3]: ./output/report.csv or similar files' filepath
    '''
    input_order_products = sys.argv[1]
    input_products = sys.argv[2]
    output_report = sys.argv[3]

    order_reader = csv.DictReader(open(input_order_products, mode="r"))
    products_reader = csv.DictReader(open(input_products, mode="r"))

    purchase_analytics = PurchaseAnalytics(order_reader, products_reader)
    result_dict = purchase_analytics.create_department_mapping()
    report = calculate_report(result_dict, output_report)
