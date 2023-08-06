from bidtoolsdk.google.keyword_performance import get_keyword_performance_df
from bidtoolsdk.configuration.adgroup_config import get_adgroup_config_df

if __name__ == '__main__':
    config = get_adgroup_config_df('123-830-9364', is_staging=True)
    # config = get_keyword_performance_df('123-830-9364')
    print(config.columns)
