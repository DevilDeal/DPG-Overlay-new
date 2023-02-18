from ctypes import c_int
import ctypes,win32api,win32gui,win32con
from dataclasses import dataclass
import dearpygui.dearpygui as dpg
import time

#globals
points_tags = []
window_units = []
window_parameter = {}
drag_exclude_window = {}
dwm = ctypes.windll.dwmapi

#overlay ctypes
class MARGINS(ctypes.Structure):
  _fields_ = [("cxLeftWidth", c_int),
              ("cxRightWidth", c_int),
              ("cyTopHeight", c_int),
              ("cyBottomHeight", c_int)
             ]
#overlay class calc
class WINDOWS:

    def __init__(self,mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y):

        self.left = window_pos_x
        self.top = window_pos_y
        self.window_x = window_x 
        self.window_y = window_y
        self.right = self.left + self.window_x
        self.bottom = self.top + self.window_y
        self.mouse_pos_x = mouse_pos_x
        self.mouse_pos_y = mouse_pos_y
        
        if self.left <= self.mouse_pos_x <= self.right and self.top <=  self.mouse_pos_y <= self.bottom:
            self.calcpos = False
        else:
            self.calcpos = True
    
    def calcposition(self):
        return self.calcpos,self.window_x,self.window_y,self.left,self.top

margins = MARGINS(-1, -1,-1, -1)

@dataclass
class window_create:
    def __init__(self,tag : str , no_move = False) -> list | dict:
        window_units.insert(0,tag)
        window_parameter.update({tag: no_move})

#change move attr
def change_window(tag : str, no_move: bool):
    window_parameter.update({tag: no_move})
    return True

#delete window init
def delete_window(name):
    
    for list_obj in range(len(window_units)):
        
        if window_units[list_obj] == name:
            window_units.pop(list_obj)
            window_parameter.pop(name)
            return True
    else:
        return False
    
@dataclass
class drag_exclude:
    def __init__(self,tag : str, exclude = True) -> dict:
        drag_exclude_window.update({tag: exclude})

#change exclusion of item
def change_exclude(tag : str, exclude : bool):
    drag_exclude_window.update({tag: exclude})

#del exclusion of item
def delete_exclude(tag : str):
    drag_exclude_window.pop(tag)

@dataclass
class point:
    
    def __init__(self, name , pos : tuple[int, int], tag : str, width=50, heigth=50) -> list:
        points_tags.insert(0,["point", tag,name, pos[0], pos[1],width,heigth])

@dataclass
class rectangle:
    
    def __init__(self, name , pmin : tuple[int,int], pmax : tuple[int,int], tag : str, width=50, heigth=50, image=False) -> list:
            x = pmin[0]
            y = pmin[1]
            x2 = pmax[0]
            y2 = pmax[1]
            x3 = pmin[0]
            y3 = pmax[1]
            x4 = pmax[0]
            y4 = pmin[1]
            if not image:
                points_tags.insert(0,["rectangle", tag,name, x, y, x2, y2, x3, y3, x4, y4, width, heigth] )
@dataclass
class line:
    
    def __init__(self, name, x, y, x2, y2 , tag) -> list:
            points_tags.insert(0,["line",tag,name, x, y,x2, y2 ])

#del any draw with tag or coordinate or name
def del_draw(name):
    break_cond = False
    for list_obj in range(len(points_tags)):
        
        for search in range(len(points_tags[list_obj])):
            
            if points_tags[list_obj][search] == name:
                points_tags.pop(list_obj)
                break_cond = True
                break
        if break_cond:
            break

autodetect_dict = { "mvAppItemType::mvWindowAppItem",
                    "mvAppItemType::mvChildWindow",
                    "mvAppItemType::mvText",
                   }

