# My Sudoku Solver attempt.

import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as et
from argparse import ArgumentParser, SUPPRESS

PUZZLE = 'puzzle_name'
SOLVE = 'solve_on_startup'
TIME = 'time_delay'
SOLUTION = 'solution_name'
EXIT = 'exit_on_solve'

class myArgParse:
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument(f'--{PUZZLE}', help='Takes name of XML file puzzle spec and automatically loads it.')
        parser.add_argument(f'--{SOLVE}', help='Whether to solve on program startup.', action='store_true')
        parser.add_argument(f'--{TIME}', help='Delay, in seconds, between each solving step.', type=float)
        parser.add_argument(f'--{SOLUTION}', help='Name of output XML file solution.')
        parser.add_argument(f'--{EXIT}', help='Whether to exit program on solving the puzzle.', action='store_true')
        self._args = vars(parser.parse_args())

    def setup(self):
        pass

    @property
    def args(self):
        return self._args

myArgParse()

def runSteps(x):
    ss = stepSolver(x, str(interStepDelay.get()))
    ss.doStep()

class createGrid:
    def __init__(self, x, y):
        keysFromDict = [i for i in startStateDict.keys()]
        valuesFromDict = [i for i in startStateDict.values()]

        global coordsID, coordsContent, boxID, boxContent
        coordsID = []
        coordsContent = []

        for row in range(0, x):
            rowID = []
            rowContent = []
            for col in range(0, y):
                if tuple((row, col)) in keysFromDict:
                    rowContent.append(startStateDict.get((row,col)))
                    one_list = rowContent[col]

                    frame = tk.Frame(master=win, highlightbackground='black', highlightthickness='1')
                    frame.grid(row=row, column=col)
                    label = tk.Label(master=frame, text=one_list, height=rowheight, width=rowwidth, bg='light green')
                    label.grid(row=row, column=col)
                    rowID.append(label)

                else:
                    maxNumList = [i+1 for i in range(maxNum)]
                    rowContent.append(maxNumList)

                    frame = tk.Frame(master=win, highlightbackground='black', highlightthickness='1' )
                    frame.grid(row=row, column=col)
                    label = tk.Label(master=frame, text=maxNumList, height=rowheight, width=rowwidth, bg='white')
                    label.grid(row=row, column=col)
                    rowID.append(label)
            coordsID.append(rowID)
            coordsContent.append(rowContent)

        boxID = []
        boxContent = []
        for a in range(0, rowsPerBox * colsPerBox, max(colsPerBox, 1)):
            for b in range(0, rowsPerBox * colsPerBox, rowsPerBox):
                createGrid.boxClassification(self, a, b)
        colors = ['white', 'salmon1', 'white', 'salmon1', 'white', 'salmon1', 'white', 'salmon1', 'white']
        for i in range(len(boxID)):
            for j in range(len(boxID[a])):
                boxID[i][j].configure(bg=colors[i])

    def boxClassification(self, a, b):
        global boxMiniContent, boxMiniID
        boxMiniID = []
        boxMiniContent = []
        for i in range(b, rowsPerBox+b):
            for j in range(a, colsPerBox+a):
                boxMiniID.append(coordsID[i][j])
                boxMiniContent.append(coordsContent[i][j])
        if (boxMiniContent not in boxContent) and (boxMiniID not in boxID):
            boxContent.append(boxMiniContent)
            boxID.append(boxMiniID)

