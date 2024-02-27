import uuid
import flask 
import pathlib
import mindriver

# files save and delete======================================
def save_file():
    """Help save file."""
    # Unpack flask object
    fileobj = flask.request.files["file"]
    filename = fileobj.filename
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    uuid_basename = f"{stem}{suffix}"
    # Save to disk
    path = mindriver.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    return uuid_basename