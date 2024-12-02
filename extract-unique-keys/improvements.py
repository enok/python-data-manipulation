"""
For large datasets

Handling large JSON files with 500 million records requires careful planning for memory efficiency, scalability, and performance. Here are the best approaches:

"""



"""
1. Use Incremental Processing (Streaming)
For extremely large files, avoid loading the entire file into memory. Instead, process it incrementally using a streaming library like ijson or by reading the file in chunks.

Using ijson for Streaming:
ijson parses JSON incrementally, allowing you to process each JSON object one at a time.
"""
import ijson

def extract_unique_keys_large_json(file: str) -> list:
    """
    Extract unique keys from a very large JSON file using incremental parsing.

    Args:
        file (str): Path to the large JSON file.

    Returns:
        list: List of unique keys in the JSON file.
    """
    unique_keys = set()

    with open(file, 'r') as f:
        for record in ijson.items(f, 'item'):
            def extract_keys(obj, prefix=""):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        full_key = f"{prefix}.{key}" if prefix else key
                        unique_keys.add(full_key)
                        extract_keys(value, prefix=full_key)
                elif isinstance(obj, list):
                    for item in obj:
                        extract_keys(item, prefix=prefix)

            extract_keys(record)

    return sorted(set(key.split('.')[0] for key in unique_keys))



"""
2. Use JSON Lines Format (.jsonl)
Convert the large JSON file into a JSON Lines format, where each record is a separate line. This allows you to read and process the file line-by-line.

Advantages:
Reduces memory overhead as you process one record at a time.
Easier to parallelize processing.
"""
import json

def extract_unique_keys_jsonl(file: str) -> list:
    """
    Extract unique keys from a JSON Lines file.

    Args:
        file (str): Path to the JSON Lines file.

    Returns:
        list: List of unique keys in the file.
    """
    unique_keys = set()

    with open(file, 'r') as f:
        for line in f:
            record = json.loads(line.strip())

            def extract_keys(obj, prefix=""):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        full_key = f"{prefix}.{key}" if prefix else key
                        unique_keys.add(full_key)
                        extract_keys(value, prefix=full_key)
                elif isinstance(obj, list):
                    for item in obj:
                        extract_keys(item, prefix=prefix)

            extract_keys(record)

    return sorted(set(key.split('.')[0] for key in unique_keys))



"""
3. Use Big Data Tools
If the file is too large for Python alone, leverage Big Data frameworks like Apache Spark or Dask for distributed processing.

Using Apache Spark (PySpark):
Apache Spark is optimized for handling large datasets across clusters.
"""
from pyspark.sql import SparkSession

def extract_unique_keys_spark(file: str) -> list:
    """
    Extract unique keys from a JSON file using Apache Spark.

    Args:
        file (str): Path to the JSON file.

    Returns:
        list: List of unique keys in the file.
    """
    spark = SparkSession.builder \
        .appName("Extract Unique Keys") \
        .getOrCreate()

    # Load JSON file
    df = spark.read.json(file)

    # Flatten and collect unique keys
    unique_keys = df.schema.names
    return sorted(unique_keys)

# Example usage:
# file_path = "large_file.json"
# print(extract_unique_keys_spark(file_path))



"""
4. Use Chunk-Based Processing
For hierarchical JSON files, split the file into smaller chunks for parallel processing using tools like multiprocessing.
"""
import json
from multiprocessing import Pool

def process_chunk(chunk):
    unique_keys = set()
    for record in chunk:
        def extract_keys(obj, prefix=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    full_key = f"{prefix}.{key}" if prefix else key
                    unique_keys.add(full_key)
                    extract_keys(value, prefix=full_key)
            elif isinstance(obj, list):
                for item in obj:
                    extract_keys(item, prefix=prefix)

        extract_keys(record)

    return unique_keys

def extract_unique_keys_parallel(file: str, chunk_size: int = 10000) -> list:
    unique_keys = set()

    with open(file, 'r') as f:
        data = json.load(f)

    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    with Pool() as pool:
        results = pool.map(process_chunk, chunks)

    for result in results:
        unique_keys.update(result)

    return sorted(set(key.split('.')[0] for key in unique_keys))




"""
Recommendations
- For Large Files in a Single Machine: Use ijson or JSON Lines.
- For Distributed Processing: Use Apache Spark or Dask.
- For Parallel Processing: Use Python’s multiprocessing with chunked processing.


Considerations
- Storage: If the file is compressed, decompress it first for better performance.
- Memory: Incremental processing (e.g., ijson or line-by-line processing) avoids memory bottlenecks.
- Disk I/O: Optimize disk I/O by using efficient formats (e.g., JSON Lines, Parquet).
"""