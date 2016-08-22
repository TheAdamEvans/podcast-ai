
# coding: utf-8

# In[1]:

import os
import pickle
import time
from random import uniform

import pandas as pd
from urllib2 import urlopen
from bs4 import BeautifulSoup


# In[27]:

class Scraper(object):
    """ Opens the webpage and retains information """

    def __init__(self, episode_number):
        self.episode_number = episode_number
        
        try:
            page = urlopen('http://www.thisamericanlife.org/radio-archives/episode/'+ episode_number +'/transcript')
        except:
            print episode_number + ' failed to LOAD!'
            self.soup = None
        else:
            try:
                html = page.read()
            except:
                print episode_number + ' failed to READ!'
                self.soup = None
            else:
                self.soup = BeautifulSoup(html, 'html.parser')

    def get_episode(self):
        # main object of interest on transcript page
        wrapper = self.soup.find('div', {'class': 'radio-wrapper'})
        
        if wrapper:
            # information about the episode
            title = wrapper.h2.a.get_text()
            print title
            # originally_aired = wrapper.find('div', {'class': 'radio-date'}).get_text()

            # acts are in separate divs
            act_table = wrapper.find_all('div', {'class': 'act'})

            collect = []
            for act in act_table:

                act_title = act.h3.get_text()
                act_type = act['id']
                act_inner = act.find('div', {'class': 'act-inner'})

                for speaker in act_inner.find_all('div'):
                    if speaker.h4:
                        speaker_name = speaker.h4.get_text().strip()
                    else:
                        speaker_name = ''
                    speaker_class = speaker['class'][0]

                    for segment in speaker.find_all('p'):
                        begin = segment['begin']
                        text = segment.get_text()
                        # print speaker_name, speaker_class, begin, text[:50]

                        speech = (episode_number, title, act_type, speaker_name, speaker_class, begin, text)
                        collect.append(speech)

            cols = ['episode_number', 'title', 'act_type', 'speaker_name', 'speaker_class', 'begin', 'text']
            episode = pd.DataFrame.from_records(collect, columns = cols)
            return episode


# In[42]:

def save_info_from(episode_number, data_dir):

    # check if we have already crawled this
    OBJECT_OUTFILE = data_dir + episode_number + '.pickle'
    if os.path.exists(OBJECT_OUTFILE):
        print episode_number + ' has already been crawled'
        pass
    else:
        if not os.path.isdir(os.path.dirname(OBJECT_OUTFILE)):
            os.makedirs(os.path.dirname(OBJECT_OUTFILE))
        
        # wait a hot second
        delay = uniform(1,5)
        time.sleep(delay)
    
        # scrape episode info
        scrap = Scraper(episode_number)
        if scrap.soup:
            # harvest information
            episode = scrap.get_episode()

            # save object as pickle
            with open(OBJECT_OUTFILE, 'wb') as handle:
                pickle.dump(episode, handle)


# In[43]:

data_dir = '/Users/adam/audio/data/'

# latest episode as of august 2016
episode_number = '596'

while int(episode_number) >= 1:
    # grab the info
    save_info_from(episode_number, data_dir)
    
    # episode counter
    episode_number = str(int(episode_number) - 1)
#     if episode_number == '590':
#         break


# In[44]:

def combine_pickle(DATA_DIR):
    """ Combines directory of pickled episode objects into a single DataFrame """
    
    collect = []
    for epi in os.listdir(DATA_DIR):
        pkl = '.pickle'
        if epi[-len(pkl):] != pkl:
            pass
        else:
            partial = pickle.load(open(DATA_DIR + epi, 'rb'))
            if partial is not None:
                print 'Found %d segments in %s' % (partial.shape[0], epi)
            collect.append(partial)
    episode = pd.concat(collect, axis=0)

    return episode


# In[45]:

tal = combine_pickle(data_dir)


# In[46]:

tal.columns


# In[47]:

x = tal.speaker_name.unique()


# In[48]:

tal.shape


# In[50]:

import sys
sys.getsizeof(tal)


# In[52]:

len(tal['episode_number'].unique())


# In[ ]:



