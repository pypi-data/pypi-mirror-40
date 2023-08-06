# fluentxy

A small package to parse `.xy` output files from Fluent into Pandas DataFrames.
The typical `.xy` output from Fluent looks like

```text
(title "Axial Velocity")
(labels "Position" "Axial Velocity")

((xy/key/label "inlet")
0	0.2
...
0.00873	0.2
)
```

and this module parses this output into a DataFrame that looks like

```python
from fluentxy import parse_data
with open('filename.xy', 'r') as f:
    lines = f.readlines()
data = parse_data(lines)
data.head()
      inlet
   Position Axial Velocity
0  0.000000            0.2
1  0.000582            0.2
2  0.001164            0.2
3  0.001746            0.2
4  0.002328            0.2
```
