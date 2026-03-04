def update_account_data(v1_data, onboarding_data):

    updated = v1_data.copy()

    for key, value in onboarding_data.items():

        if value:  
            updated[key] = value

    return updated