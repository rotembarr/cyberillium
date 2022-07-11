PostReqSchema = {
    "type": "object",
    "properties" : {
        "content": {"type" : "string"},
        "username": {"type" : "string"},
    },
    "required": ["content", "username"],
    "additionalProperties": False
}

LikeReqSchema = {
    "type": "object",
    "properties" : {
        "username": {"type" : "string"},
    },
    "required": ["username"],
    "additionalProperties": False
}


CommentReqSchema = {
    "type": "object",
    "properties" : {
        "username": {"type" : "string"},
        "content": {"type" : "string"},
    },
    "required": ["content", "username"],
    "additionalProperties": False
}
