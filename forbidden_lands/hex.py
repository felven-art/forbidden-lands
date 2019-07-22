from PIL import Image, ImageDraw, ImageFont


#load image
#number every hex by column
#eg. columns are numbered 01, 02, 03 etc.
#rows are numbered 01, 02
#so hexes should be named 00.00, 00.01, 04.12 etc.

def number_hexes():
    def switch(var):
        if var == True:
            return False
        elif var == False:
            return True
    # alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    columns = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO']
    file_path_in = r'C:\Users\felven\Desktop\Forbidden Lands Map_1_small.jpg'
    file_path_out = r'C:\Users\felven\Desktop\hexes_numbered.jpg'
    img = Image.open(file_path_in)
    d = ImageDraw.Draw(img)


    counter_row = 0
    counter_col = 0
    is_it_even = True
    font = ImageFont.truetype(font=r'C:\Windows\Fonts\CALIBRI.TTF', size=14)
    x = 58.5

    for i in range(1, 42):
        is_it_even = switch(is_it_even)
        if is_it_even == False:
            for j in range(1, 26):
                # counter_row += 1
                counter = str(j) + '.' + columns[counter_col]
                d.text(xy=(x*i, 67.4*j), text=str(counter), fill='rgb(0,0,0)', font=font)
        elif is_it_even == True:
            for j in range(1, 26):
                # counter_row += 1
                counter = str(j) + '.' + columns[counter_col]
                d.text(xy=(x*i, 67.4*j+32), text=str(counter), fill='rgb(0,0,0)', font=font)
        counter_col += 1

    img.save(file_path_out)



if __name__ == "__main__":
    number_hexes()