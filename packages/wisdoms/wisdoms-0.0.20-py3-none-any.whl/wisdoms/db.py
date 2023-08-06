# Created by Q-ays.
# whosqays@gmail.com

# Have to install sqlalchemy

from sqlalchemy.exc import SQLAlchemyError


def session_exception(session, is_raise=True):

    def wrapper(func):

        def catch(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except SQLAlchemyError as e:
                print(e)
                print('~~~~~~~~~~~~~~~~session error~~~~~~~~~~~~~~~~~~')
                session.rollback()
                if is_raise:
                    raise e

        return catch

    return wrapper
