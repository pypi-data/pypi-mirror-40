from sqlalchemy.orm import sessionmaker
from ads_api.database.dealer_config import db, DealerConfig
import pandas as pd

Session = sessionmaker(db)
session = Session()


def get_configuration_to_df(platform_ids):

    try:
        rows = session.query(DealerConfig).filter(DealerConfig.platform_id.in_([str(id_) for id_ in platform_ids])).all()
    except Exception as e:
        print('config error', e)
        session.rollback()
        return

    config_df = pd.DataFrame([row.__dict__ for row in rows])
    if '_sa_instance_state' in config_df:
        return config_df.drop('_sa_instance_state', axis=1)
    return config_df


if __name__ == '__main__':

    print(get_configuration_to_df(['123-830-9364']))
