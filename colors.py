import os
import pandas as pd
import matplotlib.pyplot as plt

class Colors:

    def __init__(self, filename, columns):
        self.filename = filename #'colors.csv'
        self.columns = columns # ['name', 'hexcode']

    def createCsv(self):
        if os.path.exists(self.filename):
            pass
        else:
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.filename, index=False)
    
    def validateFilename(self):   
        if os.path.exists(self.filename):
            pass
        else:
            raise Exception("filename for color database does not exist: " + self.filename + ". File can be created through 'createCsv'")

    def createColors(self, colors):
        # color(s) must be dictionary with name and hex code. 
        # Eg. [{name: 'mexico', hex_code: '#B99E6B'}] 
        # OR [{name: 'mexico', hex_code: '#B99E6B'}, {name: 'earthyyellow', hex_code: '#CDBC94'}]
        
        self.validateFilename()
        new_rows = pd.DataFrame(colors)

        try:
            existing_df = pd.read_csv(self.filename)
        except FileNotFoundError:
            existing_df = pd.DataFrame(columns=new_rows.columns)

        combined_df = pd.concat([existing_df, new_rows], ignore_index=True)
        unique_df = combined_df.drop_duplicates(subset=['name', 'hex_code'], keep='last')
        unique_df.to_csv(self.filename, index=False)
        
    def getColors(self, name=None, hexCode=None, showColor=False):
        df = pd.read_csv(self.filename)
        if name and hexCode:
            row = df[(df['name'] == name) & (df['hex_code'] == hexCode)]
        elif name:
            row = df[df['name'] == name]
        elif hexCode:
            row = df[df['hex_code'] == hexCode]
        else:
            row = df
        
        if row.empty:
            raise ValueError(f"No row matching name: '{name}' or hex code: '{hexCode}' was found.")
        if showColor:
            for i in range(len(row)):
                hexCode = row.iloc[i]['hex_code']; name = row.iloc[i]['name']
                self.plotColor(hexCode=hexCode, name=name, save=True)
        return row
    
    def plotColor(self, hexCode, name=None, size=5, save=False):
        fig, ax = plt.subplots(figsize=(size, size))
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=hexCode))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')  # Fjern akser
        if name:
            print_text = name +': ' + hexCode
            save_text = name +'_' + hexCode
        else:
            print_text = hexCode
            save_text = hexCode
        ax.text(0.5, 0.5, print_text, ha='center', va='center', fontsize=12, color='black',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3'))
        if save:
            plt.savefig(save_text + '.png', dpi=300)
        plt.show()

# """
cl = Colors('colors.csv', ['name', 'hex_code'])
# cl.createColors(colors=[
#     {'name': 'soft_green', 'hex_code': '#abce9c'},
#     {'name': 'butter_yellow', 'hex_code': '#ffeaab'},
#     {'name': 'sophisticated_red', 'hex_code': '#a64b4b'}
#     ])

print(cl.getColors())

# cl.plotColor('#ffeaab', save=True)
# """