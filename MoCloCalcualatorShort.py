#!/usr/bin/env python3.11.9
import tkinter as tk
from tkinter import filedialog
standard_stock_concentration = 100
standart_input_volume = 9
# Small program to read snapgene 6 files and the performs molar calculations
# By Max 

round_value = 3
def create_gui(data, title="Plasmid calculator"):
    label_update_reference = {}
    n = len(data)
    names = list(data.keys())
    lengths = list(data.values())
    root = tk.Tk()
    root.title(title)

    # Ratio label
    ratio_label = tk.Label(root, text="Plasmid:Insert ratio:")
    ratio_label.grid(row=0, column=0, sticky="w")
    ratio_plasmid = tk.Label(root, text="Plasmid:")
    ratio_plasmid.grid(row=1, column=0, sticky="w")
    ratio_insert = tk.Label(root, text="Insert:")
    ratio_insert.grid(row=2, column=0, sticky="w")
    
    # Ratio input
    plasmid_ratio_input = tk.Label(root, text=1, justify=tk.CENTER)
    plasmid_ratio_input.grid(row=1, column=1)
    insert_ratio_input = tk.Entry(root, justify=tk.CENTER)
    insert_ratio_input.grid(row=2, column=1)
    insert_ratio_input.insert(0, 1)
    
    # Total input volume
    tk.Label(root, text="Total input volume [µl]:").grid(row=0, column=n, sticky="e")
    total_volume_input = tk.Entry(root, justify=tk.CENTER)
    total_volume_input.grid(row=0, column=n+1)
    total_volume_input.insert(0, standart_input_volume)
    
    # Header labels for Backbone, Inserts, and Water
    tk.Label(root, text="Backbone").grid(row=3, column=1)
    for i in range(2, n+2):
        tk.Label(root, text=f"Insert {i-1}").grid(row=3, column=i)
    tk.Label(root, text="Water").grid(row=3, column=n+1)
    
    # Mass, fmol, stock concentration, and insert volume rows
    rows = ["Type", "Filename", "Length [bp]", "Mass [ng]", "fmol", "Stock concentration [ng/µl]", "Insert volume [µl]"]
    for row in range(len(rows)):
        index_label = tk.Label(root, text=rows[row])
        index_label.grid(row=3+row, column=0)
        
    # Filename
    for i in range(n):
        filename_label = tk.Label(root, text=names[i])
        filename_label.grid(row=4, column=i+1)

    # Length
    for i in range(n):
        length_label = tk.Label(root, text=lengths[i])
        length_label.grid(row=5, column=i+1)

    # Mass
    backbone_mass = tk.Entry(root, justify=tk.CENTER)
    backbone_mass.grid(row=6, column=1)
    backbone_mass.insert(0,50)
    mass_label_list = []
    for i in range(n-1):
        mass_label = tk.Label(root, text="calc ng")
        mass_label.grid(row=6, column=i+2)
        mass_label_list.append(mass_label)
    label_update_reference["mass_label_list"] = mass_label_list

    # fmol
    fmol_label_list = []
    for i in range(n):
        fmol_label = tk.Label(root, text="-")
        fmol_label.grid(row=7, column=i+1)
        fmol_label_list.append(fmol_label)
    label_update_reference["fmol_label_list"] = fmol_label_list

    # Stock concentration inputs
    concentration_inputs = []
    for i in range(n):
        entry = tk.Entry(root, justify=tk.CENTER)
        entry.grid(row=8, column=i+1)
        entry.insert(0, standard_stock_concentration) 
        concentration_inputs.append(entry)

    # Insert volume
    volume_label_list = []
    for i in range(n+1):
        volume_label = tk.Label(root, text="x ul")
        volume_label.grid(row=9, column=i+1)
        volume_label_list.append(volume_label)
    label_update_reference["volume_label_list"] = volume_label_list

    # Buttons
    new_button = tk.Button(root, text="Open new file", command=lambda: open_file(root)) 
    new_button.grid(row=1, column=2, rowspan=2, padx=5, pady=5)
    calculate_button = tk.Button(root, text="Calculate", command=lambda: calculate(label_update_reference, lengths=lengths,
                                                                                              insert_ratio = insert_ratio_input.get(),
                                                                                              backbone_mass = backbone_mass.get(),
                                                                                              input_volume = total_volume_input.get(), 
                                                                                              concentrations = [entry.get() for entry in concentration_inputs],
                                                                                              plasmid_ratio = 1)) 
    calculate_button.grid(row=1, column=3, rowspan=2, padx=5, pady=5)
    root.mainloop()