class myTkinter:
    def __init__(self):
        global win
        win = tk.Tk()

        rowdim = coldim = 9
        global rowwidth
        rowwidth = 20
        global rowheight
        rowheight = 4

        labels = []

        win.title('Sudoku Solver')
        win.rowconfigure( 3, weight=1)
        win.columnconfigure( 3, weight=1)

        global fileName, numSteps, nextRow, interStepDelay, newFileName
        fileName = tk.StringVar()
        newFileName = tk.StringVar()
        numSteps = tk.IntVar()
        interStepDelay = tk.StringVar()

        nextRow = rowdim
        # File name button
        fileNameButton = tk.Button(master=win, text="Enter puzzle filename:", bg="SteelBlue1", width=rowwidth, command=lambda: myXML(fileName.get()))
        fileNameButton.grid(row=nextRow, column=0, sticky=tk.W)
        #File name entry box
        fileNameEntry = tk.Entry(master=win, bg="White", width=rowwidth, text=fileName)
        fileNameEntry.grid(row=nextRow, column=1)
        # Puzzle state button
        storeStateButton = tk.Button(master=win, text="Store puzzle state as:", bg="SteelBlue3", width=rowwidth, command=lambda: myXML.saveState())
        storeStateButton.grid(row=nextRow, column=3, sticky=tk.W)
        # Puzzle state entry box
        storeState = tk.Entry(master=win, bg="White", width=rowwidth, text=newFileName)
        storeState.grid(row=nextRow, column=4)

        nextRow += 1
        # Solver stepping
        stepButton = tk.Button(master=win, text="Step the solver", bg="light cyan", fg="black", width=rowwidth, command=lambda: runSteps(int(numSteps.get())))
        stepButton.grid(row=nextRow, column=0)
        # Solver label
        stepEntryLabel = tk.Label( master=win, text="Enter number of steps: ", bg="light cyan", fg="black", width=rowwidth)
        stepEntryLabel.grid(row=nextRow, column=1)
        # Solver step count
        stepEntry = tk.Entry(master=win, bg="White", width=rowwidth, text=numSteps)
        stepEntry.grid(row=nextRow, column=2)


        nextRow += 1
        # Complete all!
        solve_all_button = tk.Button(master=win, text="Complete the puzzle", bg="burlywood2", fg="black", width=rowwidth, command=lambda: completeSolver(float(interStepDelay.get())))
        solve_all_button.grid(row=nextRow, column=0, sticky=tk.W)
        solve_all_time_step_label = tk.Label( master=win, text="Enter inter-step delay (s): ", bg="burlywood1", fg="black", width=rowwidth)
        solve_all_time_step_label.grid(row=nextRow, column=1, sticky=tk.W)
        solve_all_time_step = tk.Entry( master=win, fg="brown", bg="white", width=rowwidth, text=interStepDelay)
        solve_all_time_step.grid(row=nextRow, column=2)

        nextRow += 1
        global displaySteps
        displaySteps = tk.Text(master=win, height=5, width=80)
        displaySteps.grid(row=14, column=0, columnspan=7, rowspan=3)

        argvar = myArgParse()
        if argvar.args[PUZZLE]:
            myXML(argvar.args[PUZZLE])
        if argvar.args[SOLVE]:
            if argvar.args[TIME]:
                completeSolver(timeDelay=argvar.args[TIME])
        if argvar.args[SOLUTION]:
            myXML.saveState(argvar.args[SOLUTION])

        win.mainloop() # END CREATION OF TKINTER win

