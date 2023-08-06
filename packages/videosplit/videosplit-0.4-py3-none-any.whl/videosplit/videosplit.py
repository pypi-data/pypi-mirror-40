# videosplit module
# Given a video path, it uses ffmpeg to extract relevant frames
import os, subprocess, re, ntpath
class VideoSplitException(Exception):
    pass

# ffmpeg -ss 3 -i Michael\ Cohen\ to\ testify\ publicly\ before\ Congress-kWDyr0ewJaQ.mp4 -vf "select=gt(scene\,0.1)" -vsync vfr temp%02d.jpg
# works?
class VideoSplit():
    def __init__(self, debug = False):
        # TODO: Add timestamps to the video.
        """
        Wrapper utility to interact with ffmpeg.
        """
        self.debug = debug
        _, err = self._execute(['ffmpeg','-version'])
        if err is not '':
            raise VideoSplitException("ffmpeg is not installed: {}".format(err))

    def _execute(self, arguments,shell=False):
        """
        Executes an ffmpeg command as a subprocess.
        """
        if self.debug:
            print("Running cmd: ",arguments)
        if not shell:
            args = []
            args.extend(arguments)
        else:
            args = arguments
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
        out, err = process.communicate()
        if self.debug:
            print("Out: ", out)
            print("Error: ", err)
        return out, err

    def _get_video_info(self, videopath):
        """ Returns information about the video, such as duration
            Arguments:
                videopath (str) : location of the video.
            Returns:
                dict : the time and fps of the video.
        """
        command = ['ffmpeg', '-i', videopath]
        out, err = self._execute(command)
        # ffmpeg requires an output file, so it will throw an error. However, it still
        # outputs the relevant information


        info = out if len(out) > 1 else err
        if "No such file or directory" in info:
            raise VideoSplitException('No such file or directory:\n{}'.format(info))
        
        time = re.search(r'Duration: \d\d:\d\d:\d\d', info).group(0)[10:]
        time = ((360 * int(time[:2])) + (60 * int(time[3:5])) + int(time[6:]))
        try:
            fps = re.search(r'\d\d.\d\d fps', info).group(0)[0:6]
        except AttributeError:
            fps = 30 # default to 30fps if not found.


        return {'time': time, 'fps': fps}

    def get_relevant(self,videopath,output_name=None):
        """
        Returns the representative frames of the video.
        The representative frames of the video will be the I-Frames of the video.
        Arguments:
            videopath (str) : The path to the file
            output_name (str) (optional): prefix of the jpg output wanted
        Returns:
            list : The filenames of the jpg files created.
        """
        if output_name is None:
            output_name = self._create_prefix(videopath)

        command = ['ffmpeg', '-i', videopath, '-vf', 'select=eq(pict_type\,I)', '-vsync', '2', "{}.jpg".format(output_name) ]
        out, err = self._execute(command, shell=True)
        filenames  = self._get_filenames(output_name, 'jpg')
        return self._create_timestamps(filenames, self._get_video_info(videopath).get('time'))
    def get_n_frames(self,videopath, n, output_name=None):
        """
        Splits a video into n frames.
        Returns the filenames of the jpg files created.

        Arguments:
            videopath (str) : location of the video
            n (int) : number of frames needed,
            output_name (int) (optional) : name of the jpg files
        Returns:
            list : filenames of the jpg files created.
        """
        if output_name == None:
            output_name = self._create_prefix(videopath)

        info = self._get_video_info(videopath)
        frames = info['time'] * info['fps']
        if frames < n:
            #need an error for if requesting more frames than there are
            raise ValueError
        rate= int(n/info['time'])
        return self.get_interval(videopath, n, info['time'], output_name)


    def get_interval(self, videopath, frames, seconds, output_name=None):
        """
        Get frames of the video from a given interval
        Arguments:
            videopath (str) : The path to the video
            interval (int) : The length of the interval in frames.
            output_name (str) (optional) : The prefix of the jpg files to create.
        Returns:
            list : The filenames of the jpg files created.
        """
        if output_name is None:
            output_name = self._create_prefix(videopath)

        command = ['ffmpeg', '-i', videopath, '-vf', "fps={}/{}".format(frames, seconds), "-vsync",  "vfr", "{}_%03d.jpg".format(output_name)]
        path = ntpath.dirname(output_name)
        mkdir = ['mkdir', path]
        out, err = self._execute(mkdir)
        cmd = " ".join(command)
        out, err= self._execute(cmd, shell=True)
        _ = out if out is not "" else err
        if len(err) > 1:
            if 'No such file or directory' in err:
                raise VideoSplitException("No such file or directory", err)
        # ffmpeg does not return any relevant information.
        filenames = self._get_filenames("*", '.jpg', path)
        return self._create_timestamps(filenames, self._get_video_info(videopath).get('time'))

    def _get_filenames(self, regex, extension, path=None):
        """ Finds files of a given extension based on a regex"""
        if path:
            ls, err = self._execute(" ".join(['ls', path]), shell=True)
        else:
            ls, err = self._execute(['ls'])
        ls = ls.split('\n')
        file_names = []
        for file in ls:
            if extension in file:
                if path is not None:
                    file = path + "/" + file
                file_names.append(file)
        return file_names

    def _create_prefix(self,videopath):
        path = ntpath.dirname(videopath)
        name, _ = ntpath.basename(videopath).split(".")
        return "{}/{}/frame".format(path, name)

    def _create_timestamps(self, filenames, time):
            if type(time) != int or type(time) != float:
                time = int(time)
            timestamps = {}
            n = 0
            if len(filenames) == 0:
                return {k: 0 for k in filenames}
            delta = time / len(filenames)
            for file in filenames:
                timestamps[file] = n
                n += delta
            return timestamps
if __name__ == "__main__":
    pass

