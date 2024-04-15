# import pandas as pd
#
# # Read the CSV file into a pandas DataFrame
# df = pd.read_csv("filtered_file.csv")
#
# # Remove rows with duplicated values in the "Actual" column
# df = df.drop_duplicates(subset=["Actual"])
#
# # Save the filtered DataFrame back to a CSV file
# df.to_csv("filtered_file_2.csv", index=False)
# import pandas as pd
#
# # Read the CSV file into a pandas DataFrame
# df = pd.read_csv("340w.csv")
# df = df.drop_duplicates(subset=["Actual"])
# df.to_csv("filtered_file_2.csv", index=False)

# Calculate accuracy for each row and store it in a list
from difflib import SequenceMatcher
# import pandas as pd
#
# # def similar(a, b):
# #     if not a or not b:  # Check if either string is empty or None
# #         return 0.0
# #     else:
# #         return SequenceMatcher(None, a, b).ratio()
# #
# df = pd.read_csv('similarities.csv')
# #
# # data_dict = {'Algorithm': df['Generated'].tolist(), 'Actual': df['Actual'].tolist()}
# # df2 = pd.DataFrame(data_dict)
# # df2['Similarity'] = df2.apply(lambda row: similar(str(row['Algorithm']), str(row['Actual'])), axis=1)
# # df2.to_csv('similarities.csv', index=False)
# average_similarity = df['Similarity'].mean()
# print("Average Similarity:", average_similarity)
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # or any other backend that works for you
import matplotlib.pyplot as plt

df = pd.read_csv('similarities.csv')

average_similarity = df['Similarity'].mean()
median_similarity = df['Similarity'].median()
first_quartile_similarity = df['Similarity'].quantile(0.25)
third_quartile_similarity = df['Similarity'].quantile(0.75)
std_dev_similarity = df['Similarity'].std()

print("Average Similarity:", average_similarity)
print("Median Similarity:", median_similarity)
print("First Quartile Similarity:", first_quartile_similarity)
print("Third Quartile Similarity:", third_quartile_similarity)
print("Standard Deviation of Similarity:", std_dev_similarity)

# Box and whiskers plot
plt.figure(figsize=(8, 6))
plt.boxplot(df['Similarity'], vert=False)
plt.title('Similarity Distribution')
plt.xlabel('Similarity')
plt.ylabel('Data')
plt.grid(True)
plt.show()
