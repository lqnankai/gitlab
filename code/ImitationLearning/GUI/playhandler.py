'''
Created on 2016.7.5

@author: liangqian
'''
import tornado.web
from GUI.globaldata import brainEngine
class PlayHandler(tornado.web.RequestHandler):
    '''
    This class is used to handle the music learning requests.
    '''

    def get(self):
        ll = self.get_arguments("State")
        CurrentState = ll[0]
        print(ll)
        l1 = self.get_argument("goalname")
        print(l1)
        l2 = self.get_arguments("episode")
        print(l2)
        if(CurrentState == "Remember"):
            jStr = brainEngine.rememberMusic(l1)
            self.write(jStr)
        if(CurrentState == "Recall"):
            jStr = brainEngine.recallMusic(l1)
            self.write(jStr)
        if(CurrentState == "EpisodeRecall"):
            strs = l2[0].split(",")
            episodeNotes = []
            for i in range(0,len(strs)-1):
                episodeNotes.append(int(strs[i]))
            jStr = brainEngine.recallEpisode(episodeNotes)
            self.write(jStr)
            
            