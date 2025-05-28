import pickle


def fxer():

    with open('link_list.pickle', 'rb') as file:
        link_list = pickle.load(file)

    tlist_done: list[str] = []

    for i in link_list:
        newstr = i.replace('https://x.com', 'https://fixvx.com')
        tlist_done.append(newstr)


    with open('link_list_fx.pickle', 'wb') as file:
        pickle.dump(tlist_done, file)

    print('link_list_fx.pickle updated!')
