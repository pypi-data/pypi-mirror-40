from bidtoolsdk.configuration.adgroup_config import get_dealer_config_df

if __name__ == '__main__':
    config = get_dealer_config_df('123-830-9364')
    print(config.columns)
