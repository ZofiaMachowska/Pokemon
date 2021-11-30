import queue
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from xmlrpc.client import ServerProxy
import threading
import time

#na błędy funkcje


def Error_message(informacja):
    messagebox.showerror("Błąd", informacja)


def Warning_message(informacja):
    messagebox.showwarning("Ostrzeżenie", informacja)


def Info_message(informacja):
    messagebox.showinfo("Informacja", informacja)

playerId = -1
gameName = -1
pokmonJustDied = False;

def setPlayerId(value):
    global playerId
    playerId = value


def setGameName(value):
    global gameName
    gameName = value


def getPlayerId():
    return playerId


def getGameName():
    return gameName


#sama apka
class Pokmony(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self, height=600, width=900)
        container.pack()
        self.config(bg='#476b6b', height=600, width=900)
        self.resizable(width=False, height=False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.currentFrameType = StartPage
        thread = threading.Thread(target=main,args=[self])
        thread.start()

        for F in (StartPage, CreateGamePage, JoinGamePage, PokemonPage, BattlePage, PokemonSwitchPage):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        self.currentFrameType = cont
        frame = self.frames[cont]
        frame.tkraise()
        if cont == PokemonSwitchPage:
            print("YES")
            frame.RefreshPage()


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent,height=600, width=900, bg='#ff9966')
        name = "StartPage"
        title_top = Label(self, text="POKMON", bg='#ff9966')
        title_top.config(font=("Courier", 110))
        title_top.place(height=146, width=530, x=185, y=55)

        button_dolacz = Button(self, text="Dołącz do gry", bg='#ffdccc', command=lambda: controller.show_frame(JoinGamePage))
        button_dolacz.config(font=("Courier", 18))
        button_dolacz.place(height=103, width=210, x=101, y=336)

        button_utworz = Button(self, text="Utwórz grę", bg='#ffdccc', command=lambda: controller.show_frame(CreateGamePage))
        button_utworz.config(font=("Courier", 18))
        button_utworz.place(height=103, width=210, x=588, y=336)


class CreateGamePage(Frame):
    def __init__(self, parent, controller):
        def OnCreateNewGameButtonClicked(entry_1, entry_2):
            newGameName = entry_1.get()
            newGamePassword = entry_2.get()

            returnObject = server.TryCreateNewGame(newGameName, newGamePassword)
            print(returnObject)

            if returnObject["successful"]:
                setPlayerId(returnObject["playerId"])
                setGameName(returnObject["gameName"])
                print(playerId)
                Info_message("Successfully created a new game \n\nName: " + newGameName+"\n\nPassword: "+newGamePassword)
                controller.show_frame(PokemonPage)

            else:
                Error_message(returnObject["errorMessage"])

        Frame.__init__(self, parent,height=600, width=900,bg='#ff9966')
        title_top = Label(self, text="STWÓRZ GRĘ", bg='#ff9966')
        title_top.config(font=("Courier", 50))
        title_top.place(height=80, width=530, x=185, y=33)

        label_1 = Label(self, text="Nazwa:", bg='#ff9966')
        label_1.config(font=("Courier", 30))
        label_1.place(height=64, width=210, x=165, y=206)

        entry_1 = Entry(self)
        entry_1.config(font=("Courier", 20))
        entry_1.place(height=45, width=340, x=394, y=215)

        label_2 = Label(self, text="Hasło:", bg='#ff9966')
        label_2.config(font=("Courier", 30))
        label_2.place(height=64, width=210, x=165, y=285)

        entry_2 = Entry(self)
        entry_2.config(font=("Courier", 20))
        entry_2.place(height=45, width=340, x=394, y=294)
#,
        button_utworz = Button(self, text="Stwórz", bg='#ffdccc', command=lambda:[OnCreateNewGameButtonClicked(entry_1, entry_2)])
        button_utworz.config(font=("Courier", 30))
        button_utworz.place(height=103, width=210, x=345, y=428)


