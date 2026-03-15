import pandas as pd


# df1 = pd.read_csv("EldersWisdom.csv", sep = "|")
df2 = pd.read_table("EldersWisdom.csv", sep="|")
# print(df1.head(5))
# print(df2[0:3])
# print(f"Full table below...")
# print(df2)

quotes = df2.set_index(["quoteId"])


# print(quotes)
#
# print(quotes.to_json(orient="index"))

QUOTES = (quotes.to_json(orient="index"))
# print(QUOTES)

sug = 1


def plsgo():
    if sug == 1:
        return QUOTES
    else:
        return "Whoops!"


print(plsgo())
