from pyspark.sql import SparkSession
import csv
import math

spark = SparkSession.builder.appName("DistributedGeneExpressionAnalysis").getOrCreate()
sc = spark.sparkContext

print("Spark master:", sc.master)
print("Default parallelism:", sc.defaultParallelism)

csv_path = "/tmp/leukemia_expression.csv"

rows = []
with open(csv_path, "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        values = [float(x) for x in row]
        features = values[:-1]
        label = int(values[-1])
        rows.append((features, label))

feature_count = len(header) - 1

rdd = sc.parallelize(rows, 4)
train_rdd, test_rdd = rdd.randomSplit([0.8, 0.2], seed=42)

def add_vectors(a, b):
    return [x + y for x, y in zip(a, b)]

def seq_op(acc, row):
    features, label = row
    sums, count = acc
    return (add_vectors(sums, features), count + 1)

def comb_op(a, b):
    return (add_vectors(a[0], b[0]), a[1] + b[1])

centroid_data = train_rdd.map(lambda row: (row[1], row)) \
    .aggregateByKey(([0.0] * feature_count, 0), seq_op, comb_op) \
    .collectAsMap()

centroids = {}
for label, (sums, count) in centroid_data.items():
    centroids[label] = [x / count for x in sums]

def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def predict(features):
    best_label = None
    best_dist = None
    for label, centroid in centroids.items():
        d = distance(features, centroid)
        if best_dist is None or d < best_dist:
            best_dist = d
            best_label = label
    return best_label

correct = test_rdd.map(lambda row: 1 if predict(row[0]) == row[1] else 0).sum()
total = test_rdd.count()
accuracy = correct / total if total > 0 else 0

print("Distributed Spark ML completed successfully")
print("Bioinformatics dataset rows:", len(rows))
print("Number of gene features:", feature_count)
print("Test accuracy:", round(accuracy, 4))

spark.stop()