class JoinGamePage(Frame):
    def __init__(self, parent, controller):
        def OnJoinGameButtonClicked(entry_1, entry_2):
            gameName = entry_1.get()
            gamePassword = entry_2.get()

            returnObject = server.TryJoinGame(gameName, gamePassword)

            if returnObject["successful"]:
                setPlayerId(returnObject["playerId"])
                setGameName(returnObject["gameName"])
                print(playerId)
                Info_message("Successfully joined game " + gameName)
                controller.show_frame(PokemonPage)

            else:
                Error_message(returnObject["errorMessage"])


        # Confirm pokmon list
        Frame.__init__(self, parent,height=600, width=900,bg='#ff9966')
        title_top = Label(self, text="DOŁĄCZ DO GRY", bg='#ff9966')
        title_top.config(font=("Courier", 50))
        title_top.place(height=80, width=530, x=185, y=33)

        label_1 = Label(self, text="Nazwa:", bg='#ff9966')
        label_1.config(font=("Courier", 30))
        label_1.place(height=64, width=210, x=165, y=206)

        entry_1 = Entry(self)
        entry_1.config(font=("Courier", 20))
        entry_1.place(height=45, width=340, x=394, y=215)

        label_2 = Label(self, text="Hasło:", bg='#ff9966')
        label_2.config(font=("Courier", 30))
        label_2.place(height=64, width=210, x=165, y=285)

        entry_2 = Entry(self)
        entry_2.config(font=("Courier", 20))
        entry_2.place(height=45, width=340, x=394, y=294)

        button_utworz = Button(self, text="Dołącz", bg='#ffdccc' , command=lambda: [OnJoinGameButtonClicked(entry_1, entry_2)])
        button_utworz.config(font=("Courier", 30))
        button_utworz.place(height=103, width=210, x=345, y=428)


