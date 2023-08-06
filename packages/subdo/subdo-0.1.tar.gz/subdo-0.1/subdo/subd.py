import os, hashlib, sys, urllib.request

movie_extensions = ["avi", "mp4", "mkv", "wmv", "mov", "flv"]

movie_folder = sys.argv[1]
# path = 'E:\\Downloads\\Movies\\The Stepfather (2009) 1080p BrRip x264 - VPPV'
# movie_folder = path

def get_hash(name):
    #this hash function receives the name of the file and returns the hash code
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

def main():

    files = getFiles(movie_folder)

    for exis_files in files:
        # print ("Opening {0} ...".format(file))
        hash_key = get_hash(exis_files)
        exists = check_srt(exis_files)
        success = 0

        if exists:
            print("Subtitles already exist for the file.")
        else:
            subtitle, status = getSubtitle(hash_key)

            if (status == False):
                print("No subtitle found for the file {}".format(exis_files))
            else:
                createSRT(subtitle, exis_files)
                success+=1

                print("Subtitle was successfully downloaded for {} files".format(success))

def getFiles(path):

    existing_video=[]

    for (root,dirs,files) in os.walk(path):
        # print ("Roots: \n", root)
        # print ("Dirs: \n", dirs)
        # print ("Files: \n", files)
        # print ('--------------------------------')
        for name in files:
            if(name.split(".")[-1] in movie_extensions):
                existing_video.append(os.path.join(root, name))

    return existing_video

def check_srt(file):
    file = file.replace(file.split(".")[-1], "srt")
    if(os.path.exists(file)):
        return True
    else:
        return False

def createSRT(subtitle, exis_files):
    exis_files = exis_files.replace(exis_files.split(".")[-1], "srt")
    new = open(exis_files, 'wb')
    new.write(subtitle)
    new.close()
    return True

def getSubtitle(hash_key):

    user_agent = ['user-agent', 'SubDB/1.0 (Video Subtitle Downloader; http://github.com/kevalvc)']
    url = 'http://api.thesubdb.com/?action=download&hash=' + hash_key + '&language=en'
    error_code = ""

    try:
        request = urllib.request.Request(url, data=None)
        request.add_header(user_agent[0], user_agent[1])
        response = urllib.request.urlopen(request).read()
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        # ...
        error_code = '{}'.format(e.code)
        # print(error_code)
    # except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        # ...
    #     print('URLError: {}'.format(e.reason))
    # else:
    #     # 200
    #     # ...
    #     print('good')

    if ((error_code == '404') or (error_code == '400') ):
        return False, False
    else:
        return response, True


if __name__ == '__main__':
    main()
