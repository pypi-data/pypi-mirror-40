# --- Implementing logic gates with only NAND gate ---

# --- WIP ---

# --- THIS PROGRAM IS DESIGNED FOR INPUTS OF 0 AND 1, AND NO OTHER INPUTS ---

def Input(ch=0):
    if ch :
        return[int(input("Enter the value of pin A: ")),int(input("Enter the value of pin B: "))]

    return [int(input("Enter the input: "))]

class NAND(object):
    def __init__(self):
        self.Input = [None,None]
        self.Output = None
        self.Model = "NAND Gate"

    def __repr__(self):
        print(self.Model)
        print("Input : ",self.Input)
        print("Output : ",self.Output)
        return ''

    def getInput(self,a,b):
        self.Input = [a,b]
        self.calOutput()

    def calOutput(self):
        if self.Input[0] == 1 and self.Input[1] == 1:
            self.Output = 0
        else:
            self.Output = 1
    
class AND():
    def __init__(self,In=None):
        ### In = [num1,num2]
        ob1 = NAND()
        ob2 = NAND()

        if not In:
            self.Input = Input(1)
        else:
            self.Input = In

        self.Model = "AND Gate"

        # Calculate the value of first NAND gate 
        ob1.getInput(self.Input[0],self.Input[1])

        # Calculates the value of the second NAND gate
        ob2.getInput(ob1.Output,ob1.Output)
        self.Output = ob2.Output 
    
class AND3():
    # This class exists to and three inputs
    # Used for K-MAP SOP form
    def __init__(self,In):
        self.Input = In

        ob1 = AND([In[0],In[1]])
        ob2 = AND([ob1.Output,In[2]])

        self.Output = ob2.Output

class NOT():
    def __init__(self,In = None):
        ### In = [num1]
        ob1 = NAND()

        self.Model = "NOT Gate"
        if not In:
            self.Input = Input()
        else:
            self.Input = In

        ob1.getInput(self.Input[0],self.Input[0])
        self.Output = ob1.Output

class OR():
    def __init__(self,In=None):
        ### In = [num1,num2]
        # three gates, since there are three nand gates involved in making an OR gate
        ob1 = NAND()
        ob2 = NAND()
        ob3 = NAND()

        self.Model = "OR Gate"
        if not In:
            self.Input = Input(1)
        else:
            self.Input = In
        # Evaluating the nand gates to get the equivalent or gate
        ob1.getInput(self.Input[0],self.Input[0])
        ob2.getInput(self.Input[1],self.Input[1])

        ob3.getInput(ob1.Output,ob2.Output)

        # saving the output with the or gate
        self.Output = ob3.Output

class MultiOR():
    # This class exists to add multiple inputs with OR gates
    # used in K-MAP SOP
    def __init__(self, In):
        base = OR([In[0],In[1]])
        temp = [base.Output]
        for i in range(2,len(In)):
            ob1 = OR([temp[i-2],In[i]])
            temp.append(ob1.Output)
        self.Output = temp[::-1][0]

class NOR():
    def __init__(self,In=None):
        ### In = [num1,num2]
        if not In:
            self.Input = Input(1)
        else:
            self.Input = In

        ob1 = OR(In)
        ob2 = NOT([ob1.Output])

        self.Model = "NOR Gate"

        self.Output = ob2.Output

class XOR():
    def __init__(self,In=None):
        if not In:
            self.Input = Input(1)
        else:
            self.Input = In
        self.Model = "XOR Gate"
        
        ob1 = NAND()
        ob2 = NAND()
        ob3 = NAND()
        ob4 = NAND()

        ob1.getInput(self.Input[0],self.Input[1])
        ob2.getInput(self.Input[0],ob1.Output)
        ob3.getInput(ob1.Output,self.Input[1])
        ob4.getInput(ob2.Output,ob3.Output)

        self.Output = ob4.Output

class XNOR():
    def __init__(self,In=None):
        if not In:
            self.Input = Input(1)
        else:
            self.Input = In
        self.Model = "XNOR Gate"

        ob1 = XOR(In)
        ob2 = NOT([ob1.Output])

        self.Output = ob2.Output

class HalfAdder():
    def __init__(self,In=None):
        ### In = ['Input 1','Input 2']
        ### Out = ['Sum','Carry']
        if not In:
            self.Input = Input(1)
        else:
            self.Input = In
        self.Model = "Half Adder"

        ob1 = XOR(self.Input)
        ob2 = AND(self.Input)

        self.Output = [ob1.Output,ob2.Output]    # S,C    

class Adder():
    def __init__(self,In=None):
        ### In = ['Input 1','Input 2','Carry']
        ### Out = ['Sum','Carry']

        self.Model = 'One Bit Adder'

        ob1 = HalfAdder([In[0],In[1]])
        ob2 = HalfAdder([ob1.Output[0],In[2]])
        ob3 = OR([ob2.Output[1],ob1.Output[1]])

        self.Output = [ob2.Output[0],ob3.Output]

class HalfSubtractor():
    def __init__(self,In=None):
        ### In = ['Input 1','Input 2']
        ### Out = ['Difference','Bout']
        if not In:
            self.Input = Input(1)
        else:
            self.Input = In
        self.Model = "Half Subtractor"

        ob1 = XOR(self.Input)
        ob2 = NOT([self.Input[0]])
        ob3 = AND([ob2.Output,self.Input[1]])

        self.Output = [ob1.Output,ob3.Output]    # D,B

class Subtractor():
    def __init__(self,In=None):
        ### In = ['Input 1','Input 2','Bout']
        ### Out = ['Difference','Bout']

        self.Model = 'One Bit Subtractor'

        ob1 = HalfSubtractor([In[0],In[1]])
        ob2 = HalfSubtractor([ob1.Output[0],In[2]])
        ob3 = OR([ob2.Output[1],ob1.Output[1]])

        self.Output = [ob2.Output[0],ob3.Output]

class RCA_4Bit():
    # Four bit Ripple Carry Adder
    # Adds two four bit numbers
    # Returns a five bit output

    def __init__(self,n1,n2):
        ### n1 = [a,b,c,d] , where a,b,c,d are the number's binary representation bits
        ### similarly for n2

        ### Code to ensure all inputs are 8 bits long
        while (len(n1) != 8):
            n1.append(0)
        while (len(n2) != 8):
            n2.append(0)

        # Reversing the numbers
        t1 = n1[::-1]
        t2 = n2[::-1]

        self.Input = [t1,t2]

        ob1 = Adder([t1[0],t2[0],0])
        ob2 = Adder([t1[1],t2[1],ob1.Output[1]])
        ob3 = Adder([t1[2],t2[2],ob2.Output[1]])
        ob4 = Adder([t1[3],t2[3],ob3.Output[1]])

        self.Output = [ob4.Output[1],ob4.Output[0],ob3.Output[0],ob2.Output[0],ob1.Output[0]]
