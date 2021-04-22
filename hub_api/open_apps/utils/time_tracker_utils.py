def get_archived_time_tracker_name_items(request):
    archived = request.query_params.get('archived', None)
    if archived:
        return True
    return False
