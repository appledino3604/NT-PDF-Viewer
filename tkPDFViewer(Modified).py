try:
    from tkinter import*
    import fitz
    from tkinter.ttk import Progressbar
    from threading import Thread
    import math
except Exception as e:
    print(f"This error occured while importing neccesary modules or library {e}")
global zoomdpi
# You edited this line^^^
class ShowPdf():
    


    img_object_li = []

    def pdf_view(self,master,width=1200,height=600,pdf_location="",bar=True,load="after",zoomDPI=72):
        global tag
        zoomdpi=zoomDPI
        
        self.frame = Frame(master,width= width,height= height)

        self.scroll_y = Scrollbar(self.frame,orient="vertical") 
        self.scroll_y.pack(fill="y",side="right")
        

        percentage_view = 0
        percentage_load = StringVar()

        if bar==True and load=="after":
            self.display_msg = Label(textvariable=percentage_load)
            self.display_msg.pack(pady=10)

            loading = Progressbar(self.frame,orient= HORIZONTAL,length=100,mode='determinate')
            loading.pack(side = TOP,fill=X)

        
        self.text = Canvas(master,yscrollcommand=self.scroll_y.set,width= width,height= height,bg="#f0f0f0",scrollregion=(0,0,0,10000),yscrollincrement=10)
        self.text.pack(side="left",expand=1)


        def add_img():
            precentage_dicide = 0
            open_pdf = fitz.open(pdf_location)

            for page in open_pdf:
                pix = page.get_pixmap(dpi=zoomDPI)
                
                pix1 = fitz.Pixmap(pix,0) if pix.alpha else pix
                img = pix1.tobytes("ppm")
                timg = PhotoImage(data = img)

                h=15+timg.height() 
                w=timg.width()
                
                self.img_object_li.append(timg)
                if bar==True and load=="after":
                    precentage_dicide = precentage_dicide + 1
                    percentage_view = (float(precentage_dicide)/float(len(open_pdf))*float(100))
                    loading['value'] = percentage_view
                    percentage_load.set(f"Loading your PDF {int(math.floor(percentage_view))}%")
            
            if bar==True and load=="after":
                loading.pack_forget()
                self.display_msg.pack_forget()
            s=len(self.img_object_li)*h
            self.text.config(width=w,scrollregion=(0,0,0,s))
            number=0
            iterator=0
            for i in self.img_object_li:
                number=number+1
                iterator=iterator+1
                
                if iterator == 1:
                    number=0
                    z=10
                
                height=h*number+z

                self.text.create_image(0,height,anchor=NW,image=i)

         
            self.text.configure(state="disabled")


        def start_pack():
            t1 = Thread(target=add_img)
            t1.start()

        if load=="after":
            master.after(250,start_pack)
        else:
            start_pack()

        return  self.text
   


def main():
    root = Tk()
    root.geometry("700x780")
    d = ShowPdf().pdf_view(root,pdf_location=r"D:\DELL\Documents\Encyclopedia GUI.pdf",width=50,height=200)
    d.pack()
    
    root.mainloop()

if __name__ == '__main__':
    main()
