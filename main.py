import openfoodfacts

# User-Agent is mandatory
api = openfoodfacts.API(user_agent="MyAwesomeApp/1.0")
code = "0850003560410"
product_data = api.product.get(code, fields=["code", "product_name"])
# {'code': '3017620422003', 'product_name': 'Nutella'}

print(product_data)


# pd = api.product.text_search("mineral water")
# # {"count": 3006628, "page": 1, "page_count": 20, "page_size": 20, "products": [{...}], "skip": 0}

# print(pd)
