from .base import Bench
from .text_to_sql import create_bird

classes = locals()

TASKS = {
    "sql_generation_public": create_bird()
}

def load_benchmark(benchmark_name) -> Bench:
    if benchmark_name in TASKS:
        return TASKS[benchmark_name]
    if benchmark_name in classes:
        return classes[benchmark_name]
    raise ValueError(f"Unknown benchmark: {benchmark_name}")