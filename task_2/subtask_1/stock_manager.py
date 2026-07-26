def load_stock():
    stock={}
    try:
        with open("stock.txt","r") as file:
            for sentence in file:
                line=sentence.strip()
                parts=line.split(",")
                fruit=parts[0]
                quantity=parts[1]
                quantity=int(quantity)
                stock[fruit.lower()]=quantity
    except FileNotFoundError:
        print("error!!,file not found")
    except(ValueError,OSError):
        print("error!!,invalid format")
    return stock

def show_stock(stock):
    for i,(name,quantity ) in enumerate(stock.items(),1):
        print(f"{i}. {name} : {quantity}")

def add_stock(stock):
    show_stock(stock)
    sel=input("input the stock name or id:")
    if (sel.isdigit()):
        sel=int(sel)
        if (1<=sel and sel<=len(stock)):
          name=list(stock.keys())[sel-1]
        else:
            print("invalid id")
            return
    else:
        name=sel.lower()  
    amount=input("input the amount you want to add:")
    if not amount.isdigit() or int(amount)<=0:
        print("enter a positive number please..<3")
        return
    amount=int(amount)
    if name in stock:
        stock[name]+=amount
    else:
        stock[name]=amount   

def remove_stock(stock):
    show_stock(stock)
    sel=input("input the stock name or id:")
    if (sel.isdigit()):
        sel=int(sel)
        if (1<=sel and sel<=len(stock)):
          name=list(stock.keys())[sel-1]
        else:
            print("invalid id")
            return  
    else:
        name=sel.lower()
        if name not in stock:
            print("stock not found..")
            return
    amount=input("input the amount you want to remove:")
    if not amount.isdigit() or int (amount)<=0:
                print("enter a positive number please..<3")
                return
    amount=int(amount)
    if(amount>stock[name]):
            print("there is no sufficinet amount to remove..")
            return
    else:
            stock[name]-=amount

def save_stock(stock):
    with open ("stock.txt","w") as file:
        for name ,quantity in stock.items():
            file.write(f"{name},{quantity}\n")

def main():
    stock=load_stock()
    while True:
        print("input 1 to add stock")
        print("input 2 to remove stock")
        print("input 3 to show stock content")
        print("input 4 to exit the program")
        sel=int(input("input your choice:"))
        if sel==1:
            add_stock(stock)
        elif sel==2:
            remove_stock(stock)  
        elif sel==3:
            show_stock(stock)
        elif sel==4:
            print("exiting the program...<3")
            save_stock(stock) 
            break
        else:
            print("invalid choice!! please input a number from 1-4")


main()

