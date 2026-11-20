"""Sample optimization problems for the AIDE RSI loop."""
import random
import string


# ---------------------------------------------------------------------------
# Problem 1 — Naive bubble-sort
# ---------------------------------------------------------------------------
PROBLEM_BUBBLE_SORT = {
    "name": "Bubble Sort → Optimized Sort",
    "description": "Replace a naive O(n²) bubble sort with progressively better algorithms.",
    "versions": [
        {
            "label": "v0  naive bubble sort",
            "code": (
                "def solve(data):\n"
                "    arr = list(data)\n"
                "    n = len(arr)\n"
                "    for i in range(n):\n"
                "        for j in range(0, n - i - 1):\n"
                "            if arr[j] > arr[j + 1]:\n"
                "                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n"
                "    return arr\n"
            ),
        },
        {
            "label": "v1  early-exit bubble sort",
            "code": (
                "def solve(data):\n"
                "    arr = list(data)\n"
                "    n = len(arr)\n"
                "    for i in range(n):\n"
                "        swapped = False\n"
                "        for j in range(0, n - i - 1):\n"
                "            if arr[j] > arr[j + 1]:\n"
                "                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n"
                "                swapped = True\n"
                "        if not swapped:\n"
                "            break\n"
                "    return arr\n"
            ),
        },
        {
            "label": "v2  insertion sort",
            "code": (
                "def solve(data):\n"
                "    arr = list(data)\n"
                "    for i in range(1, len(arr)):\n"
                "        key = arr[i]\n"
                "        j = i - 1\n"
                "        while j >= 0 and arr[j] > key:\n"
                "            arr[j + 1] = arr[j]\n"
                "            j -= 1\n"
                "        arr[j + 1] = key\n"
                "    return arr\n"
            ),
        },
        {
            "label": "v3  merge sort",
            "code": (
                "def solve(data):\n"
                "    arr = list(data)\n"
                "    if len(arr) <= 1:\n"
                "        return arr\n"
                "    mid = len(arr) // 2\n"
                "    left = solve(arr[:mid])\n"
                "    right = solve(arr[mid:])\n"
                "    merged, i, j = [], 0, 0\n"
                "    while i < len(left) and j < len(right):\n"
                "        if left[i] <= right[j]:\n"
                "            merged.append(left[i]); i += 1\n"
                "        else:\n"
                "            merged.append(right[j]); j += 1\n"
                "    merged.extend(left[i:])\n"
                "    merged.extend(right[j:])\n"
                "    return merged\n"
            ),
        },
        {
            "label": "v4  Tim sort (built-in)",
            "code": (
                "def solve(data):\n"
                "    return sorted(data)\n"
            ),
        },
    ],
    "make_input": lambda size=3000: random.sample(range(size * 10), size),
    "verify": lambda out, inp: out == sorted(inp),
}


# ---------------------------------------------------------------------------
# Problem 2 — Slow string processing
# ---------------------------------------------------------------------------
def _make_string_input(size=50_000):
    return "".join(random.choices(string.ascii_lowercase + " ", k=size))


PROBLEM_STRING_PROCESSING = {
    "name": "String Word-Frequency Counter",
    "description": "Optimize a naive word-frequency counter that re-scans the string.",
    "versions": [
        {
            "label": "v0  quadratic .count() per unique word",
            "code": (
                "def solve(data):\n"
                "    words = data.split()\n"
                "    unique = []\n"
                "    for w in words:\n"
                "        if w not in unique:\n"
                "            unique.append(w)\n"
                "    freq = {}\n"
                "    for w in unique:\n"
                "        freq[w] = words.count(w)\n"
                "    return freq\n"
            ),
        },
        {
            "label": "v1  set for uniqueness, still .count()",
            "code": (
                "def solve(data):\n"
                "    words = data.split()\n"
                "    unique = set(words)\n"
                "    freq = {}\n"
                "    for w in unique:\n"
                "        freq[w] = words.count(w)\n"
                "    return freq\n"
            ),
        },
        {
            "label": "v2  single-pass dict accumulator",
            "code": (
                "def solve(data):\n"
                "    freq = {}\n"
                "    for w in data.split():\n"
                "        freq[w] = freq.get(w, 0) + 1\n"
                "    return freq\n"
            ),
        },
        {
            "label": "v3  collections.Counter (C-accelerated)",
            "code": (
                "from collections import Counter\n"
                "def solve(data):\n"
                "    return dict(Counter(data.split()))\n"
            ),
        },
    ],
    "make_input": _make_string_input,
    "verify": lambda out, inp: True,  # all versions return same dict
}


