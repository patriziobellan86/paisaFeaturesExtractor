# -*- coding: utf-8 -*-
"""
@author: Patrizio
"""

from __future__ import unicode_literals
from __future__ import division

import codecs
import os
import collections

import glob
import pickle


class InfoProgramma (object):
    def Version (self):
        return "Versione 0.1.a"
    def Author (self):
        return "Patrizio Bellan\n patrizio.bellan@gmail.com"

##############################################################################
##############################################################################
##############################################################################        
    
class GenericTools (InfoProgramma):
    def __init__ (self):
        super (GenericTools, self).__init__ ()        

#Text File
    #READ INPUT FILE        
    def LoadFile(self, fileIn):
        r"""
            Questo metodo carica un file testuale
            
            :param str fileIn: path file
            :return: il testo del file
            :rtype: uncode(str)
        """
        try:
            with codecs.open(fileIn, "r", "utf-8") as f:
                return f.readlines()
                
        except IOError:
            return False
    
    
    #SALVO I DATI IN UN FILE
    def SaveFile(self, dati, filename):
        r"""
            Questo metodo salva il file testuale
            :param list dati: dati
            :param str filename: path file
        """
        
        with codecs.open (filename, "a", "utf-8") as f:
            f.writelines (dati)
                       
            
#Byte File
    def SaveByte(self, dati, filename):
        r"""
            Questa funzione registra un pickle
            
            :param pckl_data dati: dati
            :param str filename: path file   
        """
        
        try:
            os.remove(filename)
        except:
            pass
        try:        
            out = open(filename,"wb")
            pickle.dump(dati, out)
            out.close()
            return True
            
        except:
            return False
            
            
    def LoadByte(self,filename):
        try:
            in_s=open(filename,'rb')
            dati=pickle.load(in_s)
            in_s.close()
            
            return dati   
            
        except IOError:
            return False

                  
    def DelAllFiles(self, folder, escludeExt = False):
        r"""
            Questo metodo elimina tutti i files in una cartella
            ESCLUSI quelli con estensione "escludeExt"
            
            
        """
        files=glob.glob(folder+u"*")
        for file in files:
            try:
                if escludeExt:
                    print file[file.find(os.path.extsep)+1:]
                    if file[file.find(os.path.extsep):] in escludeExt:
                        continue
                os.remove(file)
            except:
                pass
        
    
    def DelFile(self, file):
        r"""
            Questo metodo elimina un singolo file
        """
        try:
            os.remove(file)
        except:
            pass

    def VerificaFile (self, filename):
        try:
            with open(filename, 'r'):
                pass
            return True
        except IOError:
            return False
        
        
    def VerificaFolder (self, folder):
        return os.path.exists(folder)


class PaisaSimpleFeaturesExtractor (GenericTools):
    """ 
        questa classe si occupa di estrarre le features da paisà e di salvarle
    """
 
    def VERSION (self):
        return "vers-Simple.0.1.a"
     
     
    def __init__(self, paisa = None, features= None, saveFilename = "file", maxWords = -1):
        r"""
            direttamente durante la creazione dell'oggetto parte l'elaborazione dei dati
            
            :param list features: le features da estrarre
            :param str paisa: path file corpus Paisà
            :param float maxWords: numero massimo di parole da utilizzare, se -1 uso tutto il corpus
            :return: None
           
        """             
   
        super (PaisaSimpleFeaturesExtractor, self).__init__ ()
        self.featuresList = features
        self.features = collections.defaultdict (float)
        self.countTotWords = float (0)
        self.maxWords = maxWords
        self.filenameToSave = saveFilename
        if self.VerificaFile (paisa):
            self.paisa_corpus = paisa
            self.__Elabora()
            
        else:
            print "Errore!\nFile %s non trovato!\nImpossibile Procedere!" % (paisa)


    def __Elabora(self):
        period = []
        wfound=float (0)
        fpaisa = codecs.open(self.paisa_corpus, mode='r', encoding='utf-8')

        while True:
            try:
                line = fpaisa.read (1)
                
                if self.countTotWords >= self.maxWords and self.maxWords != -1:
                    print "Limite parole raggiunto\nesecuzione terminata"
                    self.features['TOTWORDS'] = self.countTotWords
                    self.SaveByte (dati = self.features, filename = self.filenameToSave)
                    return
                if line[0] == u"<":
                    if period[0] != u'#' and period[0] != u"" and len(period) > 1:
                        period = u"".join (period)
                        if len(period.strip ()) > 1:
                            try:
                                #uso il costrutto try per evitare errori quando la substring manca
                                period = period[period.index (u">")+1:]
                                
                                for s in period.split (u"\n"):
                                    if s != u'\n' and s != u"":
                                        s = s.split (u"\t")
                                        try:
                                            if s[4] in self.featuresList:
                                                #versione stabile
                                                #self.features[s[2]] += 1
                                                #versione 2 da provare
                                                self.features[tuple([s[2], s[1]])] += 1
                                                wfound+=1
                                                print "trovate %1.0f abbreviazioni su %1.0f parole" %(wfound, self.countTotWords)
                                            self.countTotWords += 1    
                                                #                                    countTotWords=self.countTotWords
                                                #                                    features=self.features
                                        except IndexError:
                                            pass
                            except ValueError:
                                period = []
                        else:
                            period = []
                    period = []
                period.append (line)
            except:
                break
        #salvo i dati
        self.features['TOTWORDS'] = self.countTotWords
        self.SaveByte (dati = self.features, filename = self.filenameToSave)
        #self.SaveFile (dati = str(self.countTotWords), filename = "totWords.txt")
        fpaisa.close ()
        
        
if __name__=='__main__':
    paisa = 'C:\\Users\\Patrizio\\Documents\\prova testi\\tokenizer\\0.3.8.3.1\\paisa.annotated.CoNLL.utf8'
    save = 'file.file'
    
    
    paisa =' //paisa.annotated.CoNLL.utf8'
    save = ''
    PaisaSimpleFeaturesExtractor (paisa =paisa, features = ["SA"], saveFile = save)
