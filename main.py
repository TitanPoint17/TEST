import requests
from tkinter import *
from typing import List, Dict, Union

api = "https://jsonplaceholder.typicode.com/"

posts_by_id: List[Dict[str, Union[int, str]]] = []
posts_by_userid: Dict[int, List[Dict[str, Union[int, str]]]] = {}


# Helper functions


def validate(userid):

    resp = requests.get(api + "users/").json()

    for user in resp:
        if user['id'] == userid:
            return True

    invalid = Label(frame, text="User ID does not exist")
    invalid.grid(row=10)

    return False


def destroy():

    for widgets in frame.winfo_children():
        widgets.destroy()


def back_to_first_page(colspan=1):

    new_action = Button(frame, text="Another action", command=initialize)
    new_action.grid(row=20, pady=20, columnspan=colspan)


def invalid_uid():

    invalid = Label(frame, text="User ID contains invalid characters\n"
                                "User ID should only contain numbers")
    invalid.grid(row=10)


def invalid_pid():

    invalid = Label(frame, text="Post ID contains invalid characters\n"
                                "Post ID should only contain numbers")
    invalid.grid(row=10)


def success():

    valid = Label(frame, text="Success!", padx=150, pady=10)
    valid.grid(row=10)


def add_to_local(userid, title, body):

    post_id = len(posts_by_id) + 1

    posts_by_id.append({"userId": userid, "id": post_id,
                        "title": title, "body": body})

    posts_by_userid[userid].append({"userId": userid, "id": post_id,
                                    "title": title, "body": body})


def nonexistent(col=0):

    invalid = Label(frame, text="Post with this ID does not exist")
    invalid.grid(row=10, column=col)


# Add post functions


def add_post(userid, title, body):

    if not userid.isnumeric():
        invalid_uid()
        return

    userid = int(userid)

    if not validate(userid):
        return

    add_to_local(userid, title, body)

    post_id = len(posts_by_id) + 1

    requests.post(api + "posts/", json={"userId": userid, "id": post_id,
                                        "title": title, "body": body})

    success()

    back_to_first_page()


def click_add():

    destroy()

    userid = Label(frame, text="Enter your user ID:")
    e_user = Entry(frame, width=20)

    title = Label(frame, text="Add an interesting title:")
    e_title = Entry(frame, width=40)

    body = Label(frame, text="Enter your text:")
    e_body = Text(frame, width=128, height=22)

    submitt = Button(frame, text="Submit", command=lambda: add_post(
        e_user.get(), e_title.get(), e_body.get(1.0, "end-1c")))

    submitt.grid(row=6, column=0, pady=15)

    userid.grid(row=0, column=0, pady=5)
    e_user.grid(row=1, column=0)
    title.grid(row=2, column=0, pady=5)
    e_title.grid(row=3, column=0)
    body.grid(row=4, column=0, pady=5)
    e_body.grid(row=5, column=0)
    submitt.grid(row=6, column=0, pady=15)

    back_to_first_page()


# Delete post functions


def delete(userid, post_id):

    if not userid.isnumeric():
        invalid_uid()
        return

    if not post_id.isnumeric():
        invalid_pid()
        return

    userid = int(userid)
    post_id = int(post_id)

    try:
        post_to_delete = posts_by_id[post_id - 1]

    except IndexError:
        nonexistent()
        return

    if post_to_delete is None:
        invalid = Label(frame, text="Post has already been deleted")
        invalid.grid(row=10)
        return

    if posts_by_id[post_id - 1]['userId'] != userid:
        invalid = Label(frame, text="Unable to delete posts from other users")
        invalid.grid(row=10)
        return

    posts_by_userid[post_to_delete['userId']].remove(post_to_delete)
    posts_by_id[post_id - 1] = None

    requests.delete(api + "posts/" + str(post_id))

    success()

    back_to_first_page()


def click_del():

    destroy()

    userid = Label(frame, text="Enter your user ID:")
    e_user = Entry(frame, width=20)

    post_id = Label(frame, text="Enter post ID:")
    e_pid = Entry(frame, width=20)

    submitt = Button(frame, text="Submit",
                     command=lambda: delete(e_user.get(), e_pid.get()))

    userid.grid(row=0, column=0, pady=25, padx=450)
    e_user.grid(row=1, column=0)

    post_id.grid(row=2, column=0, pady=25)
    e_pid.grid(row=3, column=0)

    submitt.grid(row=4, column=0, pady=25)

    back_to_first_page()


# Edit post functions

def edit_post(userid, post_id, title, body):

    for post in posts_by_userid[userid]:

        if post_id == post['id']:
            post['title'] = title.get()
            post['body'] = body.get(1.0, "end-1c")
            break

    posts_by_id[post_id - 1]['title'] = title.get()
    posts_by_id[post_id - 1]['body'] = body.get(1.0, "end-1c")

    requests.patch(api + "posts/" + str(post_id),
                   {"title": title.get(), "body": body.get(1.0, "end-1c")})

    success()


