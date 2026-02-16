

### Exercise 4 -- Data part

You are given a CSV file `data.csv` (weather measurement data) with columns:

- `Time`
- `ParameterName`
- `ParameterValue`

Some `ParameterValue` cells are plaintext numbers. Others are encrypted and appear as:

- `PGP_B64:<base64-data>`

Encrypted cells contain a single numeric value (as text) that you must decrypt using `gpg` and your provided private key.

### Goal
Compute a short checksum of a **derived table** (further specified below) built only from temperature max/min values.
Also write a short report about your work.

### Tasks

#### 1) Read and decrypt values
1. Read `data.csv`.
2. For each row:
   - If `ParameterValue` starts with `PGP_B64:`, base64-decode the remainder to bytes and decrypt it with `gpg` to obtain the plaintext numeric string.
   - Otherwise, use the plaintext `ParameterValue` directly.
3. Convert the resulting value to a number (float is fine). If conversion fails, treat it as missing (`NaN`).

#### 2) Filter to the two required parameters
Keep only rows where `ParameterName` is exactly one of:

- `TA_PT1H_MAX`
- `TA_PT1H_MIN`

Ignore all other parameters.

#### 3) Pivot to one row per Time
Create a table indexed by `Time` with two columns:

- `TA_PT1H_MAX`
- `TA_PT1H_MIN`

If there are multiple rows for the same `(Time, ParameterName)`, keep the first one encountered in the file.

Drop any `Time` where either max or min is missing.

#### 4) Build the canonical output table
Create a new table with columns in exactly this order:

1. `Time`
2. `max`  (from `TA_PT1H_MAX`)
3. `min`  (from `TA_PT1H_MIN`)
4. `range` = `max - min`

Sort rows by `Time` ascending (string sort is fine).

#### 5) Canonical numeric formatting
Format `max`, `min`, and `range` as decimal strings with **exactly 3 digits after the decimal point** (e.g. `-9.100`, `0.000`, `12.345`).

#### 6) Canonical CSV serialization
Serialize the canonical table as CSV with:

- header line: `Time,max,min,range`
- comma as separator
- `\n` newlines
- include a final trailing newline at the end

Do not include an index column.

#### 7) Hash
Compute the SHA-256 hex digest (lowercase hex) of the UTF-8 encoded canonical CSV string.

#### 8) Submit
Replace the string `replace-answer-here` in the file `exrc-04-answer.txt` with the **first 16 hex characters** of your computed SHA-256 digest.

#### 9) Report
Write a separate report (Jupyter notebook) about solving Exercise 4 in the file

    exrc-04-report.ipynb

This report should contain (e.g.)

- code snippets used
- AI prompts used
- links to external material used
- your thoughts about the process.


### Notes / common pitfalls
- You are **not** hashing the original CSV.
- You are hashing the **derived** canonical CSV (`Time,max,min,range`) after filtering/pivoting.
- Ensure you drop times where either max or min is missing.
- Ensure the float formatting is exactly 3 decimals for all three numeric columns.
- Ensure the CSV uses `\n` line endings and includes a final trailing newline.

**Important (especially for Windows users):** Be careful with writing the canonical CSV to a file and hashing the file contents. It would be better to build the canonical CSV as a Python string, joining the lines using `"\n"` explicitly, and then hash the Python string. This guarantees `\n` newlines regardless of OS. If you necessarily want to write a file, do it like this:

```python
with open("canonical.csv", "w", encoding="utf-8", newline="\n") as f:
    f.write(payload)
```
# JAMK_2026_Excr04
