from bidtoolsdk.google.keyword_performance import get_keyword_performance_df

if __name__ == '__main__':
    config = get_keyword_performance_df('123-830-9364')
    print(config.columns)
