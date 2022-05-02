import pickle
import string

def depunc(s):
    result = ''
    p = string.punctuation
    p = p[:6] + p[7:]  #this eliminate "'"
    for i in s:
        if i not in p:
            if i == "'":
                result += ' '
            else:
                result += i
       
    return result
        
class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = []
        """
        ["1st_line", "2nd_line", "3rd_line", ...]
        Example:
        "How are you?\nI am fine.\n" will be stored as
        ["How are you?", "I am fine." ]
        """

        self.index = {}
        """
        {word1: [line_number_of_1st_occurrence,
                 line_number_of_2nd_occurrence,
                 ...]
         word2: [line_number_of_1st_occurrence,
                  line_number_of_2nd_occurrence,
                  ...]
         ...
        }
        """

        self.total_msgs = 0
        self.total_words = 0

    def get_total_words(self):
        return self.total_words

    def get_msg_size(self):
        return self.total_msgs

    def get_msg(self, n):
        return self.msgs[n]

    def add_msg(self, m):
        """
        m: the message to add

        updates self.msgs and self.total_msgs
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        m = m.strip('\n')
        l = m.split('\n')
        self.msgs.extend(l)
        self.total_msgs += len(l)
        # ---- end of your code --- #
        return

    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)

    def indexing(self, m, l):
        """
        updates self.total_words and self.index
        m: message, l: current line number
        """

        # IMPLEMENTATION
        # ---- start your code ---- #
        lm = m.split()
        self.total_words += len(lm)
        for i in lm:
            i = depunc(i)
            self.index[i] = self.index.get(i,[])
            if l not in self.index[i]:
                self.index[i].append(l)
    
        # ---- end of your code --- #
        return

    # implement: query interface

    def search(self, term):
        """
        return a list of tupple.
        Example:
        if index the first sonnet (p1.txt),
        then search('thy') will return the following:
        [(7, " Feed'st thy light's flame with self-substantial fuel,"),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (12, ' Within thine own bud buriest thy content,')]
        """
        msgs = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        term1 = depunc(term)
        
        
        if ' ' in term1:
            t = term1.split()
            #print(t)
            m0 = self.search(t[0])
            
            for i in m0:
                l = i[1].split()
                indx = l.index(t[0])
                yes = True
                for j in range(1,len(t)):
                    try:
                        if t[j] != l[indx + j]:
                            yes = False
                            break
                    except:
                        yes = False
                        break
                if yes:
                    msgs.append(i)
        else:
            try:    
                for i in self.index[term1]:
                    msgs.append((i,self.msgs[i]))
            except:
                print("Term not found")
                return msgs

        # ---- end of your code --- #
        return msgs


class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()

    def load_poems(self):
        """
        open the file for read, then call
        the base class's add_msg_and_index()
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        f = open("AllSonnets.txt",'r')
        s = f.readline()
        s = s.strip('\n')
        for i in range(2931):
            self.add_msg_and_index(s)
            s = f.readline()
            s = s.strip('\n')
        f.close()
        # ---- end of your code --- #
        return

    def get_poem(self, p):
        """
        p is an integer, get_poem(1) returns a list,
        each item is one line of the 1st sonnet

        Example:
        get_poem(1) should return:
        ['I.', '', 'From fairest creatures we desire increase,',
         " That thereby beauty's rose might never die,",
         ' But as the riper should by time decease,',
         ' His tender heir might bear his memory:',
         ' But thou contracted to thine own bright eyes,',
         " Feed'st thy light's flame with self-substantial fuel,",
         ' Making a famine where abundance lies,',
         ' Thy self thy foe, to thy sweet self too cruel:',
         " Thou that art now the world's fresh ornament,",
         ' And only herald to the gaudy spring,',
         ' Within thine own bud buriest thy content,',
         " And, tender churl, mak'st waste in niggarding:",
         ' Pity the world, or else this glutton be,',
         " To eat the world's due, by the grave and thee.",
         '', '', '']
        """
        poem = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        
       
        indxl = self.index[self.int2roman[p]][0]
        for i in range(indxl,indxl + 19):
            poem.append(self.msgs[i]) #A sonnet is 14-line long.

        # ---- end of your code --- #
        return poem


if __name__ == "__main__":
    sonnets = PIndex("AllSonnets.txt")
    # the next two lines are just for testing
    #print(sonnets.index)
    p3 = sonnets.get_poem(3)
    print(p3)
    s_love = sonnets.search("love")
    print(s_love)
    #print(sonnets.search('my love'))