class myXML:
    def __init__(self, x):
        tree = et.parse(str(x))
        root = tree.getroot()

        global puzzleName, rowsPerBox, colsPerBox, startStateDict, wellFormed, Solvable, uniqueSolution, \
            pigeonholeDecidable, rowNum, colNum, maxNum, finalMessage
        puzzleName = root[0].text
        rowsPerBox = int(root[1].text)
        colsPerBox = int(root[2].text)
        startState = root[3].text
        wellFormed = root[4].text
        Solvable = root[5].text
        uniqueSolution = root[6].text
        pigeonholeDecidable = root[7].text


        try:
            startStateDict = eval(f'dict({startState})')
        except:
            startStateDict={}
            gridNP = tk.Label(master = win, text = 'Grid is not possible.', bg = 'red', fg = 'black')
            gridNP.grid(row=nextRow, column=0, columnspan=5)

        maxNum = int(colsPerBox) * int(rowsPerBox)

        if int(rowsPerBox) == int(colsPerBox):
            rowNum, colNum = rowsPerBox**2, colsPerBox**2
        else:
            rowNum, colNum = rowsPerBox * colsPerBox, rowsPerBox * colsPerBox

        createGrid(rowNum, colNum)

        if wellFormed == 'True':
            wellFormedMessage = 'is well formed, '
        else:
            wellFormedMessage = 'is not well formed, '

        if Solvable == 'True':
            solvableMessage = 'is solvable, '
        else:
            solvableMessage = 'is not solvable, '

        if uniqueSolution == 'True':
            uniqueSolutionMessage = 'has a unique solution, '
        else:
            uniqueSolutionMessage = 'does not have a unique solution, '

        if pigeonholeDecidable == 'True':
            pigeonholeDecidableMessage = 'and is pigeon-hole decidable.'
        else:
            pigeonholeDecidableMessage = 'and is not pigeon-hole decidable.'

        finalMessage = wellFormedMessage + solvableMessage + uniqueSolutionMessage + pigeonholeDecidableMessage
        tkinterName()

    def saveState(x=0):
        puzzle = et.Element('puzzle')
        tree = et.ElementTree(puzzle)

        name = et.SubElement(puzzle, 'name')
        rows_per_box = et.SubElement(puzzle, 'rows_per_box')
        cols_per_box = et.SubElement(puzzle, 'cols_per_box')
        start_state = et.SubElement(puzzle, 'start_state')
        well_formed = et.SubElement(puzzle, 'well_formed')
        solvable = et.SubElement(puzzle, 'solvable')
        unique_solution = et.SubElement(puzzle, 'unique_solution')
        pigeonhole_decidable = et.SubElement(puzzle, 'pigeonhole_decidable')

        rows_per_box.text = str(rowsPerBox)
        cols_per_box.text = str(colsPerBox)
        #start_state.text = str(startStateDict)

        newStateDict = {}
        for i in range(rowNum):
            for j in range(colNum):
                newStateDict.update({(eval(f'{i}, {j}')): [coordsContent[i][j]]})
        start_state.text = str(newStateDict)

        well_formed.text = wellFormed
        solvable.text = Solvable
        unique_solution.text = uniqueSolution
        pigeonhole_decidable.text = pigeonholeDecidable

        puzzle_file = et.tostring(puzzle)

        if x:
            name.text = str(x)
            tree.write(rf'C:\Users\me\OneDrive - East Tennessee State University\{x}.xml')
            displaySteps.insert(1.0, f'File saved as {x}.xml\n')
        else:
            name.text = str(newFileName.get())
            tree.write(rf'C:\Users\me\OneDrive - East Tennessee State University\{newFileName.get()}.xml')
            displaySteps.insert(1.0, f'File saved as {newFileName.get()}.xml\n')

class tkinterName:
    def __init__(self):
        pInfoLabel = tk.Label(master=win, text=(puzzleName + ' ' + finalMessage), height=2)
        pInfoLabel.grid(row=13, column=0, columnspan=5)

