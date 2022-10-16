import pandas as pd

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def normalize(old_columns):
    new_columns = []
    for s in old_columns:
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        new_columns.append(s)
    return new_columns

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def counter(df, par, find, index_):
    funiq = pd.unique(df[par])
    arr = []
    for i in funiq:
        arr.append(df.loc[(df[index_] == find) & (df[par] == i)].shape[0])

    return arr

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def adder(df, par, index_):
  funiq = pd.unique(df[par])
  arr = []
  for i in funiq:
    a = df.loc[df[par] == i]
    sum = a.sum()
    arr.append(sum[index_])
  return arr