class BattlePage(Frame):
    def __init__(self, parent, controller):
        def ChangingWidgetsOptions(mainwin, Bottom_Text, Bottom_Button1, Bottom_Button2,Bottom_Action0, Bottom_Action1, Bottom_Action2, Bottom_Action3, Bottom_Action5,Bottom_Action6, Bottom_Text_Action):

            Bottom_Button1 = Button(mainwin, bg='#339966', text='FIGHT', command=lambda: OnFightButtonClicked(mainwin, Bottom_Text, Bottom_Button1, Bottom_Button2, Bottom_Action0, Bottom_Action1, Bottom_Action2, Bottom_Action3, Bottom_Action5,Bottom_Action6, Bottom_Text_Action))
            Bottom_Button1.config(font=("Courier", 20))
            Bottom_Button1.place(height=121, width=190, x=467, y=459)

            Bottom_Button2 = Button(mainwin, bg='#dea0c0', text='POKMON', command=lambda: OnPokmonSwitchButtonClicked(controller))
            Bottom_Button2.config(font=("Courier", 20))
            Bottom_Button2.place(height=121, width=190, x=689, y=459)

            Bottom_Text.config(font=("Courier", 18), bg='#e1eaea')
            Bottom_Text.place(height=121, width=420, x=15, y=459)

            self.messageTextVisible = True

            Bottom_Action0.place_forget()
            Bottom_Action1.place_forget()
            Bottom_Action2.place_forget()
            Bottom_Action3.place_forget()
            Bottom_Action5.place_forget()
            Bottom_Action6.place_forget()
            Bottom_Text_Action.place_forget()

        def ChangingWidgetsAction(mainwin, Bottom_Text, Bottom_Button1, Bottom_Button2,Bottom_Action0, Bottom_Action1, Bottom_Action2, Bottom_Action3, Bottom_Action5,Bottom_Action6, Bottom_Text_Action):
            Bottom_Text_Action.config(font=("Courier", 18), bg='#e1eaea', text="")
            Bottom_Text_Action.place(height=121, width=305, x=450, y=459)
            Bottom_Action5 = Button(mainwin, bg='#339966', text='Zatwierdź',
                                    command=lambda:[ChangingWidgetsOptions(mainwin, Bottom_Text, Bottom_Button1, Bottom_Button2, Bottom_Action0, Bottom_Action1, Bottom_Action2, Bottom_Action3, Bottom_Action5, Bottom_Action6, Bottom_Text_Action), PerformAttack()])
            Bottom_Action5.config(font=("Courier", 15))
            Bottom_Action5.place(height=60, width=125, x=768, y=460)

            Bottom_Action6 = Button(mainwin, bg='#339966', text='Powrót',
                                    command=lambda: ChangingWidgetsOptions(mainwin, Bottom_Text, Bottom_Button1, Bottom_Button2, Bottom_Action0, Bottom_Action1, Bottom_Action2, Bottom_Action3, Bottom_Action5, Bottom_Action6, Bottom_Text_Action))
            Bottom_Action6.config(font=("Courier", 15))
            Bottom_Action6.place(height=60, width=125, x=768, y=521)

            self.messageTextVisible = False

            Bottom_Text.place_forget()
            Bottom_Button1.place_forget()
            Bottom_Button2.place_forget()

        def OnPokmonSwitchButtonClicked(controller):
            if not self.myTurn:
                return
            self.forceSwitch = False
            controller.show_frame(PokemonSwitchPage)

        def OnFightButtonClicked(mainwin, Bottom_Text, Bottom_Button1, Bottom_Button2, Bottom_Action0, Bottom_Action1, Bottom_Action2, Bottom_Action3, Bottom_Action5, Bottom_Action6, Bottom_Text_Action):
            # SERVER
            if not self.myTurn:
                return
            if self.forceSwitch:
                self.DisplayMessageFromQueue(message="You must switch pokemon!")
                return
            returnObject = None
            self.awaitingServerResponse = True
            while True:
                try:
                    if returnObject is not None:
                        break
                    returnObject = server.TryGetPokmonAttacks(getPlayerId(), getGameName())
                    break
                except:
                    print("Handled connection error has occurred!")

            self.awaitingServerResponse = False
            attacksArr = returnObject["attacksList"]

            if returnObject["successful"]:

                Bottom_Action0 = Button(mainwin, bg='#dea0c0', text=attacksArr[0], command=lambda: OnAttackButtonClicked(0, Bottom_Text_Action))
                Bottom_Action0.config(font=("Courier", 20))
                Bottom_Action0.place(height=60, width=210, x=15, y=460)

                Bottom_Action1 = Button(mainwin, bg='#dea0c0', text=attacksArr[1], command=lambda: OnAttackButtonClicked(1, Bottom_Text_Action))
                Bottom_Action1.config(font=("Courier", 20))
                Bottom_Action1.place(height=60, width=210, x=226, y=460)

                Bottom_Action2 = Button(mainwin, bg='#dea0c0', text=attacksArr[2], command=lambda: OnAttackButtonClicked(2, Bottom_Text_Action))
                Bottom_Action2.config(font=("Courier", 20))
                Bottom_Action2.place(height=60, width=210, x=15, y=521)

                Bottom_Action3 = Button(mainwin, bg='#dea0c0', text=attacksArr[3], command=lambda: OnAttackButtonClicked(3, Bottom_Text_Action))
                Bottom_Action3.config(font=("Courier", 20))
                Bottom_Action3.place(height=60, width=210, x=226, y=521)

                ChangingWidgetsAction(self, Bottom_Text, Bottom_Button1, Bottom_Button2,Bottom_Action0, Bottom_Action1, Bottom_Action2, Bottom_Action3, Bottom_Action5,Bottom_Action6, Bottom_Text_Action)
            else:
                Error_message(returnObject["errorMessage"])

        def OnAttackButtonClicked(buttonId, Bottom_Text_Action):#SERVER

            self.awaitingServerResponse = True
            while True:
                try:
                    returnObject = server.TryGetPokmonAttacksDescription(getPlayerId(), getGameName(), buttonId)
                    break
                except:
                    print("Handled connection error has occurred!")

            self.awaitingServerResponse = False
            self.attackId = buttonId

            if returnObject["successful"]:
                # attackDescription.config(text=returnObject.attacksArr[buttonId].description)
                # Bottom_Text_Action = Label(mainwin, bg='#e1eaea', text=returnObject.attacksArr[buttonId].description)
                opis = returnObject["description"]
                Bottom_Text_Action.config(font=("Courier", 18), bg='#e1eaea', text=opis)
                Bottom_Text_Action.place(height=121, width=305, x=450, y=459)
            else:
                Error_message(returnObject["errorMessage"])

        def PerformAttack():
            self.awaitingServerResponse = True
            while True:
                try:
                    server.TryPerformAttack(gameName, playerId, self.attackId)
                    break
                except:
                    print("Handled connection error has occurred!")
            self.awaitingServerResponse = False
            self.Bottom_Text.config(text="")

        Frame.__init__(self, parent, height=600, width=900, bg='#476b6b')
        Player1_panel = Label(self, bg='#d1e0e0')
        Player1_panel.place(height=91, width=415, x=0, y=72)
        # img = ImageTk.PhotoImage(Image.open('pikaczu.png'))
        Player1_imag = Label(self, bg='#476b6b')  # , image=img)
        Player1_imag.place(height=200, width=200, x=589, y=17)

        self.Player1_name = Label(self, bg='#d1e0e0', text='NAME1')
        self.Player1_name.config(font=("Courier", 30))
        self.Player1_name.place(height=38, width=300, x=15, y=79)

        self.Player1_hp = Label(self, bg='#d1e0e0', text='HP:100/100')
        self.Player1_hp.config(font=("Courier", 30))
        self.Player1_hp.place(height=40, width=331, x=72, y=123)

        Player2_panel = Label(self, bg='#d1e0e0')
        Player2_panel.place(height=91, width=415, x=485, y=287)

        self.Player2_name = Label(self, bg='#d1e0e0', text='NAME2')
        self.Player2_name.config(font=("Courier", 30))
        self.Player2_name.place(height=38, width=300, x=508, y=297)

        self.Player2_hp = Label(self, bg='#d1e0e0', text='HP:100/100')
        self.Player2_hp.config(font=("Courier", 30))
        self.Player2_hp.place(height=40, width=331, x=562, y=338)

        Player2_imag = Label(self, bg='#476b6b')  # , image=img)
        Player2_imag.place(height=200, width=200, x=108, y=232)

        Bottom_Panel = Label(self, bg='#94b8b8')
        Bottom_Panel.place(height=160, width=900, x=0, y=440)

        Bottom_Text_panel = Label(self, bg='#e1eaea')
        Bottom_Text_panel.place(height=121, width=420, x=15, y=459)

        self.Bottom_Text = Label(self)
        Bottom_Button1 = Button(self)
        Bottom_Button2 = Button(self)

        Bottom_Action0 = Button(self)
        Bottom_Action1 = Button(self)
        Bottom_Action2 = Button(self)
        Bottom_Action3 = Button(self)
        Bottom_Text_Action = Label(self)
        Bottom_Action5 = Button(self)
        Bottom_Action6 = Button(self)
        # OnStartBottomText(Bottom_Text) #startowe wartości tych
        ChangingWidgetsOptions(self, self.Bottom_Text, Bottom_Button1, Bottom_Button2, Bottom_Action0, Bottom_Action1, Bottom_Action2, Bottom_Action3, Bottom_Action5, Bottom_Action6, Bottom_Text_Action)

        self.awaitingServerResponse = False
        self.state = -1
        self.myTurn = False
        self.messageQueue = queue.Queue(50)

        self.messageTextVisible = True

        self.messageDelay = 0
        self.maxHp1 = -1
        self.maxHp2 = -1

        self.attackId = -1
        self.forceSwitch = False

    def SetPlayerHpLabelWithMaxHp(self, newHp: int, maxHp: int):
        self.maxHp1 = maxHp
        print(maxHp)
        self.SetPlayerHpLabel(newHp)

    def SetEnemyHpLabelWithMaxHp(self, newHp: int, maxHp: int):
        self.maxHp2 = maxHp
        self.SetEnemyHpLabel(newHp)

    def SetPlayerHpLabel(self, newHp: int):
        print(self.maxHp1)
        self.Player1_hp.config(text="HP:" + str(newHp) + "/"+str(self.maxHp1))

    def SetEnemyHpLabel(self, newHp: int):
        self.Player2_hp.config(text="HP:" + str(newHp) + "/"+str(self.maxHp2))

    def SetPlayerPokmonNameLabel(self, name):
        self.Player1_name.config(text=name)

    def SetEnemyPokmonNameLabel(self, name):
        self.Player2_name.config(text=name)

    def AddMessageToQueue(self, message):
        self.messageQueue.put(message)

    def DisplayMessageFromQueue(self, message=""):
        if not message == "":
            self.Bottom_Text.config(text=message)
            self.messageDelay = 3
        if not self.messageTextVisible:
            return
        if self.messageDelay > 0:
            self.messageDelay = self.messageDelay - 1
            return
        if self.messageQueue.empty():
            if self.myTurn:
                print("What will you do?")
                self.Bottom_Text.config(text="What will you do?")
            else:
                print("Waiting for my opponent")
                self.Bottom_Text.config(text="Waiting for my opponent")
            return
        messageText = self.messageQueue.get()
        self.messageDelay = 3
        self.Bottom_Text.config(text=messageText)


