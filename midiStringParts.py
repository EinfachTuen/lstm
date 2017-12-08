# -*- coding: utf-8 -*-

def midiStartString():
    midiStartString = """MFile 1 17 480
MTrk
0 Meta TrkName "untitled"
0 SMPTE 96 0 3 0 0
0 TimeSig 4/4 24 8
0 KeySig 0 major
0 Tempo 600000
0 Meta Marker "A"
34560 Meta Marker "1."
36480 Meta Marker "A'"
71040 Meta Marker "2."
72960 Meta Marker "B"
123840 Tempo 1200000
123840 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Solo Flute"
0 PrCh ch=1 p=73
0 Par ch=1 c=7 v=100
0 Par ch=1 c=10 v=64"""

    return midiStartString
    
def midiEndeString():
    Ende = """124800 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "--------------------------------------"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Johann Sebastian Bach  (1685-1750)"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "--------------------------------------"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Partita in A minor for Solo Flute - BWV 1013"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "--------------------------------------"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "1st Movement: Allemande"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "--------------------------------------"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Sequenced with Cakewalk Pro Audio by"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "David J. Grossman - dave@unpronounceable.com"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "This and other Bach MIDI files can be found at:"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Dave's J.S. Bach Page"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "http://www.unpronounceable.com/bach"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "--------------------------------------"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Original Filename: fp-1all.mid"
0 Meta TrkEnd
TrkEnd
MTrk
0 Meta 0x21 00
0 Meta TrkName "Last Modified: March 1, 1997"
0 Meta TrkEnd
TrkEnd"""    
    
    return Ende