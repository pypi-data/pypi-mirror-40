def upload_to(slug, file_name):
    return f"posts/{slug}/{file_name}"


def photo_upload_to(instance, file_name):
    return upload_to(instance.slug, file_name)


def post_photo_upload_to(instance, file_name):
    return upload_to(instance.post.slug, file_name)
