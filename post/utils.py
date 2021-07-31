from .models import PostModel

def getPostCount(id = None):
    if not id:
        return 0
    posts = PostModel.objects.filter(posted_by=id)
    return len(posts)