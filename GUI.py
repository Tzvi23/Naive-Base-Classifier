# Author: Tzvi Puchinsky
from Tkinter import *
import tkFileDialog,tkMessageBox


class GUI:
    def __init__(self, root, struct, model):
        root.title("Naive Bayes Classifier")
        root.geometry("800x375")
        frame1 = Frame(root)
        frame2 = Frame(root)
        frame3 = Frame(root)
        frame4 = Frame(root)
        frame5 = Frame(root)
        frame0 = Frame(root)

        frame0.place(x=100, y=25)
        frame1.place(x=5, y=100)
        frame2.place(x=5, y=140)
        frame3.place(x=300, y=200)
        frame4.place(x=300, y=250)
        frame5.place(x=300, y=300)

        lbl0 = Label(frame0, text="Naive Bayes Classifier", font="Courier 15 bold", width=50)
        lbl0.pack()
        lbl01 = Label(frame0, text="By Tzvi Puchinsky", width=50)
        lbl01.pack()

        # First Row
        lbl1 = Label(frame1, text="Directory Path", width=20)
        lbl1.pack(side=LEFT)

        entry1 = Entry(frame1, width=80)
        entry1.pack(side=LEFT)

        def browse():
            try:
                entry1.delete(0, END)
                root.directory = tkFileDialog.askdirectory()
                print (root.directory)
                entry1.insert(0, root.directory)
                model.struct.build_structure(root.directory)
                model.set_data(root.directory)
                build_button.configure(state=NORMAL)
            except Exception as e:
                print(e)
                tkMessageBox.showerror("Error!", "Choose Correct Directory!")

        # Browse button
        browse_button = Button(frame1, text="Browse", command=browse)
        browse_button.pack(side=LEFT)
        # Second Row
        lbl2 = Label(frame2, text="Discretization Bin", width=20)
        lbl2.pack(side=LEFT)

        bins = ""

        def click(key):
            if entry2.get() == "Enter Number Of Bins":
                entry2.delete(0, END)
            frame2.update_idletasks()
            bins = entry2.get()
            print "Bins: {0}".format(bins)

        # discretization bins
        entry2 = Entry(frame2, width=30)
        entry2.insert(0, "Enter Number Of Bins")
        entry2.pack(side=LEFT)
        entry2.bind("<Key>", click)

        def build_b():
            try:
                browse_button.configure(state=DISABLED)
                build_button.configure(state=DISABLED)
                classify_button.configure(state=DISABLED)
                yes_dict = {}
                no_dict = {}
                bins = entry2.get()
                userCols = int(bins)
                if model.probability_attribute_to_yes == {}:
                    raise ValueError("Build model first!")
                if userCols <= 0:
                    raise ValueError("Bins need to be more than 0")
                out = open(model.struct.root_path + "/output.txt", "w")
                lbl4 = Label(frame5, text="Classifier Working! \n It'll take several minutes", width=30, fg="red")
                lbl4.pack()
                root.update()
                for i in range(1, len(model.testData)):
                    lbl5 = Label(frame5, text="Currently Processing: " + str(i) + "/" + str(len(model.testData)),
                                 width=30,
                                 fg="red")
                    lbl5.pack()
                    root.update()
                    ans = model.activate_model(i, userCols, yes_dict, no_dict)
                    if ans == 1:
                        out.write(str(i) + "  Yes \n")
                    else:
                        out.write(str(i) + "  No \n")
                    lbl5.pack_forget()
                    root.update()
                out.close()
                lbl4.pack_forget()
                root.update()
                tkMessageBox.showinfo("Classifier Complete", "Finished Classifying \n Check output.txt")
                root.quit()
                browse_button.configure(state=NORMAL)
                build_button.configure(state=NORMAL)
                classify_button.configure(state=NORMAL)
            except ValueError as e:
                print(e)
                if e.message == "Build model first!":
                    tkMessageBox.showerror("Error!", "Build model first!")
                else:
                    tkMessageBox.showerror("Error!", "Number Bins need to be more than 0 and Integer")
            except TclError as e:
                print(e)
            except Exception as e:
                print(e)
                lbl5.pack_forget()
                lbl4.pack_forget()
                root.update()
                tkMessageBox.showerror("Error!", "Check Directory and Number bins")

        def build_m():
            try:
                bins = entry2.get()
                userCols = int(bins)
                if userCols <= 0:
                    raise ValueError("Bins need to be more than 0")
                if entry1.get() == "":
                    raise ValueError("No Model Exists")
                browse_button.configure(state=DISABLED)
                build_button.configure(state=DISABLED)
                classify_button.configure(state=DISABLED)
                lbl5 = Label(frame5, text="Working, Please Wait!", width=30, fg="red")
                lbl5.pack()
                root.update()
                model.build_model(userCols)
                lbl5.pack_forget()
                root.update()
                tkMessageBox.showinfo("Model Complete", "Building classifier using train-set is done!")
                browse_button.configure(state=NORMAL)
                build_button.configure(state=NORMAL)
                classify_button.configure(state=NORMAL)
            except ValueError as e:
                print(e)
                if e.message == "Bins need to be more than 0":
                    tkMessageBox.showerror("Error!", "Number Bins need to be more than 0 and Integer")
                else:
                    tkMessageBox.showerror("Error!", "No Model Exists")
            except Exception as e:
                print(e)
                tkMessageBox.showerror("Error!", "Check Directory and Number bins")

        # Button Build
        build_button = Button(frame3, text="Build", state=DISABLED, width=30, command=build_m)
        build_button.pack()

        # Button Classify
        classify_button = Button(frame4, text="Classify", state=DISABLED, width=30, command=build_b)
        classify_button.pack()

        root.mainloop()
