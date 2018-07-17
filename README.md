# pharmacy-counting
My solution to the [Insight Data Engineering Coding Competition](https://github.com/InsightDataScience/pharmacy_counting).

## Executing the project
The solution is written in Python 2.  

The script `run.sh` executes the project; the input data file is `input/itcont.txt`, and the result is written into `output/top_cost_drug.txt`. Running `insight_testsuite/run_tests.sh` evaluates the solution using the tests from `insight_testsuite/tests/`.

There are 2 versions of the solution: basic and with _MapReduce_. By default the basic algorithm script (`pharmacy-counting.py`) is called. To run another script(`pharmacy-counting_divide.py`), comment line 3 and uncomment line 4 in `run.sh` file.

_**Note:**_ *to execute `run_tests.sh`, change your current_working_directory to `insight_testsuite/` first, and then call `./run_tests.sh`.*

## Basic algorithm overview
The basic version of the algorithm reads data entries from the input file `itcont.txt` line by line, extracting required fields from each line after it is read, and adding the new data to the data structures that allow efficient computation of the required statistics.

The complexity of the algorithm is _**O(N)+O(M*log(M))**_, where _**N**_ is the total number of entries scanned, _**M<=N**_ is the number of unique drug names. In the worst case (when _**M=N**_) the complexity is _**O(N*log(N))**_, but if _**M<<N**_ it reduces to _**O(N)**_.

The data structure used to store the drugs information is a dictionary `drugs`, that has drug names as keys and pairs (lists) `[total_cost,id_set]` as values. `total_cost` is the total cost of all prescriptions of particular drug and is updated as more and more data entries are processed. `id_set` is a set of all `id`-fields of people that prescribed this particular drug. Since it is needed to count all _unique_ prescribers for each drug name, it is checked frequently whether the current provider already prescribed it. `set()` data structure is used because, compared to list, it allows a faster check whether element is a part of the iterable or not.

## MapReduce version of the algorithm
This version of the algorithm reads data entries from the input file `itcont.txt` line by line, extracting required fields from each line after it is read and grouping data entries (tuples `(id,drug_name,drug_cost)`) by the 1st character in the `drug_name` field. After that each group is recorded into the file `<first_character>.json` (or `quotes.json` for drug names with quotes). This allows for parallel processing of data.

Each group of data entries is processed in tha same way as in the basic algorithm, which yields a number of sorted lists. Those lists are then merged into one sorted list, which represents the required statistics.

## Assumptions
* input is not extremely large so that all the processed data may be stored in the RAM;
* `id` is a row of symbols (without `,`);
* each prescriber has their unique id, so when checking uniqueness, we can just refer to the `id` field and ignore the name of prescriber;
* `drug_name` can contain `,` and when it does, it also has `"` in the beginning and the end;
* `drug_cost` is a real (float) number (the input numbers can be integers, but they will be converted to floats);
* if there is a tie in `total_cost`, drugs are sorted alphabetically by name (without quotes).

## Project dependencies
My basic implementation only imports variables from standard Python library `sys`. Implementation with _Mapreduce_ requires the following Python libraries: `sys`, `os`, `json` and `heapq`.

## Other
The test proposed in the assignment was modified to fit into the format of the proposed large dataset in a way that:
* all data entries (for input and output) start from new lines;
* the cost values in the output are converted to floats.