# easypipeline: Chaining functions execution made easy

```
from easypipeline import make_pipeline
from math import sqrt

def operation(n1: float, n2: float) -> float:
    return n1 + n2

pipeline = make_pipeline(
    operation,
    lambda n: n**0.5
)

assert pipeline(1, 2) == sqrt(3)
```