class PokemonPage(Frame):
    def __init__(self, parent, controller):
        def OnPokemonButtonClicked():
            serverResponse = server.GetAllPokmonList()
            returnList = []
            for pok in serverResponse:
                returnList.append(pok["name"]+" "+pok["type"])
            return returnList

        def OnPokmonSelectionConfirmButtonClicked(myPokmonList):#SERVER
            if len(myPokmonList.curselection()) < 3:
                self.SetAwaitLabelCustom("Less then 3 pokmons selected!")
                return
            pokmons = []

            for index in myPokmonList.curselection():
                pokmons.append(myPokmonList.get(index).split()[0])

            self.awaitingServerResponse=True
            while True:
                try:
                    server.SetPlayerPokmons(gameName, playerId, pokmons)
                    break
                except:
                    print("Handled connection error has occurred!")

            self.awaitingServerResponse = False
            self.Ready = True

        Frame.__init__(self, parent, height=600, width=900, bg='#ff9966')
        title_top = Label(self, text="WYBIERZ POKMONY", bg='#ff9966')
        title_top.config(font=("Courier", 43))
        title_top.place(height=80, width=530, x=185, y=33)
        pokmon_list = OnPokemonButtonClicked()
        myPokmonList = PokmonList(self, pokmon_list)

        self.awaitLabel = Label(self, text="Waiting for a second player", bg='#ff9966')
        self.awaitLabel.config(font=("Courier", 12))
        self.awaitLabel.place(height=80, width=830, x=185, y=400)

        button_zatw = Button(self, text="Zatwierdź", command=lambda: [OnPokmonSelectionConfirmButtonClicked(myPokmonList.listbox)])
        button_zatw.config(font=("Courier", 20))
        button_zatw.place(height=80, width=210, x=345, y=476)

        #img = ImageTk.PhotoImage(Image.open('pikaczu.png'))
        panel = Label(self,  height=200, width=200, bg='#ff9966') #image=img,
        panel.place(height=200, width=200, x=546, y=175)
        self.infodelay = 0
        self.Ready = False
        self.controller = controller
        self.awaitingServerResponse=False

    def SetAwaitLabelCustom(self, myText):
        self.awaitLabel.config(text=myText)
        self.infodelay = 2

    def SetAwaitLabel(self, otherJoined, otherReady):
        if self.infodelay > 0:
            self.infodelay = self.infodelay-1
            return
        if not otherJoined:
            self.awaitLabel.config(text="Waiting for a second player.")
        if otherJoined:
            self.awaitLabel.config(text="Other player joined! Waiting for their Pokmon selection.")
        if otherReady:
            if self.Ready:
                self.controller.show_frame(BattlePage)
                print("YES")
            self.awaitLabel.config(text="Other player is ready!.")


