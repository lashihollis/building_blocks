from dataqualitycheck import results
import matplotlib.pyplot as plt

check_names = []
failure_counts = []

check_names = []
failure_counts = []

for result in results:
    check_names.append(result["check"])
    failure_counts.append(result["failure_count"])

plt.bar(check_names, failure_counts)
plt.title("Data Quality Check Results")
plt.xlabel("Data Quality Check")
plt.ylabel("Amount of Errors")
plt.xticks(rotation=45)

plt.show()
