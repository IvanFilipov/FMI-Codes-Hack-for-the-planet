import logging
import os
from scp import SCPClient
import paramiko
from time import sleep


HOST = '192.168.2.105'
REMOTE_IMAGES_DIR = '/home/pi/Downloads/fmi-wall-e/camera/images/'
IMAGES_DIR = '/home/pi/Downloads/test/images/'
print("test")
def get_ssh_connection():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # TODO: use env variables instead of this disaster.
        print('SSH-ing...')
        ssh.connect(HOST,
                    username='pi',
                    password='raspberry',
                    allow_agent=False,
                    look_for_keys=False)
        return ssh
    except Exception as e:
        sleep(300)
        # Trying forever
        print('SSH-ing not successful, trying again...')
        return get_ssh_connection()

    return ssh


def get_most_recent_image_dir(ssh):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls {}'.format(REMOTE_IMAGES_DIR))
    images = list(ssh_stdout)
    image_name = sorted(images, reverse=True)[0].strip()
    return os.path.join(REMOTE_IMAGES_DIR, image_name), image_name

def get_3_most_recent_images_dir(ssh):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('ls {}'.format(REMOTE_IMAGES_DIR))
    images = list(ssh_stdout)
    images_names = sorted(images, reverse=True)
    result_images = list();
    result_images.append(os.path.join(REMOTE_IMAGES_DIR, images_names[0]).strip())
    result_images.append(os.path.join(REMOTE_IMAGES_DIR, images_names[1]).strip())
    result_images.append(os.path.join(REMOTE_IMAGES_DIR, images_names[2]).strip())
    print(result_images)
    return result_images


def get_images():
    # return '/home/desi/Downloads/1553347394.jpeg'
    # The ssh key of the computer should be added to the raspberry already!
    # use ssh-copy-id beforehand.
    ssh = get_ssh_connection()

    most_recent_images = get_3_most_recent_images_dir(ssh)
    
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(most_recent_images[2], os.path.join(IMAGES_DIR, 'center.jpeg'))
        scp.put(most_recent_images[1], os.path.join(IMAGES_DIR, 'left.jpeg'))
        scp.put(most_recent_images[0], os.path.join(IMAGES_DIR, 'right.jpeg'))
        #scp_client.put(srcfile, destfile, recursive=True)
        #scp.get(most_recent_images[0])
    
#    image_dir = os.path.join(os.getcwd(), IMAGES_DIR, "image_center.jpeg")
#    logging.info('Storing image to: {}'.format(image_dir))
    return most_recent_images


if __name__ == "__main__":
    #model, visualize = model_initializer.load_model()

    # Somehow we have to know whether
    # Wall-E has collected the trash.
    #while True:
    images = get_images()
    print(images)
        #for img in images
        #print('Processing image: {}'.format(images))
        # mask = get_mask(model, image_dir, visualize)
        # distance_to_object = distance_computer.get_distance()

        # move_commands = move(mask)
        # ssh = None
        # for move_command, arg in move_commands:
        #     ssh = move_remote(move_command, arg)
        #     logging.info('Command for the movement {} with args {}'.format(move_command, arg))
        #     print('Command for the movement {} with args {}'.format(move_command, arg))

        # if move_commands[-1] == (MOVE_CLAW, CLOSE):
        #     break

