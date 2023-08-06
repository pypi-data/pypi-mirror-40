# videosplit module
# Given a video path, it uses ffmpeg to extract relevant frames
import os, subprocess, re
class VideoSplitException(Exception):
    pass

# ffmpeg -ss 3 -i Michael\ Cohen\ to\ testify\ publicly\ before\ Congress-kWDyr0ewJaQ.mp4 -vf "select=gt(scene\,0.1)" -vsync vfr temp%02d.jpg
# works?
class VideoSplit():
    def __init__(self):
        # TODO: Add timestamps to the video.
        """
        Wrapper utility to interact with ffmpeg.
        """
        _, err = self._execute(['ffmpeg','-version'])
        if err is not '':
            raise VideoSplitException("ffmpeg is not installed: {}".format(err))

    def _execute(self, arguments):
        """
        Executes an ffmpeg command as a subprocess.
        """
        args = []
        args.extend(arguments)
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
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

        command = ['ffmpeg', '-i', videopath, '-vf', 'select=eq(pict_type\,I)', '-vsync', '2', "{}%02d.jpg".format(output_name) ]
        out, err = self._execute(command)
        filenames  = self._get_filenames(output_name, 'jpg')
        return filenames
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
        seconds = info['time']
        denominator= int(int(seconds)/n) #ffmpeg requires the denominator to be an integer
        return self.get_interval(videopath, denominator, output_name)


    def get_interval(self, videopath, interval, output_name=None):
        """
        Get frames of the video from a given interval
        Arguments:
            videopath (str) : The path to the video
            interval (int) : The length of the interval in seconds.
            output_name (str) (optional) : The prefix of the jpg files to create.
        Returns:
            list : The filenames of the jpg files created.
        """
        if output_name is None:
            output_name = self._create_prefix(videopath)

        command = ['ffmpeg', '-ss', '3', '-i', videopath, '-vf', 'fps=1/{}'.format(interval), "{}%02d.jpg".format(output_name)]
        out, err= self._execute(command)
        _ = out if out is not "" else err
        if len(err) > 1:
            if 'No such file or directory' in err:
                raise VideoSplitException("No such file or directory", err)
        # ffmpeg does not return any relevant information.
        filenames = self._get_filenames(output_name, '.jpg')
        return filenames

    def _get_filenames(self, regex, extension):
        """ Finds files of a given extension based on a regex"""
        ls, err = self._execute(['ls'])
        ls = ls.split('\n')
        file_names = []
        for file in ls:
            if extension in file:
                file_names.append(file)
        return file_names

    def _create_prefix(self,videopath):
        title = videopath.split('.')
        title = title[-2]
        if '/' in title:
            title = title.split('/n')[-1]

        output_name = 'tmp_{}'.format(title)
        return output_name


if __name__ == "__main__":
    ffmpeg = VideoSplit()
    frames = ffmpeg.get_n_frames("Watch President Trump's Full Immigration Address And Response From Democrats _ NBC News-H7eA1K4j8GU.f137.mp4", 1)
    print(frames)