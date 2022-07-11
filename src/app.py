from flask import Flask, request, jsonify, json
from pymongo import MongoClient
from jsonschema import validate
from requests import PostReqSchema, LikeReqSchema, CommentReqSchema
import datetime as dt

# Create REST-API using flask
app = Flask(__name__)


# Connect to mongodb.
cluster = MongoClient("mongodb+srv://rotem:Aa123456@cyberilliumcluster.ceo1ppf.mongodb.net/?retryWrites=true&w=majority")
db = cluster["db"]
posts = db["posts"]
comments = db["comments"]

    
### Post-Collection handler
def serielizePost(rec):
    rec['_id'] = str(rec['_id'])
    return rec

# Get all posts.
@app.route('/posts', methods=['GET'])
def get_all_posts():
    return jsonify([serielizePost(post) for post in posts.find()])

# Post a post (lolll). 
@app.route('/posts', methods=['POST'])
def add_post():
    try:
        # Pasrse request and check all fields are there.        
        req = json.loads(request.data)
        validate(instance=req, schema=PostReqSchema)

        # Inset to mongoDB.
        posts.insert_one({
            "content": req['content'],
            "username": req['username'],
            "timestamp": dt.datetime.now(),
            "likes_count": 0,
            "comments_count": 0
            
        })
        
        return ("post accepted", 200)
    except:
        print("Couldn't parse post request")
        return ("Bad post request", 400)
    


### Likes-Collection handler
@app.route('/posts/<id>/likes', methods=['POST'])
def add_like(id):
    try:
        # Pasrse request and check all fields are there.        
        req = json.loads(request.data)
        validate(instance=req, schema=LikeReqSchema)

        # Check the post exists.        
        if posts.find_one({'_id':ObjectId(id)}) == None:
            return ("Bad like request: no such post", 400)
            
        # Inc likes counter in mongo.
        posts.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$inc': {'likes_count': 1}},
        )
        
        return ("like accepted", 200)
    except:
        print("Couldn't parse like request")
        return ("Bad like request: wrong structure", 400)
        


    
### Comments-Collection handler
def serielizeComment(rec):
    rec.pop('_id')
    rec['post_id'] = str(rec['post_id'])
    return rec

# Get all comments.
@app.route('/comments', methods=['GET'])
def get_all_comments():
    return jsonify([serielizeComment(comment) for comment in comments.find()])


# Post a comment
@app.route('/posts/<id>/comments', methods=['POST'])
def add_comments(id):
    try:
        # Pasrse request and check all fields are there.        
        req = json.loads(request.data)
        validate(instance=req, schema=CommentReqSchema)

        # Check the post exists.        
        if posts.find_one({'_id':ObjectId(id)}) == None:
            return ("Bad comment request: no such post", 400)
            
        # Inc post's comments counter in mongo.
        posts.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$inc': {'comments_count': 1}},
        )
        
        # Inset comment to mongoDB.
        comments.insert_one({
            "content": req['content'],
            "comment_user": req['username'],
            "post_id": ObjectId(id),
            "post_user": posts.find_one({'_id':ObjectId(id)})['username'],
            "timestamp": dt.datetime.now()
        })
        
        return ("comment accepted", 200)
    except:
        print("Couldn't parse comment request")
        return ("Bad comment request: wrong structure", 400)
        
    

