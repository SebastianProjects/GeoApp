import customtkinter as ctk
from customtkinter import filedialog
from LocationProcessor.Location_router import Location_router
from KDTree.Tester import Tester
from GUI.myMapWidget import MyMapWidget
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from LocationProcessor.Location import Land_Prop, Real_estate_prop
from typing import Union
import random
from MapShapes.Shapes.Shape import Rectangle
from MapShapes.ShapesFactory import TkinterMapShapeFactory

class GUI:
    def __init__(self):
        self.__win = ctk.CTk()

        ctk.set_default_color_theme("GUI/assets/yellow.json")
        self.__router = Location_router()

        self.__win.geometry("1040x640")
        self.__win.title("Location App")

        self.__win.title("Location App")
        self.__win.resizable(True, True)

        self.__win.grid_columnconfigure(0, weight=1)
        self.__win.grid_rowconfigure(0, weight=0)
        self.__win.grid_rowconfigure(1, weight=1)

        # MAIN FRAMES

        self.__upper_frame = ctk.CTkFrame(self.__win)
        self.__upper_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.__lower_frame = ctk.CTkFrame(self.__win)
        self.__lower_frame.grid(row=1, column=0, pady=5, padx=5, sticky="nsew")
        
        self.__label_coordinates = ctk.CTkLabel(self.__win, text="Move the mouse over the map to see coordinates.")
        self.__label_coordinates.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")

        self.__upper_frame.grid_columnconfigure(0, weight=0)
        self.__upper_frame.grid_columnconfigure(1, weight=1)
        # LEFT FRAME

        self.__upper_menu_hidden = True

        self.__upper_left_frame = ctk.CTkFrame(self.__upper_frame)
        self.__upper_left_frame.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")

        self.__upper_left_frame.rowconfigure(1, weight=1)
        self.__upper_right_frame = ctk.CTkFrame(self.__upper_frame)
        self.__upper_right_frame.grid(row=0, column=1, pady=5, padx=5, sticky="nsew")

        self.__upper_right_frame.rowconfigure(0, weight=1)
        self.__upper_right_frame.columnconfigure(1, weight=1)

        fig, self.__ax = plt.subplots()
        self.__graph_canvas = FigureCanvasTkAgg(fig, master=self.__upper_right_frame)

        self.__output_field = ctk.CTkTextbox(self.__upper_right_frame)
        self.__output_field.grid(
            row=0, column=0, columnspan=2, pady=5, padx=5, sticky="nsew"
        )
        self.__output_field.insert("1.0", "Output here!")
        self.__output_field.configure(state="disabled")

        self.__combobox_delete_locations = ctk.CTkComboBox(self.__upper_right_frame)
        self.__combobox_edit_locations = ctk.CTkComboBox(self.__upper_right_frame)
        self.__edit_location_prop : Union[Land_Prop, Real_estate_prop] = None

        # MENU - NAV BAR

        self.__nav_bar = ctk.CTkFrame(self.__upper_left_frame)
        self.__nav_bar.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")

        self.__menu_find_button = ctk.CTkButton(
            self.__nav_bar, text="Find", command=self.show_menu_find, width=100
        )
        self.__menu_find_button.grid(row=0, column=0, padx=5, pady=5)

        self.__menu_insert_button = ctk.CTkButton(
            self.__nav_bar, text="Insert", command=self.show_menu_insert, width=100
        )
        self.__menu_insert_button.grid(row=1, column=0, padx=5, pady=5)

        self.__menu_delete_button = ctk.CTkButton(
            self.__nav_bar, text="Delete", command=self.show_menu_delete, width=100
        )
        self.__menu_delete_button.grid(row=2, column=0, padx=5, pady=5)

        self.__menu_edit_button = ctk.CTkButton(
            self.__nav_bar, text="Edit", command=self.show_menu_edit, width=100
        )
        self.__menu_edit_button.grid(row=3, column=0, padx=5, pady=5)

        self.__menu_file_button = ctk.CTkButton(
            self.__nav_bar, text="File", command=self.show_menu_file, width=100
        )
        self.__menu_file_button.grid(row=4, column=0, padx=5, pady=5)

        self.__menu_test_button = ctk.CTkButton(
            self.__nav_bar, text="Test", command=self.show_menu_test, width=100
        )
        self.__menu_test_button.grid(row=5, column=0, padx=5, pady=5)

        self.__menu_perf_button = ctk.CTkButton(
            self.__nav_bar, text="Performance", command=self.show_menu_perf, width=100
        )
        self.__menu_perf_button.grid(row=6, column=0, padx=5, pady=5)

        self.__menu_about_button = ctk.CTkButton(
            self.__nav_bar, text="About", command=self.show_menu_about, width=100
        )
        self.__menu_about_button.grid(row=7, column=0, padx=5, pady=5)

        # FIND, DELETE, INSERT, EDIT

        self.__find_insert_delete_edit_menu_frame = ctk.CTkFrame(
            self.__upper_left_frame, width=480
        )
        self.__find_insert_delete_edit_menu_frame.grid(
            row=0, column=1, pady=5, padx=5, sticky="nsew"
        )

        self.__number_entry = ctk.CTkEntry(
            self.__find_insert_delete_edit_menu_frame, placeholder_text="Number"
        )

        self.__description_entry = ctk.CTkEntry(
            self.__find_insert_delete_edit_menu_frame, placeholder_text="Description"
        )

        self.__lat_entry1 = ctk.CTkEntry(
            self.__find_insert_delete_edit_menu_frame, placeholder_text="1 latitude"
        )
        self.__lat_entry1.grid(row=3, column=0, padx=5, pady=5)

        self.__lat_direction_entry1 = ctk.CTkEntry(
            self.__find_insert_delete_edit_menu_frame,
            placeholder_text="1 latitude direction",
        )
        self.__lat_direction_entry1.grid(row=3, column=1, padx=5, pady=5)

        self.__lon_entry1 = ctk.CTkEntry(
            self.__find_insert_delete_edit_menu_frame, placeholder_text="1 longitude"
        )
        self.__lon_entry1.grid(row=4, column=0, padx=5, pady=5)

        self.__lon_direction_entry1 = ctk.CTkEntry(
            self.__find_insert_delete_edit_menu_frame,
            placeholder_text="1 longitude direction",
        )
        self.__lon_direction_entry1.grid(row=4, column=1, padx=5, pady=5)

        self.__lat_entry2 = ctk.CTkEntry(
            self.__find_insert_delete_edit_menu_frame, placeholder_text="2 latitude"
        )

        self.__lat_direction_entry2 = ctk.CTkEntry(
            self.__find_insert_delete_edit_menu_frame,
            placeholder_text="2 latitude direction",
        )

        self.__lon_entry2 = ctk.CTkEntry(
            self.__find_insert_delete_edit_menu_frame, placeholder_text="2 longitude"
        )

        self.__lon_direction_entry2 = ctk.CTkEntry(
            self.__find_insert_delete_edit_menu_frame,
            placeholder_text="2 longitude direction",
        )

        self.__land_checkbox = ctk.CTkCheckBox(
            self.__find_insert_delete_edit_menu_frame, text="Land"
        )
        self.__land_checkbox.grid(row=7, column=0, padx=5, pady=5)

        self.__real_estate_checkbox = ctk.CTkCheckBox(
            self.__find_insert_delete_edit_menu_frame, text="Real estate"
        )
        self.__real_estate_checkbox.grid(row=7, column=1, padx=5, pady=5)

        self.__find_button = ctk.CTkButton(
            self.__find_insert_delete_edit_menu_frame,
            text="Find",
            command=self.find_location
        )
        self.__find_all_button = ctk.CTkButton(
            self.__find_insert_delete_edit_menu_frame,
            text="Find all",
            command=self.find_all
        )
        self.__delete_button = ctk.CTkButton(
            self.__find_insert_delete_edit_menu_frame,
            text="Delete",
            command=self.find_and_delete_locations
        )
        self.__delete_all_button = ctk.CTkButton(
            self.__find_insert_delete_edit_menu_frame,
            text="Delete all",
            command=self.__router.delete_all_locations
        )
        self.__insert_button = ctk.CTkButton(
            self.__find_insert_delete_edit_menu_frame,
            text="Insert",
            command=self.insert_location
        )
        self.__edit_button = ctk.CTkButton(
            self.__find_insert_delete_edit_menu_frame,
            text="Edit",
            command=self.edit_and_find_location
        )

        # FILE

        self.__file_menu_frame = ctk.CTkFrame(self.__upper_left_frame, width=480)
        self.__file_menu_frame.grid(row=0, column=1, pady=5, padx=5, sticky="nsew")

        self.__upload_button = ctk.CTkButton(
            self.__file_menu_frame, text="Upload", command=self.upload_data
        )
        self.__upload_button.grid(row=0, column=0, padx=5, pady=5)

        self.__save_button = ctk.CTkButton(
            self.__file_menu_frame, text="Save", command=self.save_data
        )
        self.__save_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.__generate_data_count = ctk.CTkEntry(
            self.__file_menu_frame, placeholder_text="Number of data"
        )
        self.__generate_data_count.grid(row=2, column=0, padx=5, pady=5)
        
        self.__generate_prob = ctk.CTkEntry(
            self.__file_menu_frame, placeholder_text="Probability"
        )
        self.__generate_prob.grid(row=3, column=0, padx=5, pady=5)
        
        self.__generate_data_button = ctk.CTkButton(
            self.__file_menu_frame, text="Generate data", command=self.generate_data
        )
        self.__generate_data_button.grid(row=4, column=0, padx=5, pady=5)

        # TEST, PERF

        self.__test_perf_menu_frame = ctk.CTkFrame(self.__upper_left_frame, width=480)
        self.__test_perf_menu_frame.grid(row=0, column=1, pady=5, padx=5, sticky="nsew")

        self.__test_insert_checkbox = ctk.CTkCheckBox(
            self.__test_perf_menu_frame, text="Test Insert"
        )
        self.__test_insert_checkbox.grid(row=0, column=0, padx=5, pady=5)

        self.__test_find_checkbox = ctk.CTkCheckBox(
            self.__test_perf_menu_frame, text="Test Find"
        )
        self.__test_find_checkbox.grid(row=0, column=1, padx=5, pady=5)

        self.__test_delete_checkbox = ctk.CTkCheckBox(
            self.__test_perf_menu_frame, text="Test Delete"
        )
        self.__test_delete_checkbox.grid(row=1, column=0, padx=5, pady=5)

        self.__test_all_checkbox = ctk.CTkCheckBox(
            self.__test_perf_menu_frame, text="Test All"
        )
        self.__test_all_checkbox.grid(row=1, column=1, padx=5, pady=5)

        self.__data_size_entry = ctk.CTkEntry(
            self.__test_perf_menu_frame, placeholder_text="Data size"
        )
        self.__data_size_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.__test_button = ctk.CTkButton(
            self.__test_perf_menu_frame, text="Test", command=self.test
        )
        self.__step_count_entry = ctk.CTkEntry(
            self.__test_perf_menu_frame, placeholder_text="Step count"
        )
        self.__replication_count_entry = ctk.CTkEntry(
            self.__test_perf_menu_frame, placeholder_text="Replication count"
        )
        self.__perf_button = ctk.CTkButton(
            self.__test_perf_menu_frame, text="Perf", command=self.perf
        )

        # ABOUT

        self.__about_menu_frame = ctk.CTkFrame(self.__upper_left_frame, width=480)
        self.__about_menu_frame.grid(row=0, column=1, pady=5, padx=5, sticky="nsew")

        self.__about_label = ctk.CTkLabel(
            self.__about_menu_frame, text="This application was made by Sebastian"
        )
        self.__about_label.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")

        # RIGHT FRAME

        self.__upper_frame.grid_forget()

        self.__mmw = MyMapWidget(
            self.__lower_frame, self.hide_show_left_menu, width=1920, height=1024
        )
        self.__mmw.grid(row=0, column=0, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.__map_shape_factory = TkinterMapShapeFactory(self.__mmw)

        self.__win.after(10, self.update_label_coordinates)
        self.__win.mainloop()

    def hide_show_left_menu(self):
        if self.__upper_menu_hidden:
            self.__upper_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.__upper_menu_hidden = False
        else:
            self.__upper_frame.grid_forget()
            self.__upper_menu_hidden = True

    def show_menu_find(self):
        self.hide_all_menus()
        self.set_output(
            "Info >> Please provide one of the coordinates above and choose one of the checkboxes or both!"
        )
        self.__find_insert_delete_edit_menu_frame.grid(
            row=0, column=1, pady=5, padx=5, sticky="nsew"
        )
        self.__lat_entry2.grid(row=5, column=0, padx=5, pady=5)
        self.__lat_direction_entry2.grid(row=5, column=1, padx=5, pady=5)
        self.__lon_entry2.grid(row=6, column=0, padx=5, pady=5)
        self.__lon_direction_entry2.grid(row=6, column=1, padx=5, pady=5)
        self.__find_button.grid(
            row=8, column=0, columnspan=2, pady=10, padx=5, sticky="ew"
        )
        self.__find_all_button.grid(
            row=9, column=0, columnspan=2, pady=10, padx=5, sticky="ew"
        )

    def show_menu_insert(self):
        self.hide_all_menus()
        self.set_output(
            "Info >> Please provide information and coordinates above and choose one of the checkboxes!"
        )
        self.__find_insert_delete_edit_menu_frame.grid(
            row=0, column=1, pady=5, padx=5, sticky="nsew"
        )
        self.__number_entry.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.__description_entry.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.__lat_entry2.grid(row=5, column=0, padx=5, pady=5)
        self.__lat_direction_entry2.grid(row=5, column=1, padx=5, pady=5)
        self.__lon_entry2.grid(row=6, column=0, padx=5, pady=5)
        self.__lon_direction_entry2.grid(row=6, column=1, padx=5, pady=5)
        self.__insert_button.grid(
            row=8, column=0, columnspan=2, pady=10, padx=5, sticky="ew"
        )

    def show_menu_delete(self):
        self.hide_all_menus()
        self.set_output(
            "Info >> Please provide coordinates above and choose one of the checkboxes!"
        )
        self.__find_insert_delete_edit_menu_frame.grid(
            row=0, column=1, pady=5, padx=5, sticky="nsew"
        )
        self.__delete_button.grid(
            row=8, column=0, columnspan=2, pady=10, padx=5, sticky="ew"
        )
        self.__delete_all_button.grid(
            row=9, column=0, columnspan=2, pady=10, padx=5, sticky="ew"
        )
        
    def show_menu_edit(self):
        self.hide_all_menus()
        self.set_output("Info >> Please provide coordinates and choose one of the checkboxes or both!")
        self.__find_insert_delete_edit_menu_frame.grid(
            row=0, column=1, pady=5, padx=5, sticky="nsew"
        )
        self.__number_entry.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.__number_entry.configure(state="disabled")
        self.__description_entry.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.__description_entry.configure(state="disabled")
        self.__lat_entry2.grid(row=5, column=0, padx=5, pady=5)
        self.__lat_direction_entry2.grid(row=5, column=1, padx=5, pady=5)
        self.__lon_entry2.grid(row=6, column=0, padx=5, pady=5)
        self.__lon_direction_entry2.grid(row=6, column=1, padx=5, pady=5)
        self.__edit_button.grid(
            row=8, column=0, columnspan=2, pady=10, padx=5, sticky="ew"
        )

    def show_menu_file(self):
        self.hide_all_menus()
        self.set_output("Info >> Please choose csv file to upload or choose directory to save locations to!")
        self.__file_menu_frame.grid(row=0, column=1, pady=5, padx=5, sticky="nsew")

    def show_menu_test(self):
        self.hide_all_menus()
        self.set_output("Info >> Provide operation count and choose one of the options above!")
        self.__test_perf_menu_frame.grid(row=0, column=1, pady=5, padx=5, sticky="nsew")
        self.__test_button.grid(
            row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )

    def show_menu_perf(self):
        self.hide_all_menus()
        self.set_output("Info >> Provide info and choose one of the options above!")
        self.__test_perf_menu_frame.grid(row=0, column=1, pady=5, padx=5, sticky="nsew")
        self.__step_count_entry.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.__replication_count_entry.grid(
            row=4, column=0, columnspan=2, padx=5, pady=5
        )
        self.__perf_button.grid(
            row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )

    def show_menu_about(self):
        self.hide_all_menus()
        self.set_output(":)")
        self.__about_menu_frame.grid(row=0, column=1, pady=5, padx=5, sticky="nsew")

    def hide_all_menus(self):
        self.__test_perf_menu_frame.grid_forget()
        self.__find_insert_delete_edit_menu_frame.grid_forget()
        self.__file_menu_frame.grid_forget()
        self.__about_menu_frame.grid_forget()

        self.__find_button.grid_forget()
        self.__find_all_button.grid_forget()
        self.__delete_button.grid_forget()
        self.__delete_all_button.grid_forget()
        self.__insert_button.grid_forget()
        self.__edit_button.grid_forget()
        self.__edit_button.configure(command=self.edit_and_find_location)
        self.__number_entry.configure(state='normal')
        self.__description_entry.configure(state='normal')

        self.__description_entry.grid_forget()
        self.__number_entry.grid_forget()
        self.__lat_entry2.grid_forget()
        self.__lat_direction_entry2.grid_forget()
        self.__lon_entry2.grid_forget()
        self.__lon_direction_entry2.grid_forget()

        self.__step_count_entry.grid_forget()
        self.__replication_count_entry.grid_forget()
        self.__perf_button.grid_forget()
        self.__test_button.grid_forget()

    def set_output(self, text: str):
        self.hide_all_outputs()
        self.__output_field.grid(
            row=0, column=0, columnspan=2, pady=5, padx=5, sticky="nsew"
        )
        self.__output_field.configure(state="normal")
        self.__output_field.delete("1.0", ctk.END)
        self.__output_field.insert("1.0", text)
        self.__output_field.configure(state="disabled")

    def hide_all_outputs(self):
        self.__output_field.grid_forget()
        self.__graph_canvas.get_tk_widget().grid_forget()
        self.__combobox_delete_locations.grid_forget()
        self.__combobox_edit_locations.grid_forget()

    def insert_location(self):
        if (
            self.__number_entry.get()
            and self.__description_entry.get()
            and self.__lat_entry1.get()
            and self.__lat_direction_entry1.get()
            and self.__lon_entry1.get()
            and self.__lon_direction_entry1.get()
            and self.__lat_entry2.get()
            and self.__lat_direction_entry2.get()
            and self.__lon_entry2.get()
            and self.__lon_direction_entry2.get()
        ):

            location_type: str = ""

            if self.__land_checkbox.get() and self.__real_estate_checkbox.get():
                self.set_output("Error >> Please choose only one of the options above!")
                return
            elif self.__land_checkbox.get():
                location_type = "l"
            elif self.__real_estate_checkbox.get():
                location_type = "re"
            else:
                self.set_output("Error >> Please choose one of the options above!")
                return

            self.__router.insert_location(
                location_type=location_type,
                number=int(self.__number_entry.get()),
                description=self.__description_entry.get(),
                left_upper_lat_position=float(self.__lat_entry1.get()),
                left_upper_lat_direction=self.__lat_direction_entry1.get(),
                left_upper_lon_position=float(self.__lon_entry1.get()),
                left_upper_lon_direction=self.__lon_direction_entry1.get(),
                right_lower_lat_position=float(self.__lat_entry2.get()),
                right_lower_lat_direction=self.__lat_direction_entry2.get(),
                right_lower_lon_position=float(self.__lon_entry2.get()),
                right_lower_lon_direction=self.__lon_direction_entry2.get(),
            )

            self.set_output(f"Info >> Location {self.__number_entry.get()} inserted!")

        else:
            self.set_output("Error >> Please provide all coordinates above!")

    def find_location(self):
        self.hide_all_outputs()
        self.__mmw.delete_all_objects()
        
        location_props: list[Union[Land_Prop, Real_estate_prop]] = []
        
        if (
            self.__lat_entry1.get()
            and self.__lat_direction_entry1.get()
            and self.__lon_entry1.get()
            and self.__lon_direction_entry1.get()
            and self.__lat_entry2.get()
            and self.__lat_direction_entry2.get()
            and self.__lon_entry2.get()
            and self.__lon_direction_entry2.get()
        ):
            if self.__land_checkbox.get() and self.__real_estate_checkbox.get():
                location_props = self.__router.find_location(
                    "b",
                    lat_position1=float(self.__lat_entry1.get()),
                    lat_direction1=self.__lat_direction_entry1.get(),
                    lon_position1=float(self.__lon_entry1.get()),
                    lon_direction1=self.__lon_direction_entry1.get(),
                    lat_position2=float(self.__lat_entry2.get()),
                    lat_direction2=self.__lat_direction_entry2.get(),
                    lon_position2=float(self.__lon_entry2.get()),
                    lon_direction2=self.__lon_direction_entry2.get(),
                )
            else:
                self.set_output(
                    "Error >> For fiding between two nodes choose both options above"
                )
                return
        elif (
            self.__lat_entry1.get()
            and self.__lat_direction_entry1.get()
            and self.__lon_entry1.get()
            and self.__lon_direction_entry1.get()
        ):

            location_type: str = ""

            if self.__land_checkbox.get() and self.__real_estate_checkbox.get():
                self.set_output(
                    "Error >> Please choose only one of the options above or provide both coordinates!"
                )
                return
            elif self.__land_checkbox.get():
                location_type = "l"
            elif self.__real_estate_checkbox.get():
                location_type = "re"
            else:
                self.set_output("Error >> Please choose one of the options above!")
                return

            location_props = self.__router.find_location(
                location_type=location_type,
                lat_position1=float(self.__lat_entry1.get()),
                lat_direction1=self.__lat_direction_entry1.get(),
                lon_position1=float(self.__lon_entry1.get()),
                lon_direction1=self.__lon_direction_entry1.get(),
            )

        elif (
            self.__lat_entry2.get()
            and self.__lat_direction_entry2.get()
            and self.__lon_entry2.get()
            and self.__lon_direction_entry2.get()
        ):
            location_type: str = ""

            if self.__land_checkbox.get():
                location_type = "l"
            elif self.__real_estate_checkbox.get():
                location_type = "re"
            else:
                self.set_output("Error >> Please choose one of the options above!")
                return

            location_props = self.__router.find_location(
                location_type=location_type,
                lat_position2=float(self.__lat_entry2.get()),
                lat_direction2=self.__lat_direction_entry2.get(),
                lon_position2=float(self.__lon_entry2.get()),
                lon_direction2=self.__lon_direction_entry2.get(),
            )

        else:
            self.set_output("Error >> Please provide coordinates above!")
            return

        if location_props:
            locations_str = ""
            for location_prop in location_props:
                colliding_locations = []
                if isinstance(location_prop, Land_Prop):
                    colliding_locations = location_prop.get_real_estate_list()
                elif isinstance(location_prop, Real_estate_prop):
                    colliding_locations = location_prop.get_land_list()

                colliding_locations_str = "\n"

                for colliding_location in colliding_locations:
                    colliding_locations_str += (
                        f"\t{colliding_location.get_full_decsription()}\n"
                    )
                    
                    position1 = colliding_location.get_positions()[0].get_position()
                    position2 = colliding_location.get_positions()[1].get_position()
                
                    """ self.__mmw.set_rectangle(
                        f'{position1[0]} {position1[1]}', f'{position2[0]} {position2[1]}', outline_color='red'
                    ) """

                locations_str += (
                    f"{location_prop.get_full_decsription()}{colliding_locations_str}\n"
                )
                
                position1 = location_prop.get_positions()[0].get_position()
                position2 = location_prop.get_positions()[1].get_position()
                
                
                """ self.__mmw.set_rectangle(
                    f'{position1[0]} {position1[1]}', f'{position2[0]} {position2[1]}'
                ) """
                self.__map_shape_factory.create_rectangle(
                    position1, position2
                )
            self.set_output(f"Info >> Locations found\n\n{locations_str}")

        else:
            self.set_output("Info >> Location was not found!")
            return

    def find_all(self):
        self.hide_all_outputs()
        self.__mmw.delete_all_objects()
        location_props = self.__router.get_all_locations()
        if location_props:
            locations_str = ""
            for location_prop in location_props:
                colliding_locations = []
                if isinstance(location_prop, Land_Prop):
                    colliding_locations = location_prop.get_real_estate_list()
                elif isinstance(location_prop, Real_estate_prop):
                    colliding_locations = location_prop.get_land_list()

                colliding_locations_str = "\n"

                for colliding_location in colliding_locations:
                    colliding_locations_str += (
                        f"\t{colliding_location.get_full_decsription()}\n"
                    )
                    
                    position1 = colliding_location.get_positions()[0].get_position()
                    position2 = colliding_location.get_positions()[1].get_position()
                
                    """ self.__mmw.set_rectangle(
                        f'{position1[0]} {position1[1]}', f'{position2[0]} {position2[1]}', outline_color='red'
                    ) """

                locations_str += (
                    f"{location_prop.get_full_decsription()}{colliding_locations_str}\n"
                )
                
                position1 = location_prop.get_positions()[0].get_position()
                position2 = location_prop.get_positions()[1].get_position()
                
                """ self.__mmw.set_rectangle(
                    f'{position1[0]} {position1[1]}', f'{position2[0]} {position2[1]}'
                ) """
                self.__map_shape_factory.create_rectangle(
                    position1, position2
                )
            self.set_output(f"Info >> Locations found\n\n{locations_str}")
        
        else:
            self.set_output("Info >> No locations found!")
            

    def find_and_delete_locations(self):
        self.hide_all_outputs()
        if (
            self.__lat_entry1.get()
            and self.__lat_direction_entry1.get()
            and self.__lon_entry1.get()
            and self.__lon_direction_entry1.get()
        ):

            location_type: str = ""

            if self.__land_checkbox.get() and self.__real_estate_checkbox.get():
                self.set_output("Error >> Please choose only one of the options above!")
                return
            elif self.__land_checkbox.get():
                location_type = "l"
            elif self.__real_estate_checkbox.get():
                location_type = "re"
            else:
                self.set_output("Error >> Please choose one of the options above!")
                return

            location_props = self.__router.find_location(
                location_type=location_type,
                lat_position1=float(self.__lat_entry1.get()),
                lat_direction1=self.__lat_direction_entry1.get(),
                lon_position1=float(self.__lon_entry1.get()),
                lon_direction1=self.__lon_direction_entry1.get(),
            )

            if location_props:
                locations_str_list = []
                for location_prop in location_props:
                    locations_str_list.append(location_prop.get_full_decsription())
                self.__combobox_delete_locations.configure(
                    values=locations_str_list,
                    command=lambda event: self.on_combobox_delete_select(
                        event, location_type, location_props
                    ),
                )
                self.__combobox_delete_locations.grid(
                    row=0, column=0, columnspan=2, padx=5, pady=5, sticky="new"
                )

            else:
                self.set_output("Info >> Land was not found!")
        else:
            self.set_output("Error >> Please provide coordinates above!")

    def on_combobox_delete_select(self, event, type: str, props: list):
        for prop in props:
            if event == prop.get_full_decsription():
                self.__router.delete_location(location_type=type, prop=prop)

    def edit_and_find_location(self):
        self.hide_all_outputs()
        location_props: list[Union[Land_Prop, Real_estate_prop]] = []
        if (
            self.__lat_entry1.get()
            and self.__lat_direction_entry1.get()
            and self.__lon_entry1.get()
            and self.__lon_direction_entry1.get()
            and self.__lat_entry2.get()
            and self.__lat_direction_entry2.get()
            and self.__lon_entry2.get()
            and self.__lon_direction_entry2.get()
        ):
            if self.__land_checkbox.get() and self.__real_estate_checkbox.get():
                location_props = self.__router.find_location(
                    "b",
                    lat_position1=float(self.__lat_entry1.get()),
                    lat_direction1=self.__lat_direction_entry1.get(),
                    lon_position1=float(self.__lon_entry1.get()),
                    lon_direction1=self.__lon_direction_entry1.get(),
                    lat_position2=float(self.__lat_entry2.get()),
                    lat_direction2=self.__lat_direction_entry2.get(),
                    lon_position2=float(self.__lon_entry2.get()),
                    lon_direction2=self.__lon_direction_entry2.get(),
                )
            else:
                self.set_output(
                    "Error >> For fiding between two nodes choose both options above"
                )
                return
        elif (
            self.__lat_entry1.get()
            and self.__lat_direction_entry1.get()
            and self.__lon_entry1.get()
            and self.__lon_direction_entry1.get()
        ):

            location_type: str = ""

            if self.__land_checkbox.get() and self.__real_estate_checkbox.get():
                self.set_output(
                    "Error >> Please choose only one of the options above or provide both coordinates!"
                )
                return
            elif self.__land_checkbox.get():
                location_type = "l"
            elif self.__real_estate_checkbox.get():
                location_type = "re"
            else:
                self.set_output("Error >> Please choose one of the options above!")
                return

            location_props = self.__router.find_location(
                location_type=location_type,
                lat_position1=float(self.__lat_entry1.get()),
                lat_direction1=self.__lat_direction_entry1.get(),
                lon_position1=float(self.__lon_entry1.get()),
                lon_direction1=self.__lon_direction_entry1.get(),
            )

        elif (
            self.__lat_entry2.get()
            and self.__lat_direction_entry2.get()
            and self.__lon_entry2.get()
            and self.__lon_direction_entry2.get()
        ):
            location_type: str = ""

            if self.__land_checkbox.get():
                location_type = "l"
            elif self.__real_estate_checkbox.get():
                location_type = "re"
            else:
                self.set_output("Error >> Please choose one of the options above!")
                return

            location_props = self.__router.find_location(
                location_type=location_type,
                lat_position2=float(self.__lat_entry2.get()),
                lat_direction2=self.__lat_direction_entry2.get(),
                lon_position2=float(self.__lon_entry2.get()),
                lon_direction2=self.__lon_direction_entry2.get(),
            )
        
        if location_props:
            print('here')
            locations_str_list = []
            for location_prop in location_props:
                locations_str_list.append(location_prop.get_full_decsription())
            self.__combobox_edit_locations.configure(
                values=locations_str_list,
                command=lambda event: self.on_combobox_edit_select(
                    event, location_type, location_props
                ),
            )
            self.__combobox_edit_locations.grid(
                row=0, column=0, columnspan=2, padx=5, pady=5, sticky="new"
            )

        else:
            self.set_output("Error >> Please provide coordinates above!")
            return

    def on_combobox_edit_select(self, event, type: str, props: list[Union[Land_Prop, Real_estate_prop]]):
        for prop in props:
            if event == prop.get_full_decsription():
                self.__number_entry.configure(state="normal")
                self.__number_entry.delete(0, ctk.END)
                if isinstance(prop, Land_Prop):
                    self.__number_entry.insert(0, prop.get_land_number())
                else:
                    self.__number_entry.insert(0, prop.get_real_estate_number())
                self.__description_entry.configure(state="normal")
                self.__description_entry.delete(0, ctk.END)
                self.__description_entry.insert(0, prop.get_description())
                
                self.__lat_entry1.delete(0, ctk.END)
                self.__lat_entry1.insert(0, prop.get_positions()[0].get_lat_position())
                self.__lat_direction_entry1.delete(0, ctk.END)
                self.__lat_direction_entry1.insert(0, prop.get_positions()[0].get_lat_direction())
                self.__lon_entry1.delete(0, ctk.END)
                self.__lon_entry1.insert(0, prop.get_positions()[0].get_lon_position())
                self.__lon_direction_entry1.delete(0, ctk.END)
                self.__lon_direction_entry1.insert(0, prop.get_positions()[0].get_lon_direction())
                
                self.__lat_entry2.delete(0, ctk.END)
                self.__lat_entry2.insert(0, prop.get_positions()[1].get_lat_position())
                self.__lat_direction_entry2.delete(0, ctk.END)
                self.__lat_direction_entry2.insert(0, prop.get_positions()[1].get_lat_direction())
                self.__lon_entry2.delete(0, ctk.END)
                self.__lon_entry2.insert(0, prop.get_positions()[1].get_lon_position())
                self.__lon_direction_entry2.delete(0, ctk.END)
                self.__lon_direction_entry2.insert(0, prop.get_positions()[1].get_lon_direction())
                
                self.__edit_location_prop = prop
                self.__edit_button.configure(command=self.edit_location)

    def edit_location(self):
        location_type = ''
        if isinstance(self.__edit_location_prop, Land_Prop):
            location_type = 'l'
        else:
            location_type = 'r'
        self.__router.edit_location(location_type=location_type,
                                    prev_prop=self.__edit_location_prop,
                                    number=int(self.__number_entry.get()),
                                    description=self.__description_entry.get(),
                                    left_upper_lat_position=float(self.__lat_entry1.get()),
                                    left_upper_lat_direction=self.__lat_direction_entry1.get(),
                                    left_upper_lon_position=float(self.__lon_entry1.get()),
                                    left_upper_lon_direction=self.__lon_direction_entry1.get(),
                                    right_lower_lat_position=float(self.__lat_entry2.get()),
                                    right_lower_lat_direction=self.__lat_direction_entry2.get(),
                                    right_lower_lon_position=float(self.__lon_entry2.get()),
                                    right_lower_lon_direction=self.__lon_direction_entry2.get())
        self.set_output('Info >> Location edited successfully!')
        
    def test(self):
        tester = Tester()
        
        # TESTING INSERT
        if self.__test_all_checkbox.get() and self.__data_size_entry.get():
            test = tester.all(operation_count=int(self.__data_size_entry.get()))
            self.set_output(test)
            
        elif self.__test_insert_checkbox.get() and self.__data_size_entry.get():
            test = tester.insert(operation_count=int(self.__data_size_entry.get()))
            self.set_output(test)
            
        elif self.__test_find_checkbox.get() and self.__data_size_entry.get():
            test = tester.find(operation_count=int(self.__data_size_entry.get()))
            self.set_output(test)
            
        elif self.__test_delete_checkbox.get() and self.__data_size_entry.get():
            test = tester.delete(operation_count=int(self.__data_size_entry.get()))
            self.set_output(test)
        else:
            self.set_output('Error >> Please provide operation count and choose one of the options above!')

    def perf(self):
        tester = Tester()
        self.hide_all_outputs()

        # TESTING INSERT PERFORMANCE
        if (
            self.__test_insert_checkbox.get()
            and self.__data_size_entry.get()
            and self.__step_count_entry.get()
            and self.__replication_count_entry.get()
        ):
            data_count_list, average_time_list = tester.insert_for_performance(
                replication_count=int(self.__replication_count_entry.get()),
                step_size=int(self.__data_size_entry.get()),
                step_count=int(self.__step_count_entry.get()),
            )

            fig, self.__ax = plt.subplots()
            self.__graph_canvas = FigureCanvasTkAgg(fig, master=self.__upper_right_frame)

            self.__ax.plot(data_count_list, average_time_list, marker="o", color="b")
            self.__ax.set_xlabel("Data Count")
            self.__ax.set_ylabel("Average Time")
            self.__ax.set_title("Performance Graph")

            self.__graph_canvas.draw()
            self.__graph_canvas.get_tk_widget().grid(
                row=0, column=0, pady=5, padx=5, sticky="nsew"
            )
            
        elif (
            self.__test_find_checkbox.get()
            and self.__data_size_entry.get()
            and self.__step_count_entry.get()
            and self.__replication_count_entry.get()
        ):
            self.set_output('Not yet implemented')
            
        elif (
            self.__test_delete_checkbox.get()
            and self.__data_size_entry.get()
            and self.__step_count_entry.get()
            and self.__replication_count_entry.get()
        ):
            self.set_output('Not yet implemented')
        
        elif (
            self.__test_all_checkbox.get()
            and self.__data_size_entry.get()
            and self.__step_count_entry.get()
            and self.__replication_count_entry.get()
        ):
            self.set_output('Not yet implemented')
        
        else:
            self.set_output("Error >> Please provide data size, step count and replication count and choose one of the options above!")
            

    def upload_data(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        
        try:
            self.__router.load_locations_from_csv(filename=filename)
            self.set_output("Info >> Data uploaded!")
            
        except FileNotFoundError:
            self.set_output("Error >> File not found!")

    def save_data(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
        )
        
        try:
            self.__router.save_locations_to_csv(filename=filename)
            self.set_output("Info >> Data Saved!")
            
        except FileNotFoundError:
            self.set_output("Error >> File not found!")
            
    def generate_data(self):
        self.__router.generate_locations(int(self.__generate_data_count.get()), prob_of_colliding=float(self.__generate_prob.get()))
        self.set_output("Info >> Data generated!")
        
    def update_label_coordinates(self):
        latitude, longitude = self.__mmw.get_mouse_coordinates()
        self.__label_coordinates.configure(text = f"Latitude: {latitude:.7f}, Longitude: {longitude:.7f}")
        self.__win.after(10, self.update_label_coordinates)
