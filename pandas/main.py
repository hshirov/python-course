import pandas as pd

users = [
    {'name': 'John Doe', 'email': 'john.doe@example.com', 'age': 42},
    {'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'age': 35},
    {'name': 'Alice Johnson', 'email': 'alice.johnson@example.com', 'age': 29},
    {'name': 'Michael Brown', 'email': 'michael.brown@example.com', 'age': 54},
    {'name': 'Linda Davis', 'email': 'linda.davis@example.com', 'age': 47},
    {'name': 'William Wilson', 'email': 'william.wilson@example.com', 'age': 31},
    {'name': 'Barbara Miller', 'email': 'barbara.miller@example.com', 'age': 20},
    {'name': 'James Anderson', 'email': 'james.anderson@example.com', 'age': 27},
    {'name': 'Patricia Thomas', 'email': 'patricia.thomas@example.com', 'age': 43},
    {'name': 'Robert Jackson', 'email': 'robert.jackson@example.com', 'age': 59},
    {'name': 'Jennifer White', 'email': 'jennifer.white@example.com', 'age': 24},
    {'name': 'Charles Harris', 'email': 'charles.harris@example.com', 'age': 62},
    {'name': 'Elizabeth Martin', 'email': 'elizabeth.martin@example.com', 'age': 33},
    {'name': 'Joseph Thompson', 'email': 'joseph.thompson@example.com', 'age': 40},
    {'name': 'Susan Garcia', 'email': 'susan.garcia@example.com', 'age': 36}
]

users_df = pd.DataFrame(users)

count_over_21 = users_df[users_df['age'] > 21].shape[0]
df_sorted = users_df.sort_values(by='email')

print(f'Number of users over the age of 21 - {count_over_21}')
print(df_sorted)
