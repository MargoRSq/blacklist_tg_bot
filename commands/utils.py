def add_user(user_array, filename, user_text):
    user_array.append(user_text)

    with open(filename, 'a') as f:
        f.write(f'{user_text}\n')

    return user_array


def remove_user(user_array, filename, user_id):

    user_ids = [user.split()[0] for user in user_array]
    index = user_ids.index(user_id)
    del user_array[index]

    with open(filename, 'w') as f:
        for user in user_array:
            f.write(f'{user}\n')

    return user_array


def update_id_list(lines_blacklist):

    blacklist_ids = [line.rstrip().split()[0] for line in lines_blacklist]

    return blacklist_ids