# ---------------------------------------------------------------------------
# Problem 3 — Inefficient data aggregation
# ---------------------------------------------------------------------------
def _make_sales_input(n=5000):
    regions = ["North", "South", "East", "West"]
    products = ["Widget", "Gadget", "Doohickey", "Thingamajig"]
    rows = []
    for _ in range(n):
        rows.append(
            {
                "region": random.choice(regions),
                "product": random.choice(products),
                "amount": round(random.uniform(10, 500), 2),
            }
        )
    return rows


PROBLEM_DATA_AGGREGATION = {
    "name": "Sales Data Aggregation",
    "description": "Aggregate sales by region+product — from nested loops to vectorised.",
    "versions": [
        {
            "label": "v0  triple nested loop",
            "code": (
                "def solve(data):\n"
                "    regions = list({r['region'] for r in data})\n"
                "    products = list({r['product'] for r in data})\n"
                "    result = {}\n"
                "    for reg in regions:\n"
                "        for prod in products:\n"
                "            total = 0\n"
                "            for row in data:\n"
                "                if row['region'] == reg and row['product'] == prod:\n"
                "                    total += row['amount']\n"
                "            result[(reg, prod)] = round(total, 2)\n"
                "    return result\n"
            ),
        },
        {
            "label": "v1  single pass with dict accumulator",
            "code": (
                "def solve(data):\n"
                "    result = {}\n"
                "    for row in data:\n"
                "        key = (row['region'], row['product'])\n"
                "        result[key] = result.get(key, 0) + row['amount']\n"
                "    return {k: round(v, 2) for k, v in result.items()}\n"
            ),
        },
        {
            "label": "v2  defaultdict accumulator",
            "code": (
                "from collections import defaultdict\n"
                "def solve(data):\n"
                "    result = defaultdict(float)\n"
                "    for row in data:\n"
                "        result[(row['region'], row['product'])] += row['amount']\n"
                "    return {k: round(v, 2) for k, v in result.items()}\n"
            ),
        },
        {
            "label": "v3  pandas groupby",
            "code": (
                "import pandas as pd\n"
                "def solve(data):\n"
                "    df = pd.DataFrame(data)\n"
                "    agg = df.groupby(['region', 'product'])['amount'].sum().round(2)\n"
                "    return {k: v for k, v in agg.items()}\n"
            ),
        },
    ],
    "make_input": _make_sales_input,
    "verify": lambda out, inp: True,
}


# ---------------------------------------------------------------------------
# Problem 4 — Fibonacci (exponential → linear → constant)
# ---------------------------------------------------------------------------
PROBLEM_FIBONACCI = {
    "name": "Fibonacci Computation",
    "description": "Compute the n-th Fibonacci number — from naive recursion to O(1) formula.",
    "versions": [
        {
            "label": "v0  naive recursion O(2^n)",
            "code": (
                "def solve(data):\n"
                "    n = data\n"
                "    if n <= 1:\n"
                "        return n\n"
                "    return solve(n - 1) + solve(n - 2)\n"
            ),
        },
        {
            "label": "v1  memoised recursion",
            "code": (
                "def solve(data, _cache={}):\n"
                "    n = data\n"
                "    if n in _cache:\n"
                "        return _cache[n]\n"
                "    if n <= 1:\n"
                "        return n\n"
                "    _cache[n] = solve(n - 1) + solve(n - 2)\n"
                "    return _cache[n]\n"
            ),
        },
        {
            "label": "v2  iterative O(n)",
            "code": (
                "def solve(data):\n"
                "    n = data\n"
                "    if n <= 1:\n"
                "        return n\n"
                "    a, b = 0, 1\n"
                "    for _ in range(2, n + 1):\n"
                "        a, b = b, a + b\n"
                "    return b\n"
            ),
        },
        {
            "label": "v3  matrix exponentiation O(log n)",
            "code": (
                "def solve(data):\n"
                "    n = data\n"
                "    if n <= 1:\n"
                "        return n\n"
                "    def mat_mul(A, B):\n"
                "        return [\n"
                "            [A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],\n"
                "            [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]],\n"
                "        ]\n"
                "    def mat_pow(M, p):\n"
                "        result = [[1,0],[0,1]]\n"
                "        while p:\n"
                "            if p % 2:\n"
                "                result = mat_mul(result, M)\n"
                "            M = mat_mul(M, M)\n"
                "            p //= 2\n"
                "        return result\n"
                "    return mat_pow([[1,1],[1,0]], n)[0][1]\n"
            ),
        },
    ],
    "make_input": lambda size=30: 30,  # fixed n=30 for fair comparison
    "verify": lambda out, inp: out == 832040,
}


ALL_PROBLEMS = [
    PROBLEM_BUBBLE_SORT,
    PROBLEM_STRING_PROCESSING,
    PROBLEM_DATA_AGGREGATION,
    PROBLEM_FIBONACCI,
]