class stepSolver:
    def __init__(self, maxSteps, timeDelay=0):
        self.intCount = 0
        self.currentSteps = 0
        self.maxSteps = maxSteps
        self.newIntCount = 0
        self.timeDelay = timeDelay

        for a in range(rowNum):
            for b in range(colNum):
                if len(coordsContent[a][b]) == 1:
                    self.intCount += 1

    def checkNewInts(self):
        for a in range(rowNum):
            for b in range(colNum):
                if len(coordsContent[a][b]) == 1:
                    self.newIntCount += 1
        if self.intCount != self.newIntCount and self.currentSteps < self.maxSteps:
            self.doStep()

    def doStep(self):
        for a in range(rowNum):
            for b in range(colNum):
                if len(coordsContent[a][b]) == 1:
                    self.intCount += 1

        for row in range(rowNum):
            for col in range(colNum):
                if len(coordsContent[row][col]) == 1:
                    global checkNum
                    checkNum = coordsContent[row][col][0]
                    stepSolver.stepRow(self, row, col)
                    if self.currentSteps >= self.maxSteps:
                        self.currentSteps = 0
                        return
                    stepSolver.stepCol(self, col, row)
                    if self.currentSteps >= self.maxSteps:
                        self.currentSteps = 0
                        return

        for i in range(len(boxID)):
            for j in range(len(boxID)):
                if len(boxContent[i][j]) == 1:
                    global boxCheckNum
                    boxCheckNum = boxContent[i][j][0]
                    stepSolver.stepBox(self, i, j)
                    if self.currentSteps >= self.maxSteps:
                        self.currentSteps = 0
                        return

        for i in range(rowNum):
            for j in range(colNum):
                if len(coordsContent[i][j]) > 1:
                    self.p1_list1 = coordsContent[i][j]
                    for k in range(rowNum):
                        if coordsContent[i][k] == self.p1_list1 and j != k:
                            self.p2_list1 = coordsContent[i][k]
                            completeSolver.stepPigeon2(self, i, j, k, 1)
                            if self.currentSteps >= self.maxSteps:
                                self.currentSteps = 0
                                return
                    for l in range(colNum):
                        if coordsContent[l][j] == self.p1_list1 and l != i:
                            self.p2_list1 = coordsContent[l][j]
                            completeSolver.stepPigeon2(self, i, j, l, 2)
                            if self.currentSteps >= self.maxSteps:
                                self.currentSteps = 0
                                return

        for r in range(rowNum):
            for c1 in range(colNum):
                if len(coordsContent[r][c1]) == 2:
                    self.p2_list1 = coordsContent[r][c1]
                    for c2 in range(rowNum):
                        if coordsContent[r][c2] == self.p2_list1 and c1 != c2:
                            self.p2_list2 = coordsContent[r][c2]
                            for c3 in range(rowNum):
                                if coordsContent[r][c3] == self.p2_list1 and c1 != c3 and c2 != c3:
                                    completeSolver.stepPigeon3(self, r, c1, c2, c3, 1)
                                    if self.currentSteps >= self.maxSteps:
                                        self.currentSteps = 0
                                        return
                    for r2 in range(colNum):
                        if coordsContent[r2][c1] == self.p2_list1 and r != r2:
                            self.p2_list2 = coordsContent[r][c2]
                            for r3 in range(rowNum):
                                if coordsContent[r3][c1] == self.p2_list1 and r2 != r3 and r3 != r:
                                    completeSolver.stepPigeon3(self, c1, r, r2, r3, 2)
                                    if self.currentSteps >= self.maxSteps:
                                        self.currentSteps = 0
                                        return
                elif len(coordsContent[r][c1]) == 3:
                    self.p2_list1 = coordsContent[r][c1]
                    for c2 in range(rowNum):
                        if coordsContent[r][c2] == self.p2_list1 and c1 != c2:
                            self.p2_list2 = coordsContent[r][c2]
                            for c3 in range(rowNum):
                                if coordsContent[r][c3] == self.p2_list1 and c1 != c3 and c2 != c3:
                                    completeSolver.stepPigeon3(self, r, c1, c2, c3, 1)
                                    if self.currentSteps >= self.maxSteps:
                                        self.currentSteps = 0
                                        return
                    for r2 in range(colNum):
                        if coordsContent[r2][c1] == self.p2_list1 and r != r2:
                            self.p2_list2 = coordsContent[r][c2]
                            for r3 in range(rowNum):
                                if coordsContent[r3][c1] == self.p2_list1 and r2 != r3 and r3 != r:
                                    completeSolver.stepPigeon3(self, c1, r, r2, r3, 2)
                                    if self.currentSteps >= self.maxSteps:
                                        self.currentSteps = 0
                                        return


        stepSolver.checkNewInts(self)

    def stepRow(self, r, c):
        for i in range(len(coordsContent[r])):
            iter = coordsContent[r][i]
            if len(iter) != 1 and checkNum in iter:
                displaySteps.insert(1.0, f'Using ({r}, {c}) to remove {checkNum} from ({r}, {i})\n')
                win.after(int(float(self.timeDelay) * 1000), coordsID[r][c].configure(bg='deep sky blue'))
                win.update()
                win.after(int(float(self.timeDelay) * 1000), coordsID[r][i].configure(bg='orange'))
                win.update()
                iter.remove(checkNum)
                win.update()
                coordsID[r][c].configure(bg='white')
                coordsID[r][i].configure(bg='white', text=iter)
                self.currentSteps += 1
                if self.currentSteps >= self.maxSteps:
                    break

    def stepCol(self, c, r):
        for i in range(len(coordsContent[c])):
            iter = coordsContent[i][c]
            if len(iter) != 1 and checkNum in iter:
                displaySteps.insert(1.0, f'Using ({r}, {c}) to remove {checkNum} from ({i}, {c})\n')
                win.after(int(float(self.timeDelay) * 1000), coordsID[r][c].configure(bg='deep sky blue'))
                win.update()
                win.after(int(float(self.timeDelay) * 1000), coordsID[i][c].configure(bg='orange'))
                win.update()
                iter.remove(checkNum)
                win.update()
                coordsID[r][c].configure(bg='white')
                coordsID[i][c].configure(bg='white', text=iter)
                self.currentSteps += 1
                if self.currentSteps >= self.maxSteps:
                    break

    def stepBox(self, b, j):
        for box in range(len(boxContent[b])):
            iter = boxContent[b][box]
            if len(iter) != 1 and boxCheckNum in iter:
                displaySteps.insert(1.0, f'In Box {b}, using Cell {j} to remove {boxCheckNum} from Cell {box}\n')
                win.after(int(float(self.timeDelay) * 1000), boxID[b][j].configure(bg='deep sky blue'))
                win.update()
                win.after(int(float(self.timeDelay) * 1000), boxID[b][box].configure(bg='orange'))
                win.update()
                iter.remove(boxCheckNum)
                win.update()
                boxID[b][j].configure(bg='white')
                boxID[b][box].configure(bg='white', text=iter)
                self.currentSteps += 1
                if self.currentSteps >= self.maxSteps:
                    break

    def stepPigeon2(self, r, c, h, x):
        if x == 1:
            for i in range(rowNum):
                for num in self.p1_list1:
                    if num in coordsContent[r][i] and i != c and i != h:
                        displaySteps.insert(1.0, f'Using cells ({r}, {c}) and ({r}, {h}) to remove {num} from cell ({r}, {i})\n')
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][c].configure(bg='deep sky blue'))
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][h].configure(bg='deep sky blue'))
                        win.update()
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][i].configure(bg='orange'))
                        win.update()
                        coordsContent[r][i].remove(num)
                        coordsID[r][c].configure(bg='white')
                        coordsID[r][h].configure(bg='white')
                        coordsID[r][i].configure(bg='white', text=coordsContent[r][i])
                        self.currentSteps += 1
                if self.currentSteps >= self.maxSteps:
                    break
        else:
            for i in range(rowNum):
                for num in self.p1_list1:
                    if num in coordsContent[i][c] and i != r and i != h:
                        displaySteps.insert(1.0, f'Using cells ({r}, {c}) and ({h}, {c}) to remove {num} from cell ({i}, {c})\n')
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][c].configure(bg='deep sky blue'))
                        win.after(int(float(self.timeDelay) * 1000), coordsID[h][c].configure(bg='deep sky blue'))
                        win.update()
                        win.after(int(float(self.timeDelay) * 1000), coordsID[i][c].configure(bg='orange'))
                        win.update()
                        coordsContent[i][c].remove(num)
                        coordsID[r][c].configure(bg='white')
                        coordsID[h][c].configure(bg='white')
                        coordsID[i][c].configure(bg='white', text=coordsContent[i][c])
                        self.currentSteps += 1
                if self.currentSteps >= self.maxSteps:
                    break

    def stepPigeon3(self, r, c1, c2, c3, x):
        if x == 1:
            for i in range(rowNum):
                for num in self.p2_list1:
                    if num in coordsContent[r][i] and i != c1 and i != c2 and i != c3 and len(coordsContent[r][i]) != 1:
                        displaySteps.insert(1.0, f'Using cells ({r}, {c1}), ({r}, {c2}), and ({r}, {c3}) to remove {num} from cell ({r}, {i})\n')
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][c1].configure(bg='deep sky blue'))
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][c2].configure(bg='deep sky blue'))
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][c3].configure(bg='deep sky blue'))
                        win.update()
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][i].configure(bg='orange'))
                        win.update()
                        coordsContent[r][i].remove(num)
                        coordsID[r][c1].configure(bg='white')
                        coordsID[r][c2].configure(bg='white')
                        coordsID[r][c3].configure(bg='white')
                        coordsID[r][i].configure(bg='white', text=coordsContent[r][i])
                        self.currentSteps += 1
                if self.currentSteps >= self.maxSteps:
                    break
        else:
            for i in range(colNum):
                for num in self.p2_list1:
                    if num in coordsContent[i][c1] and i != r and i != r2 and i != r3 and len(coordsContent[i][c1]) != 1:
                        displaySteps.insert(1.0, f'Using cells ({c1}, {r}), ({c2}, {r}), and ({c3}, {r}) to remove {num} from cell ({i}, {r})\n')
                        win.after(int(float(self.timeDelay) * 1000), coordsID[c1][r].configure(bg='deep sky blue'))
                        win.after(int(float(self.timeDelay) * 1000), coordsID[c2][r].configure(bg='deep sky blue'))
                        win.after(int(float(self.timeDelay) * 1000), coordsID[c3][r].configure(bg='deep sky blue'))
                        win.update()
                        win.after(int(float(self.timeDelay) * 1000), coordsID[i][r].configure(bg='orange'))
                        win.update()
                        coordsContent[i][r].remove(num)
                        coordsID[c1][r].configure(bg='white')
                        coordsID[c2][r].configure(bg='white')
                        coordsID[c3][r].configure(bg='white')
                        coordsID[i][r].configure(bg='white', text=coordsContent[i][r])
                        self.currentSteps += 1
                if self.currentSteps >= self.maxSteps:
                    break

