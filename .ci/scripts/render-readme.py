import os
import requests
import yaml

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader(".ci/templates"),
    autoescape=select_autoescape()
)

def load_metadata_file(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

# TODO: remove hard-coded repo owner
def get_latest_image(name):
    r = requests.get(
        f"https://api.github.com/users/rafaribe/packages/container/{name}/versions",
        headers={
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "token " + os.environ["GITHUB_TOKEN"]
        },
    )
    if r.status_code != 200:
        print(f"Failed to get versions for {name}: {r.status_code}: {r.text}")
        return None
    data = r.json()
    for image in data:
        tags = image["metadata"]["container"]["tags"]
        if "latest" in tags:
            return image
    print(f"Couldn't find latest tag for {name}")
    return None

if __name__ == "__main__":
    base_images = []
    app_images = []
    for subdir, dirs, files in os.walk("./apps"):
        for file in files:
            if file != "metadata.yaml":
                continue
            meta = load_metadata_file(os.path.join(subdir, file))
            for channel in meta["channels"]:
                name = ""
                if channel.get("stable", False):
                    name = meta["app"]
                else:
                    name = "-".join([meta["app"], channel["name"]])
                image = {
                    "name": name,
                    "channel": channel["name"],
                    "html_url": ""
                }
                gh_data = get_latest_image(name)
                if gh_data is not None:
                    image["html_url"] = f"https://github.com/rafaribe/container-images/pkgs/container/{name}"
                    image["tags"] = sorted(gh_data["metadata"]["container"]["tags"])
                if meta["base"]:
                    base_images.append(image)
                else:
                    app_images.append(image)

    template = env.get_template("README.md.j2")
    with open("./README.md", "w") as f:
        f.write(template.render(base_images=base_images, app_images=app_images))
