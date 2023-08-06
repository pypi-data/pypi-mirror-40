import requests, json
from enum import Enum
import copy

from .patch import PatchManager

from .DataStore import Champion, Item, Map, Summoner, Icon, Rune

class ddragonFiles(Enum):
    champions="champion.json"
    championsFull="championFull.json"
    items="item.json"
    maps="map.json"
    summoners="summoner.json"
    icons="profileicon.json"
    runes="runesReforged.json"
    
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
cache = {}

class ddragon(metaclass=Singleton):
    
    BASE_URL = "http://ddragon.leagueoflegends.com/cdn/"
    
    def __init__(self, load=True, language="en_US", championFull=True, baseUrl=None, localDirectory=None, localVersions=None):
        self.language = language
        self.championFull = championFull
        
        if not baseUrl == None:
            self.BASE_URL = baseUrl
            
        self.LOCAL_DIRECTORY = localDirectory
        self.LOCAL_VERSIONS = localVersions
           
        
        self.version=None
        self.pm = None
        if load:
            self.setVersion()
            
    def setVersion(self, season=None, patch=None, version=None):
        if season==None or patch==None or version==None:
            if self.pm == None:
                self.pm = PatchManager(self.LOCAL_VERSIONS)
                
            self.version = self.pm.getVersion(season, patch, version)
        else:
            self.version = "{}.{}.{}".format(season,patch,version)
        self.loadAll()
            
    def loadAll(self):
        if self.championFull:
            self.load(ddragonFiles.championsFull)
        else:
            self.load(ddragonFiles.champions)
            
        
        self.load(ddragonFiles.items)
        self.load(ddragonFiles.maps)
        self.load(ddragonFiles.summoners)
        self.load(ddragonFiles.icons)
        self.load(ddragonFiles.runes)
    
    
    def load(self, file):
        
        if self.version in cache:
            if (file == ddragonFiles.champions or file == ddragonFiles.championsFull) and "championById" in cache[self.version]:
                self.championById = cache[self.version]["championById"]
                self.championByName = cache[self.version]["championByName"]
                return
                
            if file == ddragonFiles.items and "itemById" in cache[self.version]:
                self.itemById = cache[self.version]["itemById"]
                self.itemByName = cache[self.version]["itemByName"]
                return
        
            if file == ddragonFiles.maps and "mapById" in cache[self.version]:
                self.mapById = cache[self.version]["mapById"]
                self.mapByName = cache[self.version]["mapByName"]
                return
            
            if file == ddragonFiles.summoners and "summonersById =" in cache[self.version]:
                self.summonersById = cache[self.version]["summonersById"]
                self.summonersByName = cache[self.version]["summonersByName"]
                return
            
            if file == ddragonFiles.icons and "iconsById" in cache[self.version]:
                self.iconsById = cache[self.version]["iconsById"]
                return
            
            if file == ddragonFiles.runes and "runesById" in cache[self.version]:
                self.runesById = cache[self.version]["runesById"]
                self.runesByName = cache[self.version]["runesByName"]
                return
        else:
            cache[self.version] = {}
            
        if self.LOCAL_DIRECTORY == None:
            data = requests.get(self.BASE_URL + self.version + "/data/" + self.language +"/" + file.value).json()
        else:
            with open(self.LOCAL_DIRECTORY + self.version + "/data/" + self.language +"/" + file.value, "r") as f:
                data = json.load(f)
        
        if file == ddragonFiles.champions or file == ddragonFiles.championsFull:
            self.championById = {}
            self.championByName = {}
            
            for c in data["data"]:
                champion = Champion(data["data"][c])
                champion.setImageUrl(self.BASE_URL+ self.version + "/img/")
                
                self.championById[int(data["data"][c]["key"])] = champion
                self.championByName[data["data"][c]["name"]] = champion
                
            cache[self.version]["championById"] = copy.deepcopy(self.championById)
            cache[self.version]["championByName"] = copy.deepcopy(self.championByName)
                
        if file == ddragonFiles.items:
            self.itemById = {}
            self.itemByName = {}
            
            for i in data["data"]:
                item = Item(data["data"][i])
                item.setImageUrl(self.BASE_URL+ self.version + "/img/")
                
                self.itemById[int(i)] = item
                self.itemByName[data["data"][i]["name"]] = item
            
            cache[self.version]["itemById"] = copy.deepcopy(self.itemById)
            cache[self.version]["itemByName"] = copy.deepcopy(self.itemByName)
                
        if file == ddragonFiles.maps:
            self.mapById = {}
            self.mapByName = {}
            
            for i in data["data"]:
                m = Map(data["data"][i])
                m.setImageUrl(self.BASE_URL+ self.version + "/img/")
                
                self.mapById[int(i)] = m
                self.mapByName[data["data"][i]["MapName"]] = m
                
            cache[self.version]["mapById"] = copy.deepcopy(self.mapById)
            cache[self.version]["mapByName"] = copy.deepcopy(self.mapByName)
            
        if file == ddragonFiles.summoners:
            self.summonersById = {}
            self.summonersByName = {}
            
            for s in data["data"]:
                summ = Summoner(data["data"][s])
                summ.setImageUrl(self.BASE_URL+ self.version + "/img/")
                
                self.summonersById[int(data["data"][s]["key"])] = summ
                self.summonersByName[data["data"][s]["name"]] = summ
                
            cache[self.version]["summonersById"] = copy.deepcopy(self.summonersById)
            cache[self.version]["summonersByName"] = copy.deepcopy(self.summonersByName)
            
        if file == ddragonFiles.icons:
            self.iconsById = {}
            
            for i in data["data"]:
                icon = Icon(data["data"][i])
                icon.setImageUrl(self.BASE_URL+ self.version + "/img/")
                
                self.iconsById[int(i)] = icon
                
            cache[self.version]["iconsById"] = copy.deepcopy(self.iconsById)
        
        if file == ddragonFiles.runes:
            self.runesById = {}
            self.runesByName = {}
            
            for tree in data:
                for slot in tree["slots"]:
                    for r in slot["runes"]:
                        rune = Rune(r)
                        rune.setImageUrl(self.BASE_URL+ "img/")

                        self.runesById[int(r["id"])] = rune
                        self.runesByName[r["name"]] = rune
                
            cache[self.version]["runesById"] = copy.deepcopy(self.runesById)
            cache[self.version]["runesByName"] = copy.deepcopy(self.runesByName)
            
    def getChampion(self, champion):
        if isinstance(champion, int) or champion.isdigit():
            return self.championById[int(champion)]
        else:
            return self.championByName[champion]
        
    def getItem(self, item):
        if isinstance(item, int) or item.isdigit():
            return self.itemById[int(item)]
        else:
            return self.itemByName[item]
        
    def getMap(self, m):
        if isinstance(m, int) or m.isdigit():
            return self.mapById[int(m)]
        else:
            return self.mapByName[m]
        
    def getSummoner(self, s):
        if isinstance(s, int) or s.isdigit():
            return self.summonersById[int(s)]
        else:
            return self.summonersByName[s]
        
    def getIcon(self, icon):
        return self.iconsById[int(icon)]
    
    def getRune(self, r):
        if isinstance(r, int) or r.isdigit():
            return self.runesById[int(r)]
        else:
            return self.runesByName[r]
        
    def withVersion(self, season=None, patch=None, version=None):
        inst = copy.copy(self)
        inst.setVersion(season, patch, version)
        return inst