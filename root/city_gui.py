try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import json
  
class CityGUI(tk.Tk):  
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        
        self.grid()
        self.top_frame = tk.Frame(parent)
        self.top_frame.grid(column = 0, row = 0, sticky = "EW", 
                            padx = 5, pady = 5, columnspan = 2)
        self.city_label = tk.Label(self.top_frame, text = 'City:')
        self.city_label.grid(row = 0, sticky = "EW")
        self.my_lb = tk.Listbox(self.top_frame, width = 35, height = 3)
        self.my_lb.grid(row = 1, column = 0)
        self.lb_scrollbar = tk.Scrollbar(parent, orient = "vertical", 
                                         command = self.my_lb.yview)
        self.lb_scrollbar.grid(row=  0, column = 2, sticky = 'NS')
        self.my_lb.configure(yscrollcommand = self.lb_scrollbar.set)
        self.my_lb.bind('<<ListboxSelect>>', self.on_select)  
        
        self.ordered_cities = self.parse_file()
        for j in range(len(self.ordered_cities)):
            self.my_lb.insert(tk.END, self.ordered_cities[j])
 
        self.left_frame = tk.Frame(parent)
        self.left_frame.grid(row = 1, column = 0, sticky = "WS", 
                             padx = 5, pady = 5)
        self.county_label = tk.Label(self.left_frame,text = 'County:')
        self.county_label.grid(row = 0, column = 0, sticky = "W")
        self.latitude_label = tk.Label(self.left_frame,text = 'Latitude:')
        self.latitude_label.grid(row = 1, column = 0, sticky = "W")
        self.longitude_label = tk.Label(self.left_frame,text = 'Longitude:')
        self.longitude_label.grid(row = 2, column = 0, sticky = "W")

        self.right_frame = tk.Frame(parent)
        self.right_frame.grid(row = 1, column = 1, sticky = "ES", 
                              padx = 5, pady = 5)
        self.county_var = tk.StringVar()
        self.lat_var = tk.StringVar()
        self.long_var = tk.StringVar()
        self.county_var_label = tk.Label(self.right_frame, 
                                         textvariable = self.county_var)
        self.county_var_label.grid(row = 0, column = 1, sticky = "E")
        self.lat_var_label = tk.Label(self.right_frame, 
                                      textvariable = self.lat_var)
        self.lat_var_label.grid(row = 1, column = 1, sticky = "E")
        self.long_var_label = tk.Label(self.right_frame, 
                                       textvariable = self.long_var)
        self.long_var_label.grid(row = 2, column = 1, sticky = "E")

    def on_select(self, evt):
            w = evt.widget
            index = int(w.curselection()[0])
            city = w.get(index)
            city_tuple = next(item for item in self.data if item['name'] == city)
            self.county_var.set(city_tuple['county_name'])
            self.lat_var.set(city_tuple['primary_latitude'])
            self.long_var.set(city_tuple['primary_longitude'])
        
    def parse_file(self):        
        self.city_list = [] 
        with open('ca.json') as data_file:
            self.data = json.load(data_file)       
            for i in range(len(self.data)):
                if self.data[i]['feat_class'] == 'Populated Place': 
                    self.city_list.append(self.data[i]['name'])  
        self.city_set = list(set(self.city_list))
        self.city_set.sort()
        return self.city_set
    
if __name__ == "__main__":
    app = CityGUI(None)
    app.title("City Coordinates")
    app.mainloop()

    
# {"county_name":"Los Angeles","description":null,"feat_class":"Populated Place","feature_id":"1525","fips_class":"C1","fips_county_cd":"37","full_county_name":"Los Angeles County","link_title":null,"url":"http:\/\/lacity.org\/","name":"Los Angeles","primary_latitude":"34.05","primary_longitude":"-118.24","state_abbreviation":"CA","state_name":"California"},
# {"county_name":"Los Angeles","description":null,"feat_class":"Populated Place","feature_id":"1525","fips_class":"C1","fips_county_cd":"37","full_county_name":"Los Angeles County","link_title":null,"url":"http:\/\/business.lacity.org\/","name":"Los Angeles","primary_latitude":"34.05","primary_longitude":"-118.24","state_abbreviation":"CA","state_name":"California"}