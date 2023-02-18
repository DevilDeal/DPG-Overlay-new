import dearpygui.dearpygui as dpg
from overlay_class import *
from overlay_class import point,rectangle,del_draw,points_tags,drag_window,init_overlay,window_units,window_create,delete_window,drag_exclude,change_exclude,delete_exclude,change_window
import threading
import sys

# points tags is the storage of all points/rects added
# window_units is the window storage that make the window clickable
# u can acces it with this variable points_tag if u want to do smth manually
# constants

title = "example programm"

#thread drag window/draws
def drag_window_threaded():
    threading.Thread(target=drag_window,args=
                    (window_units,  # window list
                    0.001,          # sleep value
                    True,           # prio_system check for bugfixes should always be true
                    True,           # bufix for window resize when drawing is above it is not necessary but wanted
                    False,          # bugfix for item exclusion when drawing is above 
                    True,           # autodetect system for exclusions
                    
                    ),daemon=True).start() 
def close_app():   
    sys.exit()

def overlay():
    dpg.create_context()
    
    dpg.create_viewport(title=title, decorated=False,clear_color=[0.0,0.0,0.0,0.0],always_on_top=True)
    dpg.set_viewport_always_top(True)
    dpg.setup_dearpygui()
    
    with dpg.window(label="Example Window",tag="Example Window",pos=(111,111),no_move=True,no_resize=True,on_close=close_app):
        dpg.add_text("Hello, world")
        window_create("Example Window",no_move=True)     #whenever u create a window and want to make it clickable call this
        #delete_window("Example Window")     # u can make a window not clickable with this function if u need it or when u del a window u should do this 
        
    with dpg.window(label="Example Window2",tag="Example Window2",pos=(222,222),no_move=True):
        dpg.add_text("Hello, world")
        window_create("Example Window2")    #whenever u create a window and want to make it clickable call this
        #change_window("Example Window2",no_move=False)   #u can change no_move attribute with this function  
        with dpg.child_window(parent="Example Window2"):
            dpg.add_collapsing_header(tag="header")
            #drag_exclude("header")                         #exclude header so window will not be draged when item is clicked
            change_exclude("header",True)                  #change the exclusion
            dpg.add_slider_float(tag="slider")
            #drag_exclude("slider") 
    with dpg.handler_registry(tag="handler"):
        #drag_window unthreaded == bugs # drag_window_threaded solves
        dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Left,callback=drag_window_threaded)

    with dpg.viewport_drawlist(tag="drawlist"):
            pass
    
    dpg.show_viewport()
    dpg.toggle_viewport_fullscreen()
    #dpg.maximize_viewport()
    #init the overlay here before u render
    init_overlay(title=title)

    #########example point#########
    dpg.draw_text(parent="drawlist",pos=(500,500),tag="hi",color=(255,255,0),text="hi",size=50)         #draw a text
    point(name="hi",pos=(500,500),tag="hi",width=50,heigth=50)                                          #init the drawing       / make it clickable and moveable
    dpg.draw_rectangle(parent="drawlist",pmin=(666,666),pmax= (1111,1111),tag="hi2",color=(255,0,0))    #draw a rect
    rectangle(name="hi2",pmin=(666,666),pmax= (1111,1111),tag="hi2",width=20,heigth=20)                 #width height is clickable area                     #init the rect drawing  / make it clickable and moveable
                                                                                        
    dpg.draw_text(parent="drawlist",pos=(555,555),tag="hii",color=(255,255,0),text="hii",size=50)
    point(name="hii",pos=(555,555),tag="hii",width=75,heigth=50)                                        #clickable area (width = per char ~size/2, height = per line ~size)
    dpg.delete_item("hii")                                                                              #delete dpg drawing
    del_draw("hii")                                                                                     #delete item            / can pass name or tag or filter for a coordinate(first item with the coordinate will be deleted)
    #########example point#########
    
    while dpg.is_dearpygui_running():
        #make windows and draws added clickable
        make_clickable(window_units=window_units)
        
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

if __name__ == "__main__":
    threading.Thread(target=overlay).start()

