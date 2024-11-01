import streamlit as st
import streamlit_authenticator as stauth

def authenticate_user():
    names = ['Ravinder', 'Latha', 'Chandan', 'Vaishnavi']
    usernames = ['Ravinder', 'Latha', 'Chandan', 'Vaishnavi']
    passwords = ['Ravinder@3716', 'Latha@3716', 'Chandan@3716', 'Vaishnavi@3716']
    hashed_passwords = stauth.Hasher(passwords).generate()
    credentials = {
        "usernames": {
            "Ravinder": {
                "name": "Ravinder",
                "password": "Ravinder@3716"
            },
            "Latha": {
                "name": "Latha",
                "password": "Latha@3716"
            },
            "Chandan": {
                "name": "Chandan",
                "password": "Chandan@3716"
            },
            "Vaishnavi": {
                "name": "Vaishnavi",
                "password": "Vaishnavi@3716"
            }
        }
    }

    authenticator = stauth.Authenticate(
        # credentials=credentials,
        names=names,
        usernames=usernames,
        passwords=hashed_passwords,
        cookie_name='Weight Tracker',
        key='Simba',
        cookie_expiry_days=30
    )

    # Login Widget
    name, authentication_status, username = authenticator.login("Login", 'main')

    if authentication_status:
        return authenticator, name, username
    elif authentication_status is False:
        st.error("Username/password is incorrect")
    elif authentication_status is None:
        st.warning("Please enter your username and password")

    return None, None, None
