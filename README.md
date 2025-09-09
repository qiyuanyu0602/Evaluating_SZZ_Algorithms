# Evaluating_SZZ_Algorithms

- The **SZZ_tools** folder contains several SZZ algorithm tools we used for testing.
- The **testdata** folder contains several config files and test data.
- **CVECrawler.py** is used to collect CVE IDs, VIC SHAs, and VFC SHAs, and output an `.xlsx` file. The logic of this method is that each CVE ID corresponds to one VIC SHA and one VFC SHA, and among all VFCs, only the earliest commit is an upstream commit.
- **analysis.py** takes an `.xlsx` file as input and calculates the following results: cases where a VFC SHA appears as a VIC SHA, whether there are duplicate VFC SHAs, and cases where one VIC corresponds to multiple VFCs.

