import pandas as pd

def main():
    data = pd.read_csv('../data.csv')
    data.to_csv("data2.csv", index=False, float_format='{:f}'.format, encoding='utf-8')
    pass


if __name__ == "__main__":
    main()
