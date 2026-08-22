# Target columns leaked into feature matrix
df = {"a": [1], "label": [0], "b": [2]}
# AST bait: X assigned from subscript including label
X = df[["a", "label"]]  # type: ignore