#drag window // bugs sometimes with drag and drop feature // there is a way to unbug it with threading
def drag_window(window_units : list ,sleep=0.001,prio_system = True,bugfix=True,bugfix2=True,autodetect = True):

    #bug fix creates new bug that is not as bad as the previous xd riot games hire me
    if bugfix:
        #bevore everything go trhough every window and check if it is resizable
        for b in range(len(window_units)) :
            if dpg.is_item_shown(window_units[b]):
                if (not dpg.get_item_configuration(window_units[b])["autosize"] or not dpg.get_item_configuration(window_units[b])["no_resize"])  and dpg.get_item_state(window_units[b])["visible"]:
                    mouse_pos_x, mouse_pos_y = win32gui.GetCursorPos()
                    window_pos_x, window_pos_y = dpg.get_item_pos(window_units[b])
                    window_x = dpg.get_item_width(window_units[b])
                    window_y = dpg.get_item_height(window_units[b])
                    window_pos_x = window_pos_x + window_x - 12
                    window_pos_y = window_pos_y + window_y - 12
                    window_x = 12
                    window_y = 12

                    window=WINDOWS(mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y)
                    
                    if not window.calcpos :
                        #prio system
                        window_units.insert(0,window_units.pop(b))
                        return
                    mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                    window_pos_x,window_pos_y=dpg.get_item_pos(window_units[b])
                    window_x=dpg.get_item_width(window_units[b])
                    window_y=dpg.get_item_height(window_units[b])
                    window_pos_x = window_pos_x - 4
                    window_pos_y = window_pos_y - 4
                    window_x = window_x+ 9
                    window_y = window_y+ 9
                    window=WINDOWS(mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y)
                    if not window.calcpos :
                        window_pos_x,window_pos_y=dpg.get_item_pos(window_units[b])
                        window_x=dpg.get_item_width(window_units[b])
                        window_y=dpg.get_item_height(window_units[b])
                        window_pos_x = window_pos_x + 4
                        window_pos_y = window_pos_y + 4
                        window_x = window_x- 9
                        window_y = window_y- 9
                        
                        window=WINDOWS(mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y)

                        if window.calcpos :
                            #prio system
                            window_units.insert(0,window_units.pop(b))
                            return
    if bugfix2:
        #go through window and check if exclusion hovered yes == return
        for i in range(len(window_units)) :
            if dpg.is_item_shown(window_units[i]):
                mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                window_pos_x,window_pos_y=dpg.get_item_pos(window_units[i])
                window_x=dpg.get_item_width(window_units[i])
                window_y=dpg.get_item_height(window_units[i])
                window=WINDOWS(mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y)
                
                if not window.calcpos :
                    for item in drag_exclude_window:
                        if dpg.is_item_hovered(item) and drag_exclude_window.get(item):
                            #prio system
                            window_units.insert(0,window_units.pop(i))
                            return
                    break
    if autodetect:
        all_item=dpg.get_all_items()
        #print(all_item)
        for item in all_item:
            #print(dpg.get_item_alias(item))
            #print(dpg.get_item_info(item)["type"])
            if dpg.get_item_info(item)['hover_handler_applicable'] and not dpg.get_item_info(item)["type"] in autodetect_dict:
                #print(dpg.get_item_info(item))
                if dpg.is_item_hovered(item):
                    for i in range(len(window_units)) :
                        if dpg.is_item_shown(window_units[i]):
                            mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                            window_pos_x,window_pos_y=dpg.get_item_pos(window_units[i])
                            window_x=dpg.get_item_width(window_units[i])
                            window_y=dpg.get_item_height(window_units[i])
                            window=WINDOWS(mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y)
                            if not window.calcpos :
                                window_units.insert(0,window_units.pop(i))
                    return
        #print(autodetect_dict)
    break_cond=False
    #drag windows / find them using coordinates
    for z in range (len(points_tags)):
        #check if item is shown (drawing)
        if dpg.is_item_shown(points_tags[z][1]):
            #for text draws
            if points_tags[z][0] == "point":
                mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                pos_x = points_tags[z][3]
                pos_y = points_tags[z][4]
                width = points_tags[z][5]
                heigth = points_tags[z][6]
                #check if mouse is inside rect drawing clickable
                window=WINDOWS(mouse_pos_x,mouse_pos_y,width,heigth,pos_x,pos_y)
                if not window.calcpos:
                    state_left = win32api.GetKeyState(0x01)
                    mouse_pos_x_old,mouse_pos_y_old=win32gui.GetCursorPos()
                    for i in range(len(window_units)) :
                        if dpg.is_item_shown(window_units[i]):
                            mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                            window_pos_x,window_pos_y=dpg.get_item_pos(window_units[i])
                            window_x=dpg.get_item_width(window_units[i])
                            window_y=dpg.get_item_height(window_units[i])
                            window=WINDOWS(mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y)
                            if not window.calcpos :
                                window_units.insert(0,window_units.pop(i))
                    #prio system del draw then redraw to make it on top for prio next time dragging
                    if prio_system:
                        item_config_old = dpg.get_item_configuration(points_tags[z][1])
                        color_old = item_config_old["color"]
                        text_old = item_config_old["text"]
                        size_old = item_config_old["size"]
                        color_old = [255*color_old[0],255*color_old[1],255*color_old[2]]
                        #print(color_old,text_old,size_old)
                        dpg.delete_item(points_tags[z][1])
                        dpg.draw_text(text=text_old,pos=(pos_x,pos_y),color=color_old,size=size_old,tag=points_tags[z][1],parent="drawlist")
                    while True:
                        mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                        a = win32api.GetKeyState(0x01)
                        # get drag delta and apply to list values and dpg drawing
                        mouse_pos_div_x=pos_x+(mouse_pos_x-mouse_pos_x_old)
                        mouse_pos_div_y=pos_y+(mouse_pos_y-mouse_pos_y_old)
                        points_tags[z][3]=mouse_pos_div_x
                        points_tags[z][4]=mouse_pos_div_y
                        dpg.configure_item(points_tags[z][1], pos=(mouse_pos_div_x,mouse_pos_div_y))
                        if sleep>0:
                            time.sleep(sleep) #add this for performance to lower the thread cpu use so your core programm has enough cpu core space// higher value = more cpu for your core programm
                        if a!=state_left:
                            if prio_system:
                                #prio system insertion for first item checked hovered
                                points_tags.insert(0,points_tags.pop(z))
                            
                            break_cond=True
                            break
            #for rect draws
            if points_tags[z][0] == "rectangle" and not break_cond:
                #go through item list and check if any corner is hovered of the rect
                for rect in range(0,7,2):
                    #get all item information to locate if smth hovered
                    mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                    pos_x = points_tags[z][3+rect]
                    pos_y = points_tags[z][4+rect]
                    width = points_tags[z][11]
                    heigth = points_tags[z][12]
                    window=WINDOWS(mouse_pos_x,mouse_pos_y,width,heigth,pos_x-width/2,pos_y-heigth/2)
                    # if smth hovered
                    if not window.calcpos:
                        state_left = win32api.GetKeyState(0x01)
                        mouse_pos_x_old,mouse_pos_y_old=win32gui.GetCursorPos()
                        #prio system del draw then redraw to make it on top for prio next time dragging
                        for i in range(len(window_units)) :
                                if dpg.is_item_shown(window_units[i]):
                                    mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                                    window_pos_x,window_pos_y=dpg.get_item_pos(window_units[i])
                                    window_x=dpg.get_item_width(window_units[i])
                                    window_y=dpg.get_item_height(window_units[i])
                                    window=WINDOWS(mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y)
                                    if not window.calcpos :
                                        window_units.insert(0,window_units.pop(i))
                        if prio_system:
                            item_config_old = dpg.get_item_configuration(points_tags[z][1])
                            color_old = item_config_old["color"]
                            pmin_old = item_config_old["pmin"]
                            pmax_old = item_config_old["pmax"]
                            
                            color_old = [255*color_old[0],255*color_old[1],255*color_old[2]]
                            #print(color_old,text_old,size_old)
                            dpg.delete_item(points_tags[z][1])
                            dpg.draw_rectangle(pmin=pmin_old,pmax=pmax_old,color=color_old,tag=points_tags[z][1],parent="drawlist")
                        #check if rect point is not pmin or pmax
                        if rect == 4 or rect ==6:
                            #get old item states for easy acces because 
                            pmin_old = dpg.get_item_configuration(points_tags[z][1])["pmin"]
                            pmax_old = dpg.get_item_configuration(points_tags[z][1])["pmax"] 
                            # or u can do it like that does not make difference
                            #pmin_old = [points_tags[z][3],points_tags[z][4]
                            #pmax_old = [points_tags[z][5],points_tags[z][6]
                        while True:
                            mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                            a = win32api.GetKeyState(0x01)
                            #get drag delta z
                            mouse_pos_div_x=pos_x+(mouse_pos_x-mouse_pos_x_old)
                            mouse_pos_div_y=pos_y+(mouse_pos_y-mouse_pos_y_old)
                            #apply drag delta to hovered corner
                            points_tags[z][3+rect]=mouse_pos_div_x
                            points_tags[z][4+rect]=mouse_pos_div_y
                            #check if top left corner is clicked
                            if rect == 0:
                                #apply changes to item storage
                                points_tags[z][3]=mouse_pos_div_x
                                points_tags[z][4]=mouse_pos_div_y
                                points_tags[z][7]=mouse_pos_div_x
                                points_tags[z][10]=mouse_pos_div_y
                                dpg.configure_item(points_tags[z][1], pmin=(mouse_pos_div_x,mouse_pos_div_y))
                            #check if bottom right corner is clicked
                            if rect == 2:
                                #apply changes to item storage
                                points_tags[z][5]=mouse_pos_div_x
                                points_tags[z][6]=mouse_pos_div_y
                                points_tags[z][9]=mouse_pos_div_x
                                points_tags[z][8]=mouse_pos_div_y
                                dpg.configure_item(points_tags[z][1], pmax=(mouse_pos_div_x,mouse_pos_div_y))
                            #check if bottom left corner is clicked
                            if rect == 4:
                                #apply changes to item storage
                                points_tags[z][3]=mouse_pos_div_x
                               
                                points_tags[z][6]=mouse_pos_div_y

                                points_tags[z][7]=mouse_pos_div_x
                                points_tags[z][8]=mouse_pos_div_y
                                dpg.configure_item(points_tags[z][1], pmin=(mouse_pos_div_x,pmin_old[1]),pmax=(pmax_old[0],mouse_pos_div_y))
                            #check if top right corner is clicked
                            if rect == 6:
                                #apply changes to item storage
                                points_tags[z][4]=mouse_pos_div_y
                               
                                points_tags[z][5]=mouse_pos_div_x

                                points_tags[z][9]=mouse_pos_div_x
                                points_tags[z][10]=mouse_pos_div_y
                                dpg.configure_item(points_tags[z][1], pmin=(pmin_old[0],mouse_pos_div_y),pmax=(mouse_pos_div_x,pmax_old[1]))
                            if sleep>0:
                                
                                time.sleep(sleep) #add this for performance to lower the thread cpu use so your core programm has enough cpu core space// higher value = more cpu for your core programm
                            if a!=state_left:
                                if prio_system:
                                    points_tags.insert(0,points_tags.pop(z))
                                break_cond=True
                                break
                    if break_cond:
                        break
            if break_cond:
                break
    if not break_cond:
        
        #loop through windows
        for i in range(len(window_units)) :
            if dpg.is_item_shown(window_units[i]):
                mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                window_pos_x,window_pos_y=dpg.get_item_pos(window_units[i])
                window_x=dpg.get_item_width(window_units[i])
                window_y=dpg.get_item_height(window_units[i])
                #dont drag when imgui resize active
                if (not dpg.get_item_configuration(window_units[i])["autosize"] or not dpg.get_item_configuration(window_units[i])["no_resize"])  and dpg.get_item_state(window_units[i])["visible"]:
                    window_pos_x = window_pos_x + 4
                    window_pos_y = window_pos_y + 4
                    window_x = window_x - 9
                    window_y = window_y - 9

                    #bugfix bottom right corner resize window
                    window_pos_x_, window_pos_y_ = dpg.get_item_pos(window_units[i])
                    window_x_ = dpg.get_item_width(window_units[i])
                    window_y_ = dpg.get_item_height(window_units[i])
                    window_pos_x_ = window_pos_x_ + window_x_ - 12
                    window_pos_y_ = window_pos_y_ + window_y_ - 12
                    window_x_ = 12
                    window_y_ = 12
                    window_=WINDOWS(mouse_pos_x,mouse_pos_y,window_x_,window_y_,window_pos_x_,window_pos_y_)
                    if not window_.calcpos :
                        window_units.insert(0,window_units.pop(i))
                        return
                    #buf fix end

                #when collapsed y is 20
                if not dpg.get_item_state(window_units[i])["visible"]:
                    window_y = 20

                #check if cursor is inside window
                window=WINDOWS(mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y)
                window_=window_units[i]
                if not window.calcpos :
                    item_check=False
                    #prio system update when no_move active
                    if window_parameter.get(window_units[i]):
                        window_units.insert(0,window_units.pop(i))
                        break_cond=True
                        break
                    #exclusion break cond
                    for item in drag_exclude_window:
                        if dpg.is_item_hovered(item) and drag_exclude_window.get(item):
                            
                            window_units.insert(0,window_units.pop(i))
                            break_cond=True
                            item_check = True
                            break
                    #break when exclusion found
                    if item_check:
                        break
                    state_left = win32api.GetKeyState(0x01)
                    
                    mouse_pos_x_old,mouse_pos_y_old=win32gui.GetCursorPos()
                    #reverse pos coords for the math when item is not collapsed
                    if dpg.get_item_state(window_units[i])["visible"]:
                        window_pos_x = window_pos_x - 4
                        window_pos_y = window_pos_y - 4
                    while True:
                        
                        mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                        a = win32api.GetKeyState(0x01)
                        #drag delta Z
                        mouse_pos_div_x=window_pos_x+(mouse_pos_x-mouse_pos_x_old)
                        mouse_pos_div_y=window_pos_y+(mouse_pos_y-mouse_pos_y_old)
                        #change window pos
                        dpg.set_item_pos(window_, pos=(mouse_pos_div_x,mouse_pos_div_y))
                        if sleep>0:
                            
                            time.sleep(sleep) #add this for performance to lower the thread cpu use so your core programm has enough cpu core space// higher value = more cpu for your core programm
                        if a!=state_left:
                            #prio system update
                            window_units.insert(0,window_units.pop(i))
                            break_cond=True
                            break

                if break_cond:
                    break
                #if window not hovered check if border is hovered and resize is enabled
                #if resize enabled and resize is called make window prio for bugfixes
                if (not dpg.get_item_configuration(window_units[i])["autosize"] or not dpg.get_item_configuration(window_units[i])["no_resize"])  and dpg.get_item_state(window_units[i])["visible"]:
                    mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                    window_pos_x,window_pos_y=dpg.get_item_pos(window_units[i])
                    window_x=dpg.get_item_width(window_units[i])
                    window_y=dpg.get_item_height(window_units[i])
                    window_pos_x = window_pos_x - 4
                    window_pos_y = window_pos_y - 4
                    window_x = window_x+ 9
                    window_y = window_y+ 9
                    window=WINDOWS(mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y)
                    if not window.calcpos :
                        window_units.insert(0,window_units.pop(i))
                        break
