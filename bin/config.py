# TODO: cannot be overwritten on file by using hardcoded config -- needs to be exported as JSON or similar

# Contains configurations for the app, used regardless of project.
app_configs = {
    "debug": True,

    # defaults
    "beadHeight": 22,
    "beadWidth": 12,
}

# Contains configurations for the project, used for each project.
project_configs = {
    "width": 10,
    "height": 12,
    "defaultOrientation": "Vertical"
}