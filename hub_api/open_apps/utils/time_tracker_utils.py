from open_apps.models.time_tracker import TrackTimeName


def get_archived_time_tracker_name_items(request):
    archived = request.query_params.get('archived', None)
    if archived:
        return True
    return False


def create_default_break_name(request):
    TrackTimeName.objects.get_or_create(user=request.user, name="Break")
