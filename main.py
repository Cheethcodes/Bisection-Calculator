from tkinter import *
from decimal import Decimal, ROUND_HALF_UP
from py_expression_eval import Parser

def execute_Prog():
    def getEquationFromUser():
        tempA = str(txt_Equation.get())
        return tempA

    def getAn():
        tempA = Decimal(txt_An.get())
        return tempA

    def getBn():
        tempA = Decimal(txt_Bn.get())
        return tempA

    def parseUserEquation(a):
        parser = Parser()
        expr = parser.parse(userEquation)
        tempA = expr.toString()
        return tempA

    def solveFpn(a):
        parser = Parser()
        expr = parser.parse(userEquation)
        tempA = expr.evaluate({'x': a})
        return tempA

    def anbnpnIterator():
        tempA = len(fpnList) - 1
        tempB = len(bnList) - 1
        tempC = len(anList) - 1

        if (fpnList[tempA] < 0):

            x1 = Decimal(Decimal(pnList[tempA]).quantize(Decimal('.00000001'),
                                                         rounding=ROUND_HALF_UP));  # limit decimal to two decimal places
            anList.append(float(x1))

            x2 = Decimal(Decimal(bnList[tempB]).quantize(Decimal('.00000001'), rounding=ROUND_HALF_UP));
            bnList.append(float(x2))

            tempD = (anList[len(anList) - 1] + bnList[len(bnList) - 1]) / 2
            x3 = Decimal(Decimal(tempD).quantize(Decimal('.00000001'), rounding=ROUND_HALF_UP));
            pnList.append(float(x3))

        elif (fpnList[tempA] > 0):

            x1 = Decimal(Decimal(anList[tempC]).quantize(Decimal('.00000001'), rounding=ROUND_HALF_UP));
            anList.append(float(x1))

            x2 = Decimal(Decimal(pnList[tempA]).quantize(Decimal('.00000001'), rounding=ROUND_HALF_UP));
            bnList.append(float(x2))

            tempD = (anList[len(anList) - 1] + bnList[len(bnList) - 1]) / 2
            x3 = Decimal(Decimal(tempD).quantize(Decimal('.00000001'), rounding=ROUND_HALF_UP));
            pnList.append(float(x3))

    def anbnpnTerminator():
        tempA = len(pnList) - 1
        tempB = len(pnList) - 2

        if (pnList[tempA] == pnList[tempB]):
            return False
        else:
            return True

    def mainLogic():
        cont = True
        counter = 0

        while (cont == True):

            if (counter == 0):
                anNew = Decimal(an.quantize(Decimal('.00000001'), rounding=ROUND_HALF_UP))
                anList.append(float(anNew))
                bnNew = Decimal(bn.quantize(Decimal('.00000001'), rounding=ROUND_HALF_UP))
                bnList.append(float(bnNew))
                tempA = (an + bn) / 2
                tempB = Decimal(tempA.quantize(Decimal('.00000001'), rounding=ROUND_HALF_UP))
                pnList.append(float(tempB))
                fpnList.append(solveFpn(pnList[len(pnList) - 1]))
                anbnpnIterator()
                cont = anbnpnTerminator()
                counter += 1

            elif (counter > 0):
                fpnList.append(solveFpn(pnList[len(pnList) - 1]))
                anbnpnIterator()
                cont = anbnpnTerminator()
                counter += 1

        global finalAnswer
        finalAnswer = pnList[len(pnList) - 1]

    def displayTable():
        listbox.delete(2, END)

        lb_OutputAnsMain = Label(root, text=str(finalAnswer), justify=LEFT)
        lb_OutputAnsMain.grid(row=7, column=1)
        Label(root, text=" ").grid(row=8)

        counter = 0;

        outputList = []

        for a in anList:
            outputList.append(str(a) + "    " + str(bnList[counter]) + "    " + str(pnList[counter]))
            counter += 1

        for x in outputList:
            listbox.insert(END, x)

        listbox.pack(side=LEFT)
        scroll.pack(side=RIGHT, fill=Y)
        scroll.config(command=listbox.yview)
        frame.grid(row=13, columnspan=20)

    global parsedUserEquation, userEquation, anList, bnList, pnList, fpnList, finalAnswer, an, bn
    anList = []
    bnList = []
    pnList = []
    fpnList = []
    finalAnswer = 0
    userEquation = getEquationFromUser()  # gets input from user
    parsedUserEquation = parseUserEquation(userEquation)  # transforms user input into a formula in a string form
    an = getAn()
    bn = getBn()

    mainLogic()
    displayTable()

#######################################################################
#######################################################################

root = Tk()
root.geometry("530x540")
root.resizable(False, False)
root.iconbitmap('calc.ico')
root.title("Bisection Calculator")

lb_Header = Label(root, text=" Bisection Calculator")
lb_Equation = Label(root, text="Equation", width=10)
lb_An = Label(root, text="A", width=10)
lb_Bn = Label(root, text="B", width=10)
txt_Equation = Entry(root)
txt_An = Entry(root)
txt_Bn = Entry(root)

Label(root, text=" ").grid(row=0)
lb_Header.config(font=("Courier", 30))
lb_Header.grid(row=1, columnspan=10)
Label(root, text=" ").grid(row=2)

lb_Equation.grid(row=3, column=0, columnspan=1, sticky="ew")
txt_Equation.grid(row=3, column=1, columnspan=5, sticky="ew")

Label(root, text=" ").grid(row=4)

lb_An.grid(row=5, column=0)
txt_An.grid(row=5, column=1, columnspan=1, sticky="ew")

lb_Bn.grid(row=5, column=2, columnspan=1, sticky="ew")
txt_Bn.grid(row=5, column=3, columnspan=1, sticky="ew")

Label(root, text=" ").grid(row=6)

lb_Output = Label(root, text="ANSWER:")

lb_Output.grid(row=7, column=0, columnspan=1, sticky="eW")

btn_Submit = Button(text="CALCULATE", width=15, command=execute_Prog)

btn_Submit.grid(row=5, column=5, columnspan=1, sticky="ew")

curAns = "An" + "    " + "Bn" + "     " + "Pn" + "\n"

frame = Frame(root)
scroll = Scrollbar(frame)
listbox = Listbox(frame, yscrollcommand=scroll.set, width=77, height=18)
listbox.insert(END, curAns)
listbox.insert(END, "----------------------------------------------------------------------------------------------------------------")

root.mainloop()