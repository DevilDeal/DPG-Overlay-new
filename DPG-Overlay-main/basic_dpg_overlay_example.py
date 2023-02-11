import dearpygui.dearpygui as dpg
from overlay_class import *
from overlay_class import point,rectangle,del_data,points_tags,drag_window,init_overlay
import threading
import time

# points tags is the storage of all points/rects added
# u can acces it with this variable points_tag if u want to do smth manually
# constants
window_units = [] #all window tags, insert at 0 to them when u make a new window that is clickable
title = "example programm"

#thread drag window/draws
def drag_window_threaded():
    threading.Thread(target=drag_window,args=(window_units,0.001,True)).start() # time.sleep | False to disable prio system
 
def main():
    dpg.create_context()

    dpg.create_viewport(title=title, decorated=False,clear_color=[0.0,0.0,0.0,0.0],always_on_top=True)
    dpg.set_viewport_always_top(True)
    dpg.setup_dearpygui()
    with dpg.window(label="Example Window",tag="Example Window",pos=(111,111)):
        dpg.add_text("Hello, world")
        window_units.insert(0,"Example Window")     #whenever u create a window and want to make it clickable insert tag at 0 for prio system

    with dpg.window(label="Example Window2",tag="Example Window2",pos=(222,222)):
        dpg.add_text("Hello, world")
        window_units.insert(0,"Example Window2")    #whenever u create a window and want to make it clickable insert tag at 0 for prio system

    with dpg.handler_registry(tag="handler"):
        #drag_window unthreaded == bugs # drag_window_threaded solves
        dpg.add_mouse_click_handler(button=dpg.mvMouseButton_Left,callback=drag_window_threaded)
    with dpg.viewport_drawlist(tag="drawlist"):
            pass
    dpg.show_viewport()
    dpg.toggle_viewport_fullscreen()

    #init the overlay here before u render
    init_overlay(title=title)

    #########example point#########
    dpg.draw_text(parent="drawlist",pos=(500,500),tag="hi",color=(255,0,0),text="hi",size=50)           #draw a text
    point(name="hi",pos=(500,500),tag="hi",width=50,heigth=50)                                          #init the drawing       / make it clickable and moveable
    dpg.draw_rectangle(parent="drawlist",pmin=(666,666),pmax= (1111,1111),tag="hi2",color=(255,0,0))    #draw a rect
    rectangle(name="hi2",pmin=(666,666),pmax= (1111,1111),tag="hi2")                                    #init the rect drwawng  / make it clickable and moveable
                                                                                        
    dpg.draw_text(parent="drawlist",pos=(555,555),tag="hii",color=(255,255,0),text="hii",size=50)
    point(name="hii",pos=(555,555),tag="hii",width=50,heigth=50)
    dpg.delete_item("hii")                                                                              #delete dpg drawing
    del_data("hii")                                                                                     #delete item            / can pass name or tag or filter for a coordinate(first item with the coordinate will be deleted)
    #########example point#########
    
    while dpg.is_dearpygui_running():
        
        make_clickable(window_units=window_units)
        
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

if __name__ == "__main__":
    main()

