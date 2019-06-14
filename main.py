import tkinter as tk
from tkinter import messagebox as mbox 
from tkinter import scrolledtext
from tkinter import ttk
import sqlite3

import os
root = tk.Tk()
root.title("Stock Management System")
tabcontrol = ttk.Notebook(root)
Inventory = ttk.Frame(tabcontrol)
labelFrame = ttk.LabelFrame(Inventory,text="Inventory Management")
labelFrame.grid(column=0,row=0,padx=8,pady=4,sticky="N")



#*************************************************************



tabcontrol1 = ttk.Notebook(root)
Inventory1 = ttk.Frame(tabcontrol1)

labelFrame1 = ttk.LabelFrame(Inventory,text="Product List",borderwidth=3)


labelFrame1.grid(row=0,column=1,padx=8,pady=4,sticky="N")

Inventory1.pack()


#******************************** Get DATA *******************************
i=0
def Get_data():
	global i
	global j
	i=0
	tree.delete(*tree.get_children())
	db = sqlite3.connect('test.db')
	cursor = db.execute('select * from stock')
	for row in cursor:
		tree.insert('', 'end', text="Item_"+str(i), values=(row[0],row[1],row[2],row[3]))
		i=i+1
# ===========Inserting into the table=====================
def Insert_data():
	try:

		# ==================check for item===================
		db = sqlite3.connect('test.db')
		cur = db.execute("""SELECT Product_Id FROM stock WHERE Product_Id=?""", [PRODUCT_ID_VALUE.get()])
		result = cur.fetchone()

		if result:
			mbox.askretrycancel("Warning", "Item already Exists!")
			
		else:
			db = sqlite3.connect('test.db')
			db.execute('insert into stock(Product_Id,Product_Name,Sell_Price,Quantity) values (?,?,?,?)',[PRODUCT_ID_VALUE.get(),PRODUCT_NAME_VALUE.get(),PRODUCT_PRICE_VALUE.get(),PRODUCT_QUANTITY_VALUE.get()])
			db.commit()
		# ==================================================
	except:
		print("Error")	
		mbox.askretrycancel("Warning", "Please Enter valid!")	
	global i
	global j
	i=0
	tree.delete(*tree.get_children())
	db = sqlite3.connect('test.db')
	cursor = db.execute('select * from stock')
	for row in cursor:
		tree.insert('', 'end', text="Item_"+str(i), values=(row[0],row[1],row[2],row[3]))
		i=i+1


def Update_data():
	try:
		db = sqlite3.connect('test.db')
		db.execute('update stock set Product_Id = ? ,Product_Name = ?,Sell_Price = ?,Quantity = ?  where Product_Id = ?',(PRODUCT_ID_VALUE.get(),PRODUCT_NAME_VALUE.get(),PRODUCT_PRICE_VALUE.get(),PRODUCT_QUANTITY_VALUE.get(),PRODUCT_ID_VALUE.get()))
		db.commit()
		i=0		
		tree.delete(*tree.get_children())
		db = sqlite3.connect('test.db')
		cursor = db.execute('select * from stock')
		for row in cursor:
			tree.insert('', 'end', text="Item_"+str(i), values=(row[0],row[1],row[2],row[3]))
			i=i+1
	except:
		print("Error")	
		mbox.askretrycancel("Warning", "Please Enter valid!")	
	finally:
		print("working")
		

def Delete_data():
	db = sqlite3.connect('test.db')
	mbox.askokcancel ('Alert!','Do you want to delete ?') 
	db.execute('delete from stock where Product_Id = ?',(PRODUCT_ID_VALUE.get(),))
	db.commit()
	i=0
	tree.delete(*tree.get_children())
	db = sqlite3.connect('test.db')
	cursor = db.execute('select * from stock')
	for row in cursor:
		tree.insert('', 'end', text="Item_"+str(i), values=(row[0],row[1],row[2],row[3]))
		i=i+1


#************************************ TREE VIEW *******************************************

tree = ttk.Treeview(labelFrame1, columns=('Product Id', 'Product Name','Sell Price','Quantity'),height=20)
tree.place(x=30, y=95)
vsb = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
vsb.place(x=30+954+5, y=0, height=200+220)

tree.configure(yscrollcommand=vsb.set)
tree.heading('#0', text='Item no.')
tree.heading('#1', text='Product id')
tree.heading('#2', text='Name')
tree.heading('#3', text='Sell Price')
tree.heading('#4', text='Quantity')
tree.column('#1', stretch=tk.YES)
tree.column('#2', stretch=tk.YES)
tree.column('#0', stretch=tk.YES)
tree.column('#3', stretch=tk.YES)
tree.column('#4', stretch=tk.YES)
tree.grid(row=11, columnspan=4, sticky='nsew')
tabcontrol1.pack(expand=0,fill="both")