def calculate(label_update_reference, lengths, insert_ratio, backbone_mass, input_volume, concentrations, plasmid_ratio=1):
    # verify data
    try:
        temp = lengths
        lengths = [int(x) for x in temp]
        insert_ratio = float(insert_ratio)
        backbone_mass = float(backbone_mass)
        input_volume = float(input_volume)
        temp = concentrations
        concentrations = [float(x) for x in concentrations]
        plasmid_ratio = float(plasmid_ratio)
    except Exception as e:
        print("Check your input!")
        print(e)
    n = len(lengths)

    # Calculate molarity -> fmol_output
    # Formula from https://www.promega.de/en/resources/tools/biomath/
    # Added *1e3 tp get from pmol to fmol
    backbone_fmol = (backbone_mass*1e-3 / 660 * 10**6 / 1 * (1/lengths[0])) * 1e3
    fmol_list = [round(backbone_fmol,round_value)]
    for _ in range(n-1):
        fmol_list.append(round(backbone_fmol*insert_ratio, round_value))
    
    # Calculate mass -> ng_output
    # Ignore the given plasmid input 
    ng_output = []
    for i in range(1, n):
        ng_output.append(fmol_list[i]*(660*lengths[i])/1000000)    

    # Calculate insert volume -> volume_list
    volume_list = []
    ng_output.insert(0, backbone_mass)
    for i in range(n):
        volume_list.append(ng_output[i]/concentrations[i])
    water_amount = input_volume-sum(volume_list)
    volume_list.append(water_amount)
    if water_amount < 0:
        raise Exception("You do not have enough DNA to set up this reaction.\nCheck your input or get more DNA!")
    ng_output = ng_output[1:]

    # Update Labels
    for mass_index in range(len(label_update_reference["mass_label_list"])):
        label_update_reference["mass_label_list"][mass_index].config(text=round(ng_output[mass_index], round_value))
    for fmol_index in range(len(label_update_reference["fmol_label_list"])):
        label_update_reference["fmol_label_list"][fmol_index].config(text=round(fmol_list[fmol_index], round_value))
    for volume_index in range(len(label_update_reference["volume_label_list"])):
        label_update_reference["volume_label_list"][volume_index].config(text=round(volume_list[volume_index], round_value))    

def open_file(root):
    file_path = filedialog.askopenfilename(filetypes=[("SnapGene Files", "*.dna")])

    gui_input_data_from_function = from_filepath_to_history_data(file_path)
    root.destroy()
    create_gui(gui_input_data_from_function, title=file_path.split("/")[-1]+" Assembly Calculator")
    
def from_filepath_to_history_data(file_path):
    '''
    Modified code from existing library (SnapGeneFileReader) on github.
    # Original author: IsaacLuo
    # Source:
    # https://github.com/IsaacLuo/SnapGeneFileReader
    # Code modified
    '''
    import struct
    import xmltodict
    import html2text

    HTML_PARSER = html2text.HTML2Text()
    HTML_PARSER.ignore_emphasis = True
    HTML_PARSER.ignore_links = True
    HTML_PARSER.body_width = 0
    HTML_PARSER.single_line_break = True    

    def parse(val):
        '''parse html'''
        if isinstance(val, str):
            return (HTML_PARSER.handle(val)
                    .strip()
                    .replace("\n", " ")
                    .replace('"', "'"))
        else:
            return val

    def parse_dict(obj):
        """parse dict in the obj"""
        if isinstance(obj, dict):
            for key in obj:
                if isinstance(obj[key], str):
                    obj[key] = parse(obj[key])
                elif isinstance(obj[key], dict):
                    parse_dict(obj[key])
        return obj

    def snapgene_file_to_dict(filepath=None, fileobject=None):
        """
        # This function is also part of the original SnapGeneFileReader library
        Return a dictionnary containing the data from a ``*.dna`` file.

        Parameters
        ----------
        filepath
            Path to a .dna file created with SnapGene
        fileobject
            On object-like pointing to the data of a .dna file created with
            SnapGene

        """

        if filepath is not None:
            fileobject = open(filepath, 'rb')

        if fileobject.read(1) != b'\t':
            raise ValueError('Wrong format for a SnapGene file !')

        def unpack(size, mode):
            """unpack the fileobject"""
            return struct.unpack('>' + mode, fileobject.read(size))[0]

        # READ THE DOCUMENT PROPERTIES
        length = unpack(4, 'I')
        title = fileobject.read(8).decode('ascii')
        if length != 14 or title != 'SnapGene':
            raise ValueError('Wrong format for a SnapGene file !')

        data = dict(isDNA=unpack(2, 'H'),exportVersion=unpack(2, 'H'),importVersion=unpack(2, 'H'),features=[])

        while True:
            # READ THE WHOLE FILE, BLOCK BY BLOCK, UNTIL THE END
            next_byte = fileobject.read(1)

            if next_byte == b'':
                # END OF FILE
                break

            block_size = unpack(4, 'I')

            # HISTORY TREE 
            # Read the history tree block
            if ord(next_byte) == 7:
                block_content = fileobject.read(block_size).decode('utf-8')
                note_data_hist_tree = parse_dict(xmltodict.parse(block_content))
                # print(note_data_hist_tree)
                # Author Max D
                # data['notes'] = note_data['Notes'] # Actually not necessary for my application
    

            else:
                # WE IGNORE THE WHOLE BLOCK
                fileobject.read(block_size)
                pass
        fileobject.close()

        return note_data_hist_tree #data
    
    # Extract actual history elements
    history_raw = snapgene_file_to_dict(filepath=file_path)
    gui_input_data = {}
    for history_element in history_raw["HistoryTree"]["Node"]["Node"]:
        gui_input_data[history_element["@name"]] = history_element['@seqLen']
    return gui_input_data

root = tk.Tk()
root.title("SnapGene File Browser")
root.geometry('300x80')

open_button = tk.Button(root, text="Open SnapGene File", command=lambda: open_file(root))
open_button.pack(pady=20)

root.mainloop()