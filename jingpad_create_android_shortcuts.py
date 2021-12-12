import subprocess
import os

def format_console_output(output):
    clean_output = output.replace("b'", "")
    list=[]
    for ent in clean_output.split(r"\n"):
        list.append(ent.strip())
    list.pop()
    return list

def get_android_apps_package():
    list=[]
    for app in format_console_output(str(subprocess.check_output(['japm', 'list']))):
        list.append(app.split(" ")[0])
    return list

def get_android_app_details():
    list=[]
    for package in get_android_apps_package():
        list.append(format_console_output(str(subprocess.check_output(['japm', 'show', package]))))
    return list

def find_app_to_shorcut():
    existing=[]
    for file in os.listdir("/usr/share/applications"):
        name=os.path.splitext(file)[0]
        existing.append(name)
    to_create=[]
    for app in get_android_app_details():
        if app[0].lower() in existing or app[1].lower() in existing:
            pass
        else:
            to_create.append(app)
    return to_create

def create_desktop_file(name, package, version):
    low_name = name.lower()
    filepath =  os.path.join("/usr/share/applications/", low_name+".desktop")
    with open(filepath, 'x') as f:
        f.write("[Desktop Entry] \n")
        f.write("Name=%s\n" % name)
        f.write("Comment=Android application %s\n" % package)
        f.write("Version=%s\n" % version)
        f.write("Exec=%s\n" % package)
        f.write("Type=Application\n")
        f.write("Terminal=false\n")
        f.write("Icon=%s" % name + ".png\n")
        f.write("Categories=Android;")

missing=False
for f in find_app_to_shorcut():
    print("Creating desktop file for %s" % f[0])
    print("Expected icon : %s.png" % f[0])
    create_desktop_file(f[0], f[1], f[2])
    missing=True
if missing:
    print("Missing android app shortcuts created")
    icon_path = "/usr/share/icons/hicolor/scalable/app/"
    print("You can add their icon in %s" % icon_path)
else:
    print("No missing android app shortcut")