#!/usr/bin/env python3

def runic(isize, block=10):
    ''' make a random block of runic '''
    import random
    chars = list('ᚠᚡᚢᚣᚤᚥᚦᚧᚨᚩᚪᚫᚬᚭᚮᚯᚰᚱᚲᚳᚴᚵᚶᚷ'+ \
                 'ᚸᚹᚺᚻᚼᚽᚾᚿᛀᛁᛂᛃᛄᛅᛆᛇᛈᛉᛊᛋᛌᛍᛎᛏᛐᛑᛒᛓ' + \
                 'ᛔᛕᛖᛗᛘᛙᛚᛛᛜᛝᛞᛟᛠᛡᛢᛣᛤᛥᛦᛧᛨᛩᛪ'+ \
                 '᛫᛬᛭ᛮᛯᛰ')
    result = ''
    for ss in range(1,isize):
        which = random.randrange(0, len(chars))
        result += chars[which]
        if ss % block == 0:
            result += '\n'
    return result

if __name__ == '__main__':
    print(runic(35))
    
