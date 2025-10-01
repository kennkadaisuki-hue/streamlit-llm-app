
person = {"name": "山田太郎", "age": 30, "prefecture": "東京都"}
person["job"] = "エンジニア"

for key, value in person.items():

    print(f"{key}: {value}")

# personの値をリストに格納
person_values = list(person.values())
print("personの値リスト:", person_values)