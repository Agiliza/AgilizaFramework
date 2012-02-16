from agiliza.core.files.storage import FileSystemStorage


def get_storage(request):
    return FileSystemStorage()
