from tables import (IsDescription,
                    StringCol,
                    Int32Col,
                    UInt32Col,
                    UInt8Col,
                    UInt16Col,
                    Time32Col)
import tables as tb
import xml.etree.ElementTree as ET
import string
import numpy


class User(IsDescription):
    id = Int32Col()
    name = StringCol(16)
    age = UInt8Col()
    reputation = UInt16Col()
    creation_date = Time32Col()
    views = UInt16Col()
    upvotes = UInt16Col()
    downvotes = UInt16Col()


class Vote(IsDescription):
    id = Int32Col()
    post_id = UInt32Col()
    vote_type_id = UInt8Col()
    creation_date = Time32Col()


class Post(IsDescription):
    id = Int32Col()
    post_type_id = UInt8Col()
    parent_id = UInt32Col()
    accepted_answer_id = UInt32Col()
    creation_date = Time32Col()
    score = UInt32Col()
    viewcount = UInt32Col()
    owner_user_id = UInt32Col()
    answer_count = UInt16Col()
    favorite_count = UInt16Col()
    tags = StringCol(itemsize=25, shape=(5,))


def process_users(table, xml):
    tree_iter = ET.iterparse(xml)
    user = table.row
    for event, e in tree_iter:
        if e.tag != "row":
            continue
        user['id'] = e.get("Id")
        user['name'] = e.get("DisplayName")
        user['age'] = e.get("Age", -1)
        user['reputation'] = e.get("Reputation")
        user['creation_date'] = e.get("CreationDate")
        user['view'] = e.get("Views")
        user['upvotes'] = e.get("UpVotes")
        user['downvotes'] = e.get("DownVotes")
        user.append()


def process_posts(table, xml):
    tree_iter = ET.iterparse(xml)
    post = table.row
    for event, e in tree_iter:
        if e.tag != "row":
            continue
        post['id'] = e.get("Id")
        post['post_type_id'] = e.get("PostTypeId")
        post['parent_id'] = e.get("ParentId", -1)
        post['accepted_answer_id'] = e.get("AcceptedAnswerId", -1)
        post['creation_date'] = e.get("CreationDate")
        post['score'] = e.get("Score")
        post['viewcount'] = e.get("ViewCount", 0)
        post['owner_user_id'] = e.get("OwnerUserId")
        post['answer_count'] = e.get("AnswerCount", 0)
        post['favorite_count'] = e.get("FavoriteCount", 0)
        # Parse tags
        i = 0
        s = e.get["Tags"]
        num = 0
        while True:
            i = string.find(s, '&lt;', i)
            if i == -1:
                break
            end = string.find(s, '&gt;', i)
            # Add the tag into the tag array
            post['tags'][num] = string.substr(s, i+4, end)
            # Skip past the gt
            i = end + 3
            num += 1
        post.append()


def process_votes(table, xml):
    tree_iter = ET.iterparse(xml)
    vote = table.row
    for event, e in tree_iter:
        if e.tag != "row":
            continue
        vote['id'] = e.get("Id")
        vote['post_id'] = e.get("PostId")
        vote['vote_type_id'] = e.get("VoteTypeId")
        vote['creation_date'] = e.get("CreationDate")
        vote.append()


def preprocess_to_hdf5(directory):
    h5file = tb.openFile("overflow.h5",
                         mode="w",
                         title="InfoOverflow Visualization Data ")
    user_table = h5file.createTable("/", 'users', User, 'User information')
    post_table = h5file.createTable("/", 'posts', Post, 'Post information')
    vote_table = h5file.createTable("/", 'votes', Vote, 'Vote information')
    process_users(user_table, directory + "/users.xml")
    process_posts(post_table, directory + "/posts.xml")
    process_votes(vote_table, directory + "/votes.xml")
    user_table.flush()
    post_table.flush()
    vote_table.flush()
    print "Finished preprocessing, data stored in overflow.h5"