"""
edge_cursors = {
    "left": win32gui.LoadCursor(None, win32con.IDC_SIZEWE),
    "right": win32gui.LoadCursor(None, win32con.IDC_SIZEWE),
    "top": win32gui.LoadCursor(None, win32con.IDC_SIZENS),
    "bottom": win32gui.LoadCursor(None, win32con.IDC_SIZENS),
    "bottom_right": win32gui.LoadCursor(None, win32con.IDC_SIZENWSE),
}
"""
prev_state = None
window=WINDOWS(0,0,0,0,0,0)
window.calcpos = True
edge_width = 4
def make_clickable(window_units):
        global prev_state ,window
    ### overlay thingy things ###
        cursor_in_window = False
        # Check if the cursor is within any of the windows
        for name in window_units:
            
            if dpg.is_item_shown(name):
                # Get the current mouse position and the position and size of the window
                mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                window_pos_x,window_pos_y=dpg.get_item_pos(name)
                window_x=dpg.get_item_width(name)
                window_y=dpg.get_item_height(name)
                """
                if (not dpg.get_item_configuration(name)["autosize"] or not dpg.get_item_configuration(name)["no_resize"])  and dpg.get_item_state(name)["visible"]:
                    window_pos_x = window_pos_x - 4
                    window_pos_y = window_pos_y - 4
                    window_x = window_x + 8
                    window_y = window_y + 8
                """
                if not dpg.get_item_state(name)["visible"]:
                    window_y = 20
                
                # Check if the cursor is within the window
                window=WINDOWS(mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y)
                
                if not window.calcpos:
                    """
                    if dpg.get_item_state(name)["visible"]:
                        if mouse_pos_x < window_pos_x + edge_width:
                            # set the cursor icon to the left edge icon
                            win32api.SetCursor(edge_cursors["left"])
                        elif mouse_pos_x > window_pos_x + window_x - edge_width:
                            if mouse_pos_y >window_pos_y + window_y- edge_width:
                                # set the cursor icon to the bottom-right corner icon
                                win32api.SetCursor(edge_cursors["bottom_right"])
                            else:
                                # set the cursor icon to the right edge icon
                                win32api.SetCursor(edge_cursors["right"])
                        elif mouse_pos_y < window_pos_y + edge_width :
                            # set the cursor icon to the edge icon
                            win32api.SetCursor(edge_cursors["top"])
                        elif mouse_pos_y > window_pos_y + window_y- edge_width:
                            if mouse_pos_x > window_pos_x + window_x - edge_width:
                                # set the cursor icon to the bottom-right corner icon
                                win32api.SetCursor(edge_cursors["bottom_right"])
                            else:
                                # set the cursor icon to the bottom edge icon
                                win32api.SetCursor(edge_cursors["bottom"])
                        else:
                            # set the cursor icon to the default arrow icon
                            win32api.SetCursor(win32gui.LoadCursor(0, win32con.IDC_ARROW))
                            """
                    cursor_in_window = True
                    break
                """
                else:
                # set the cursor icon to the default arrow icon
                    win32api.SetCursor(win32gui.LoadCursor(0, win32con.IDC_ARROW))"""
            else:
                window.calcpos=True
        else:
            window.calcpos=True
        if window.calcpos:
            for z in range(len(points_tags)):
                
                if dpg.is_item_shown(points_tags[z][1]):    
                    if points_tags[z][0] == "point":
                        mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                        pos_x = points_tags[z][3]
                        pos_y = points_tags[z][4]
                        width = points_tags[z][5]
                        heigth = points_tags[z][6]
                        window=WINDOWS(mouse_pos_x,mouse_pos_y,width,heigth,pos_x,pos_y)
                                    
                        if not window.calcpos: 
                            cursor_in_window = True                                             
                            break
                    if points_tags[z][0] == "rectangle" :
                        for rect in range(0,7,2):
                            mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                            pos_x = points_tags[z][3+rect]
                            pos_y = points_tags[z][4+rect]
                            
                            width = points_tags[z][11]
                            heigth = points_tags[z][12]
                            window=WINDOWS(mouse_pos_x,mouse_pos_y,width,heigth,pos_x-width/2,pos_y-heigth/2)
                            if not window.calcpos: 
                                cursor_in_window = True                                             
                                break
                    if not window.calcpos: 
                        cursor_in_window = True
                        break
        # Check if the cursor has entered one of the rectangles
        if prev_state is None or prev_state != cursor_in_window:
            if cursor_in_window:
                #sets viewport layer clickable
                win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 0)
            else:
                #sets viewport layer transparent
                win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, code)
                
        prev_state = cursor_in_window
        ### overlay thingy things end ###

def init_overlay(title):
    global code,hwnd
    ########################################
    #add this /get pid
    hwnd = win32gui.FindWindow(None, title)

    #extend viewport into desktop resolution
    dwm.DwmExtendFrameIntoClientArea(hwnd, margins)

    #set layered attribute before rendering
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT )

    #constant overlay attribute
    code=win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT