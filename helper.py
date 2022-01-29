def parse_comments(comments):
    '''
    comment row structure [(comment_id, project_id, commenter_id, commenter_username, message)]
    '''
    comments_list = []
    if comments:
        for c in comments:
            comments_list.append({
                "comment_id": c[0],
                "commenter_id": c[2],
                "commenter_username": c[3],
                "message": c[4]
            })

    return comments_list