def update(userid, post_id, search):
    search.destroy()

    if not userid.isnumeric():
        invalid_uid()
        return

    if not post_id.isnumeric():
        invalid_pid()
        return

    userid = int(userid)
    post_id = int(post_id)

    try:
        posts_by_id[post_id - 1]

    except IndexError:
        nonexistent()
        return

    if posts_by_id[post_id - 1]['userId'] != userid:
        invalid = Label(frame, text="Unable to edit posts from other users")
        invalid.grid(row=10)
        return

    title = Label(frame, text="Edit title:")
    e_title = Entry(frame, width=40)
    e_title.insert(0, posts_by_id[post_id - 1]['title'])

    body = Label(frame, text="Edit text:")
    e_body = Text(frame, width=128, height=22)
    e_body.insert(END, posts_by_id[post_id - 1]['body'])

    submitt = Button(frame, text="Submit",
                     command=lambda: edit_post(userid, post_id,
                                               e_title, e_body))

    title.grid(row=4, column=0, pady=5)
    e_title.grid(row=5, column=0)

    body.grid(row=6, column=0, pady=5)
    e_body.grid(row=7, column=0)

    submitt.grid(row=8, column=0, pady=10)

    back_to_first_page()


def click_edit():

    destroy()

    userid = Label(frame, text="Enter your user ID:")
    e_user = Entry(frame, width=20)

    post_id = Label(frame, text="Enter post ID:")
    e_pid = Entry(frame, width=20)

    search = Button(frame, text="Search", command=lambda: update(
        e_user.get(), e_pid.get(), search))

    userid.grid(row=0, column=0, pady=5, padx=450)
    e_user.grid(row=1, column=0)

    post_id.grid(row=2, column=0, pady=5)
    e_pid.grid(row=3, column=0)

    search.grid(row=4, column=0, pady=15)

    back_to_first_page()


# Find post functions


def get_by_id(post_id):

    if not post_id.isnumeric():
        invalid_pid()
        return

    post_id = int(post_id)

    try:
        resp = posts_by_id[post_id - 1]

        if resp is None:
            invalid = Label(frame, text="This post was deleted")
            invalid.grid(row=10, column=1)
            return

    except IndexError:
        resp = requests.get(api + "posts/" + str(post_id)).json()

        if not bool(resp):
            nonexistent(1)
            return

        else:
            add_to_local(resp['userId'], resp['title'], resp['body'])

    show_body(resp)


def show_body(post):

    destroy()

    title = post['title']
    body = post['body']
    user = Label(frame, text="\n\nUser:\n\n" + str(post['userId']))
    post = Label(frame, text="\n\nPost:\n\n" + str(post['id']))
    title = Label(frame, text="\n\nTitle:\n\n" + title)
    body = Label(frame, text="\n\nBody:\n\n" + body)
    user.grid(row=0, padx=490)
    post.grid(row=1)
    title.grid(row=2)
    body.grid(row=3)

    back_to_first_page()


def get_by_userid(userid):

    if not userid.isnumeric():
        invalid_uid()
        return

    userid = int(userid)

    if userid not in posts_by_userid.keys():
        invalid = Label(frame, text="User with this ID does not exist",
                        pady=10, padx=50)
        invalid.grid(row=10, column=0)
        return

    destroy()

    list_of_posts = Text(frame, height=30, pady=30, padx=15)
    list_of_posts.grid(column=0, padx=180, pady=10)

    def button_update(posts):
        show_body(posts)

    for post in posts_by_userid[userid]:

        def func(x=post):

            return button_update(x)

        button = Button(text=post['title'], command=func)
        list_of_posts.window_create("end", window=button, pady=4)
        list_of_posts.insert("end", "\n")

    list_of_posts.configure(state="disabled")

    back_to_first_page()


def click_find():

    destroy()

    userid = Label(frame, text="Search by user ID:")
    e_user = Entry(frame, width=20)

    by_user = Button(frame, text="Search",
                     command=lambda: get_by_userid(e_user.get()))

    post_id = Label(frame, text="Search by post ID:")
    e_pid = Entry(frame, width=20)

    by_id = Button(frame, text="Search",
                   command=lambda: get_by_id(e_pid.get()))

    userid.grid(row=0, column=0, pady=25, padx=190)
    e_user.grid(row=1, column=0, pady=25, padx=190)

    by_user.grid(row=2, column=0, pady=25, padx=190)
    post_id.grid(row=0, column=1, pady=25, padx=190)

    e_pid.grid(row=1, column=1, pady=25, padx=190)
    by_id.grid(row=2, column=1, pady=25, padx=190)

    back_to_first_page(2)


# Initial window function


def initialize():

    destroy()

    choice = Label(frame, text="What would you like to do?")
    choice.grid(row=0, columnspan=4, pady=100, padx=425)

    add = Button(frame, text="Add post", command=click_add)
    delet = Button(frame, text="Delete post", command=click_del)
    edit = Button(frame, text="Edit post", command=click_edit)
    find = Button(frame, text="Find post", command=click_find)

    add.grid(row=1, column=0, padx=55)
    delet.grid(row=1, column=1, padx=55)
    edit.grid(row=1, column=2, padx=55)
    find.grid(row=1, column=3, padx=55)


# Loading data from api


def load():

    global posts_by_id
    posts_by_id = requests.get(api + "posts/").json()

    for entry in posts_by_id:

        try:
            posts_by_userid[entry['userId']].append(entry)

        except KeyError:
            posts_by_userid[entry['userId']] = [entry]


if __name__ == '__main__':

    root = Tk()
    root.geometry("1200x700+200+200")

    frame = Frame(root)
    frame.grid(rowspan=100, columnspan=4, padx=100)

    load()

    initialize()

    root.mainloop()

    # TODO: ? None, Responses