#*********************************************************8
global PRODUCT_QUANTITY_VALUE
global PRODUCT_ID_VALUE
global PRODUCT_PRICE_VALUE
global PRODUCT_NAME_VALUE

PRODUCT_ID_VALUE = tk.StringVar()
PRODUCT_NAME_VALUE = tk.StringVar()
PRODUCT_PRICE_VALUE = tk.IntVar()
PRODUCT_QUANTITY_VALUE = tk.IntVar()

productId = ttk.Label(labelFrame,text="Product ID: ")
productIdEntry = ttk.Entry(labelFrame,textvariable=PRODUCT_ID_VALUE)
productIdEntry.grid(column=0,row=1,sticky='W')
productName = ttk.Label(labelFrame,text="Product Name : ")
 
productNameEntry = ttk.Entry(labelFrame,textvariable=PRODUCT_NAME_VALUE)

productPrice = ttk.Label(labelFrame,text="Sell Price : ")


productPriceEntry = ttk.Entry(labelFrame,textvariable=PRODUCT_PRICE_VALUE)


productPriceEntry.grid(column=0,row=5,sticky='W')
productQuantity = ttk.Label(labelFrame,text="Quantity : ")
 
productQuantityEntry = ttk.Entry(labelFrame,textvariable=PRODUCT_QUANTITY_VALUE)
 
productQuantityEntry.grid(column=0,row=7,sticky="W")
InsertButton = ttk.Button(labelFrame,text='Insert',command=Insert_data ,width=20)	
ShowButton = ttk.Button(labelFrame,text='Show name',command=Get_data)



style = ttk.Style()
style.configure('TButton', background='#3498db')


UpdateButton = ttk.Button(labelFrame,text='Update',command=Update_data,width=20)
DeleteButton = ttk.Button(labelFrame,text='Delete',command=Delete_data,width=20)
DeleteButton.grid(column=0,row=11,sticky='W',pady=7)
UpdateButton.grid(column=0,row=10,sticky='W')


InsertButton.grid(column=0,row=8,sticky='W',pady=7)
productQuantity.grid(column=0,row=6,sticky="W")
productPrice.grid(column=0,row=4,sticky='W')
productNameEntry.grid(column=0,row=3,sticky='W')
productName.grid(column=0,row=2,sticky='W')
productId.grid(column=0,row=0,sticky='W')
tabcontrol.add(Inventory,text='Inventory')
tabcontrol.pack(expand=1,fill="both")


#****************************************************************

tab2 = ttk.Frame(tabcontrol)
tabcontrol.add(tab2,text="Billing")
tabcontrol.pack(expand=1,fill="both")
#****************************************************************

#**************** Billing panel function **********************



global BILL_ID
global BILL_PRICE
global BILL_QT

BILL_ID = tk.StringVar()
BILL_PRICE = tk.StringVar()
BILL_QT = tk.StringVar()
global t

def Bill_add():
	try:
		db = sqlite3.connect('test.db')
		db.execute('delete from temp')
		x = db.execute('select Quantity from stock where Product_Id = ?',[BILL_ID.get()])
	except:
		mbox.askretrycancel("Warning", "Please Enter valid!")
	x = db.execute('select Quantity from stock where Product_Id = ?',[BILL_ID.get()])		
	for y in x:
		t=y[0]
	try:
		t = int(t)
		y = int(BILL_QT.get())
		z= t-y
		db.execute('update stock set Quantity = ? where Product_Id = ?',[z,BILL_ID.get()])
		q = db.execute('select * from stock where Product_Id = ?',[BILL_ID.get()])
		for w in q:
			a = int(BILL_QT.get())
			a=int(a)
			b=w[2]
			b=int(b)
			db.execute('insert into temp values(?,?,?,?)',[w[0],w[1],w[2],a*b])
		db.commit()
		i=0
		db = sqlite3.connect('test.db')
		cursor = db.execute('select * from temp')
		tree1.delete(*tree1.get_children())
		for row in cursor:
			tree1.insert('', 'end', text="Item_"+str(i), values=(row[0],row[1],row[2],row[3]))
			i=i+1
	except:
		mbox.askretrycancel("Error","Product not found, try again?")