class PokmonList:
        def __init__(self, mainwin, pokmon_list):
            self.mainwin = mainwin
            self.listbox = Listbox(self.mainwin, selectmode=MULTIPLE)
            self.listbox.place(height=256, width=330, x=152, y=147)
            self.listbox.config(font=("Courier", 11))
            self.listbox.bind("<<ListboxSelect>>", self.callback)
            j = 0
            for i in pokmon_list:
                self.listbox.insert(j, i)
                j = j + 1
            self.selection = self.listbox.curselection()

        def callback(self, a):
            if len(self.listbox.curselection()) > 3:
                for i in self.listbox.curselection():
                    if i not in self.selection:
                        self.listbox.selection_clear(i)
            self.selection = self.listbox.curselection()


class PokemonSwitchPage(Frame):
    def __init__(self, parent, controller):
        def OnPokemonButtonClicked():#SERVER
            returnList = []
            if playerId == -1:
                return returnList
            serverResponse = server.TryGetChosenPokmonList(gameName, playerId)
            for pok in serverResponse:
                returnList.append(pok["name"] + " " + pok["type"])
            return returnList

        def OnPokmonSelectionConfirmButtonClicked(myPokmonList):#SERVER
            global pokmonJustDied
            pokmon = myPokmonList.get(ACTIVE)
            print(pokmon)
            while True:
                try:
                    server.TrySetActivePokmon(gameName, playerId, pokmon.split()[0], pokmonJustDied)
                    break
                except:
                    print("Line busy")
            pokmonJustDied = False



        Frame.__init__(self, parent,height=600, width=900,bg='#ff9966')
        title_top= Label(self, text="WYBIERZ POKMONY", bg='#ff9966')
        title_top.config(font=("Courier", 43))
        title_top.place(height=80, width=530, x=185, y=33)
        pokmon_list = OnPokemonButtonClicked()
        self.listbox = Listbox(self, selectmode=SINGLE)
        self.listbox.place(height=80, width=332, x=146, y=235)
        self.listbox.config(font=("Courier", 16))
        for pokmon in pokmon_list:
            self.listbox.insert(1, pokmon)

        button_zatw=Button(self,text="Zatwierdź", command=lambda: [OnPokmonSelectionConfirmButtonClicked(self.listbox), controller.show_frame(BattlePage)])
        button_zatw.config(font=("Courier", 20))
        button_zatw.place(height=103, width=170, x=277, y=437)

        button_zatw=Button(self,text="Powrót", command=lambda: controller.show_frame(BattlePage))
        button_zatw.config(font=("Courier", 20))
        button_zatw.place(height=103, width=170, x=478, y=437)

        #img = ImageTk.PhotoImage(Image.open('pikaczu.png'))
        panel = Label(self, height=200, width=200, bg='#ff9966') #image=img
        panel.place(height=200, width=200, x=546, y=175)

    def RefreshPage(self):
        self.listbox.delete(0, END)
        returnList = []
        if playerId == -1:
            return returnList
        while True:
            try:
                serverResponse = server.TryGetChosenPokmonList(gameName, playerId)
                break
            except:
                print("Line busy")

        for pok in serverResponse:
            returnList.append(pok["name"] + " " + pok["type"])
        for pokmon in returnList:
            self.listbox.insert(1, pokmon)


