import csv
import base64
import subprocess
import hashlib
import math

INPUT_FILE = "data.csv"
ANSWER_FILE = "exrc-04-answer.txt"


def decrypt_value(encrypted_bytes):
    """
    Decrypt using gpg command line.
    """
    result = subprocess.run(
        ["gpg", "--decrypt"],
        input=encrypted_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        print("Decryption failed")
        return None

    return result.stdout.decode("utf-8").strip()


def convert_to_float(value):
    try:
        return float(value)
    except:
        return float("nan")


weather_data = {}

with open(INPUT_FILE, "r", encoding="utf-8") as file:

    csv_reader = csv.reader(file)

    # skip header
    next(csv_reader, None)

    for row in csv_reader:

        try:
            time = row[0]
            parameter_name = row[1]
            parameter_value = row[2]

            # Only keep required parameters
            if parameter_name != "TA_PT1H_MAX" and parameter_name != "TA_PT1H_MIN":
                continue

            # Decrypt if needed
            if parameter_value.startswith("PGP_B64:"):
                b64_data = parameter_value[len("PGP_B64:"):]
                encrypted_bytes = base64.b64decode(b64_data)
                plaintext = decrypt_value(encrypted_bytes)
            else:
                plaintext = parameter_value

            numeric_value = convert_to_float(plaintext)

            # Skip if NaN
            if math.isnan(numeric_value):
                continue

            # Initialize dictionary if not exists
            if time not in weather_data:
                weather_data[time] = {}

            # Keep only first occurrence
            if parameter_name not in weather_data[time]:
                weather_data[time][parameter_name] = numeric_value

        except Exception as e:
            print("Error processing row:", e)


# Build canonical table
rows = []

for time in weather_data:

    if "TA_PT1H_MAX" in weather_data[time] and "TA_PT1H_MIN" in weather_data[time]:

        max_value = weather_data[time]["TA_PT1H_MAX"]
        min_value = weather_data[time]["TA_PT1H_MIN"]

        value_range = max_value - min_value

        rows.append((time, max_value, min_value, value_range))


# Sort by Time
rows.sort(key=lambda x: x[0])


# Build canonical CSV string 

lines = []
lines.append("Time,max,min,range")

for row in rows:

    time = row[0]
    max_str = "{:.3f}".format(row[1])
    min_str = "{:.3f}".format(row[2])
    range_str = "{:.3f}".format(row[3])

    line = time + "," + max_str + "," + min_str + "," + range_str
    lines.append(line)

# Important: final trailing newline
payload = "\n".join(lines) + "\n"


# Compute SHA-256
sha256_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()

short_hash = sha256_hash[:16]

print("Full SHA256:", sha256_hash)
print("First 16 characters:", short_hash)


# Write answer file
with open(ANSWER_FILE, "w", encoding="utf-8", newline="\n") as f:
    f.write(short_hash + "\n")