db = sqlite3.connect('test.db')
cursor = db.execute('select * from stock')
for row in cursor:
	tree.insert('', 'end', text="Item_"+str(i), values=(row[0],row[1],row[2],row[3]))
	i=i+1


def Bill_total():
	db = sqlite3.connect("test.db")
	cursor = db.execute('select sum(Quantity) from temp')
	total = 0
	for row in cursor:
		total = row[0]

	print(total)
	tree1.insert('', 'end', text="---------", values=('----------','---------','Total = ',total))
	db.commit()

def Bill_print():
	i=0
	lst = []
	db = sqlite3.connect('test.db')
	cursor = db.execute('select * from temp')
	tree1.delete(*tree1.get_children())
	for row in cursor:
		values=(row[0],row[1],row[2],row[3])
		lst= list(values)
		text="Item_"+str(i)
	print(lst)
	f = open("file.txt","a+")
	f.writelines("Product ID \t Name\tSell Price\tTotal \n")
	m= len(lst)
	for i in range(0,m):
		f.write(lst[i]+"\t\t")
	db = sqlite3.connect("test.db")
	cursor = db.execute('select sum(Quantity) from temp')
	total = 0
	for row in cursor:
		total = row[0]
	print(total)
	f.writelines("\n=============================================================================================\n\t\t\t\t\t\t\t\t\t")
	
	f.write(str(total))
	f.writelines("\n=============================================================================================")
	f.close()
	mbox.showinfo("Message","Successfull!")	
		
	





#******************************** Billing Panel *************************************

BillingFrame = ttk.LabelFrame(tab2,text="Billing")
BillingFrame.grid(column=0,row=0,pady=4,padx=8,sticky='N')
Billing_product_id = ttk.Label(BillingFrame,text="Product Id :")


Billing_product_id.grid(row=0,column=0,sticky='W')
Billing_product_id_Entry = ttk.Entry(BillingFrame,textvariable=BILL_ID)
 
Billing_product_id_Entry.grid(column=0,row=1,sticky='W')
Billing_PRODUCT_QUANTITY = ttk.Label(BillingFrame,text="Quantity :")
 
Billing_PRODUCT_QUANTITY.grid(column=0,row=2,sticky='W')
Billing_PRODUCT_QUANTITY_Entry = ttk.Entry(BillingFrame,textvariable=BILL_QT)

Billing_PRODUCT_QUANTITY_Entry.grid(column=0,row=3,sticky='w')
Billing_PRODUCT_Price = ttk.Label(BillingFrame,text="Price :")
Billing_PRODUCT_Price.config(font=("Courier",20))
 
Billing_PRODUCT_Price_Entry = ttk.Entry(BillingFrame,textvariable=BILL_PRICE)
 
Billing_Add_Button = ttk.Button(BillingFrame,text="Add",command=Bill_add, width="20")
Billing_Add_Button.grid(column=0,row=6,sticky='W',pady=7)
 
Billing_Print_Button = ttk.Button(BillingFrame,text="Total",width=20,command=Bill_total)
Billing_Print_Button.grid(column=0,row=7,sticky='W')
Billing_Print_Button = ttk.Button(BillingFrame,text="Print",width=20,command=Bill_print)
Billing_Print_Button.grid(column=0,row=8,sticky='W',pady=7)

#***********************************************************************

tabcontrol2 = ttk.Notebook(root)
Inventory2 = ttk.Frame(tabcontrol2)

labelFrame2 = ttk.LabelFrame(tab2,text="Product List",borderwidth=3)
 

labelFrame2.grid(row=0,column=1,padx=8,pady=4,sticky="N")

Inventory2.pack()

#*************** Billing Tree View ***************************************************

tree1 = ttk.Treeview(labelFrame2, columns=('Product Id', 'Product Name','Sell Price','Total'),height=20)
tree1.place(x=30, y=95)
vsb = ttk.Scrollbar(tree1, orient="vertical", command=tree.yview)
vsb.place(x=30+954+5, y=0, height=200+220)

tree1.configure(yscrollcommand=vsb.set)
tree1.heading('#0', text='Item no.')
tree1.heading('#1', text='Product id')
tree1.heading('#2', text='Name')
tree1.heading('#3', text='Sell Price')
tree1.heading('#4', text='Total')
tree1.column('#1', stretch=tk.YES)
tree1.column('#2', stretch=tk.YES)
tree1.column('#0', stretch=tk.YES)
tree1.column('#3', stretch=tk.YES)
tree1.column('#4', stretch=tk.YES)
tree1.grid(row=11, columnspan=4, sticky='nsew')



root.mainloop()