def UpdateBattlePage(battlePage):
    if battlePage.awaitingServerResponse:
        return
    try:
        response = server.GetBattlePageData(playerId, gameName, battlePage.state)
        if response is not False:
            print(response)
            battlePage.state = response["state"]
            battlePage.myTurn = response["turn"]

            battlePage.SetPlayerPokmonNameLabel(response["myPokmonName"])
            battlePage.SetEnemyPokmonNameLabel(response["otherPokmonName"])

            battlePage.SetPlayerHpLabelWithMaxHp(response["playerHp"], response["playerMaxHp"])
            battlePage.SetEnemyHpLabelWithMaxHp(response["otherHp"], response["otherMaxHp"])

            if response["playerHp"] <= 0:
                global pokmonJustDied
                pokmonJustDied = True
                battlePage.forceSwitch=True

            for message in response["messages"]:
                battlePage.AddMessageToQueue(message)
    except:
        print("A handled server connection exception occured!")
    battlePage.DisplayMessageFromQueue()
    time.sleep(0.1)


def UpdatePokemonPage(pokmonPage):
    if pokmonPage.awaitingServerResponse:
        return
    try:
        response = server.CheckIfSecondPlayerReady(gameName, playerId)
        print(response)
        pokmonPage.SetAwaitLabel(response["inGame"], response["Ready"])

    except:
        print("A handled server connection exception occured!")
    time.sleep(1)


def main(window):
    print(1)
    while run:
        if window.currentFrameType == BattlePage:
            UpdateBattlePage(window.frames[window.currentFrameType])
        if window.currentFrameType == PokemonPage:
            UpdatePokemonPage(window.frames[window.currentFrameType])

print(0)
server = ServerProxy("http://localhost:5000")
print(2)
run = True
app = Pokmony()
app.mainloop()
run = False
print(3)