class completeSolver:
    def __init__(self, timeDelay=0):
        self.timeDelay = timeDelay
        self.intCount = 0
        self.newIntCount = 0
        for a in range(rowNum):
            for b in range(colNum):
                if len(coordsContent[a][b]) == 1:
                    self.intCount += 1

        for row in range(rowNum):
            for col in range(colNum):
                if len(coordsContent[row][col]) == 1:
                    global checkNum
                    checkNum = int(coordsContent[row][col][0])
                    completeSolver.stepRow(self, row, col)
                    completeSolver.stepCol(self, col, row)

        for i in range(len(boxID)):
            for j in range(len(boxID)):
                if len(boxContent[i][j]) == 1:
                    global boxCheckNum
                    boxCheckNum = boxContent[i][j][0]
                    completeSolver.stepBox(self, i, j)

        for i in range(rowNum):
            for j in range(colNum):
                if len(coordsContent[i][j]) == 2:
                    self.p1_list1 = coordsContent[i][j]
                    for k in range(rowNum):
                        if coordsContent[i][k] == self.p1_list1 and j != k:
                            self.p2_list1 = coordsContent[i][k]
                            completeSolver.stepPigeon2(self, i, j, k, 1)
                    for l in range(colNum):
                        if coordsContent[l][j] == self.p1_list1 and l != i:
                            self.p2_list1 = coordsContent[l][j]
                            completeSolver.stepPigeon2(self, i, j, l, 2)

        for r in range(rowNum):
            for c1 in range(colNum):
                if len(coordsContent[r][c1]) == 2:
                    self.p2_list1 = coordsContent[r][c1]
                    for c2 in range(rowNum):
                        if coordsContent[r][c2] == self.p2_list1 and c1 != c2:
                            self.p2_list2 = coordsContent[r][c2]
                            for c3 in range(rowNum):
                                if coordsContent[r][c3] == self.p2_list1 and c1 != c3 and c2 != c3:
                                    completeSolver.stepPigeon3(self, r, c1, c2, c3, 1)
                    for r2 in range(colNum):
                        if coordsContent[r2][c1] == self.p2_list1 and r != r2:
                            self.p2_list2 = coordsContent[r][c2]
                            for r3 in range(rowNum):
                                if coordsContent[r3][c1] == self.p2_list1 and r2 != r3 and r3 != r:
                                    completeSolver.stepPigeon3(self, c1, r, r2, r3, 2)

        completeSolver.checkNewInts(self)
        completeSolver.checkSolve(self)

    def checkSolve(self):
        solve_num = 0
        for i in range(rowNum):
            for j in range(colNum):
                if len(coordsContent[i][j]) == 1:
                    solve_num += 1
        if solve_num == (rowNum * colNum):
            displaySteps.insert(1.0, 'Puzzle is solved.\n')
        if myArgParse().args[SOLUTION]:
            myXML.saveState(myArgParse().args[SOLUTION])
        if myArgParse().args[EXIT]:
            exit()

    def checkNewInts(self):
        for a in range(rowNum):
            for b in range(colNum):
                if len(coordsContent[a][b]) == 1:
                    self.newIntCount += 1
        if self.intCount != self.newIntCount:
            completeSolver()

    def stepRow(self, r, c):
        for i in range(len(coordsContent[r])):
            iter = coordsContent[r][i]
            if len(iter) != 1 and checkNum in iter:
                displaySteps.insert(1.0, f'Using ({r}, {c}) to remove {checkNum} from ({r}, {i})\n')
                win.after(int(float(self.timeDelay) * 1000), coordsID[r][c].configure(bg='deep sky blue'))
                win.update()
                win.after(int(float(self.timeDelay) * 1000), coordsID[r][i].configure(bg='orange'))
                win.update()
                iter.remove(checkNum)
                win.update()
                coordsID[r][c].configure(bg='white')
                coordsID[r][i].configure(bg='white', text=iter)

    def stepCol(self, c, r):
        for i in range(len(coordsContent[c])):
            iter = coordsContent[i][c]
            if len(iter) != 1 and checkNum in iter:
                displaySteps.insert(1.0, f'Using ({r}, {c}) to remove {checkNum} from ({i}, {c})\n')
                win.after(int(float(self.timeDelay) * 1000), coordsID[r][c].configure(bg='deep sky blue'))
                win.update()
                win.after(int(float(self.timeDelay) * 1000), coordsID[i][c].configure(bg='orange'))
                win.update()
                iter.remove(checkNum)
                win.update()
                coordsID[r][c].configure(bg='white')
                coordsID[i][c].configure(bg='white', text=iter)

    def stepBox(self, b, j):
        for box in range(len(boxContent[b])):
            iter = boxContent[b][box]
            if len(iter) != 1 and boxCheckNum in iter:
                displaySteps.insert(1.0, f'In Box {b}, using Cell {j} to remove {boxCheckNum} from Cell {box}\n')
                win.after(int(float(self.timeDelay) * 1000), boxID[b][j].configure(bg='deep sky blue'))
                win.update()
                win.after(int(float(self.timeDelay) * 1000), boxID[b][box].configure(bg='orange'))
                win.update()
                iter.remove(boxCheckNum)
                win.update()
                boxID[b][j].configure(bg='white')
                boxID[b][box].configure(bg='white', text=iter)

    def stepPigeon2(self, r, c, h, x):
        if x == 1:
            for i in range(rowNum):
                for num in self.p1_list1:
                    if num in coordsContent[r][i] and i != c and i != h and not len(coordsContent[r][i]) < 2:
                        displaySteps.insert(1.0, f'Using cells ({r}, {c}) and ({r}, {h}) to remove {num} from cell ({r}, {i})\n')
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][c].configure(bg='deep sky blue'))
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][h].configure(bg='deep sky blue'))
                        win.update()
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][i].configure(bg='orange'))
                        win.update()
                        coordsContent[r][i].remove(num)
                        win.update()
                        coordsID[r][c].configure(bg='white')
                        coordsID[r][h].configure(bg='white')
                        coordsID[r][i].configure(bg='white', text=coordsContent[r][i])
        else:
            for i in range(rowNum):
                for num in self.p1_list1:
                    if num in coordsContent[i][c] and i != r and i != h and not len(coordsContent[i][c]) < 2:
                        displaySteps.insert(1.0, f'Using cells ({r}, {c}) and ({h}, {c}) to remove {num} from cell ({i}, {c})\n')
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][c].configure(bg='deep sky blue'))
                        win.after(int(float(self.timeDelay) * 1000), coordsID[h][c].configure(bg='deep sky blue'))
                        win.update()
                        win.after(int(float(self.timeDelay) * 1000), coordsID[i][c].configure(bg='orange'))
                        win.update()
                        coordsContent[i][c].remove(num)
                        win.update()
                        coordsID[r][c].configure(bg='white')
                        coordsID[h][c].configure(bg='white')
                        coordsID[i][c].configure(bg='white', text=coordsContent[i][c])

    def stepPigeon3(self, r, c1, c2, c3, x):
        if x == 1:
            for i in range(rowNum):
                for num in self.p2_list1:
                    if num in coordsContent[r][i] and i != c1 and i != c2 and i != c3 and not len(coordsContent[r][i]) < 2:
                        displaySteps.insert(1.0, f'Using cells ({r}, {c1}), ({r}, {c2}), and ({r}, {c3}) to remove {num} from cell ({r}, {i})\n')
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][c1].configure(bg='deep sky blue'))
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][c2].configure(bg='deep sky blue'))
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][c3].configure(bg='deep sky blue'))
                        win.update()
                        win.after(int(float(self.timeDelay) * 1000), coordsID[r][i].configure(bg='orange'))
                        win.update()
                        coordsContent[r][i].remove(num)
                        win.update()
                        coordsID[r][c1].configure(bg='white')
                        coordsID[r][c2].configure(bg='white')
                        coordsID[r][c3].configure(bg='white')
                        coordsID[r][i].configure(bg='white', text=coordsContent[r][i])
        else:
            for i in range(colNum):
                for num in self.p2_list1:
                    if num in coordsContent[i][r] and i != c1 and i != c2 and i != c3 and not len(coordsContent[i][r]) < 2:
                        displaySteps.insert(1.0, f'Using cells ({c1}, {r}), ({c2}, {r}), and ({c3}, {r}) to remove {num} from cell ({i}, {r})\n')
                        win.after(int(float(self.timeDelay) * 1000), coordsID[c1][r].configure(bg='deep sky blue'))
                        win.after(int(float(self.timeDelay) * 1000), coordsID[c2][r].configure(bg='deep sky blue'))
                        win.after(int(float(self.timeDelay) * 1000), coordsID[c3][r].configure(bg='deep sky blue'))
                        win.update()
                        win.after(int(float(self.timeDelay) * 1000), coordsID[i][r].configure(bg='orange'))
                        win.update()
                        coordsContent[i][r].remove(num)
                        win.update()
                        coordsID[c1][r].configure(bg='white')
                        coordsID[c2][r].configure(bg='white')
                        coordsID[c3][r].configure(bg='white')
                        coordsID[i][r].configure(bg='white', text=coordsContent[i][r])

myTkinter()