import docker

client = docker.from_env()


def create_docker_file(python_version, python_code):
    dockerfile_content = f"""
        # Use an official Python runtime as a parent image
        FROM python:{python_version}-slim

        # Set the working directory in the container
        WORKDIR /usr/src/app

        RUN echo "{python_code}" > script.py

        # Run script.py when the container launches
        CMD ["python", "./script.py"]
        """
    with open("Dockerfile", "w") as dockerfile:
        dockerfile.write(dockerfile_content)


def build_image():
    image, logs = client.images.build(path=".", tag="python-script")
    print("Getting container logs . . .")
    for log in logs:
        print(log.get("stream", "").strip())
    return image


def get_container(container_name):
    try:
        container = client.containers.get(container_name)
        return container
    except docker.errors.NotFound:
        return False


def run_container(image_id):
    container_name = "python-script-container"
    checked_container = get_container(container_name)
    if not checked_container:
        return client.containers.run(image_id, name=container_name, detach=True)
    if checked_container.status == "running":
        checked_container.stop()
    checked_container.remove()

    return client.containers.run(image_id, name=container_name, detach=True)


def run_in_container(python_version, python_code):
    print(f"One moment please, preparing a container for your code in python {0}", python_version)
    create_docker_file(python_version, python_code)
    image = build_image()
    print(f"Created a new python image {0}", image.id)
    container = run_container(image.id)
    if container.status == 'running':
        print(f"Container running {container.id}")
    else:
        print(f"Container {container.id} is not running, trying to start")
        container.start()
        print("Container started")
        print(f"Container logs \n{container.logs().decode("utf-8")}")
