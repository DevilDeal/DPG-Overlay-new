from ctypes import c_int
import ctypes,win32api,win32gui,win32con
from dataclasses import dataclass
import dearpygui.dearpygui as dpg
import time

points_tags = []

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
        self.window_pos_x=window_pos_x
        self.window_pos_y=window_pos_y
        self.window_x=window_x 
        self.window_y=window_y
        self.newcords_x=self.window_pos_x+self.window_x
        self.newcords_y=self.window_pos_y+self.window_y
        self.mouse_pos_x=mouse_pos_x
        self.mouse_pos_y=mouse_pos_y
        
                
                
        if self.mouse_pos_y>self.newcords_y or self.mouse_pos_x>self.newcords_x or self.mouse_pos_y<self.window_pos_y or self.mouse_pos_x<self.window_pos_x:
            self.calcpos=True
        else:
            self.calcpos=False
    
    def calcposition(self):
        return self.calcpos,self.window_x,self.window_y,self.window_pos_x,self.window_pos_y

margins = MARGINS(-1, -1,-1, -1)

        
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

def del_data(name):
    break_cond = False
    for list_obj in range(len(points_tags)):
        
        for search in range(len(points_tags[list_obj])):
            
            if points_tags[list_obj][search] == name:
                points_tags.pop(list_obj)
                break_cond = True
                break
        if break_cond:
            break

#drag window // bugs sometimes with drag and drop feature // there is a way to unbug it with threading
def drag_window(window_units : list ,sleep=0.001,prio_system = True):
    
    break_cond=False
    #drag windows / find them using coordinates
    for z in range (len(points_tags)):
        if dpg.is_item_shown(points_tags[z][1]):
            if points_tags[z][0] == "point":
                mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                pos_x = points_tags[z][3]
                pos_y = points_tags[z][4]
                width = points_tags[z][5]
                heigth = points_tags[z][6]
                window=WINDOWS(mouse_pos_x,mouse_pos_y,width,heigth,pos_x,pos_y)
                if not window.calcpos:
                    state_left = win32api.GetKeyState(0x01)
                    mouse_pos_x_old,mouse_pos_y_old=win32gui.GetCursorPos()
                    
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
                        
                        mouse_pos_div_x=pos_x+(mouse_pos_x-mouse_pos_x_old)
                        mouse_pos_div_y=pos_y+(mouse_pos_y-mouse_pos_y_old)
                        points_tags[z][3]=mouse_pos_div_x
                        points_tags[z][4]=mouse_pos_div_y
                        dpg.configure_item(points_tags[z][1], pos=(mouse_pos_div_x,mouse_pos_div_y))
                        if sleep>0:
                            time.sleep(sleep) #add this for performance to lower the thread cpu use so your core programm has enough cpu core space// higher value = more cpu for your core programm
                        if a!=state_left:
                            if prio_system:
                                points_tags.insert(0,points_tags.pop(z))
                            break_cond=True
                            break
            if points_tags[z][0] == "rectangle" and not break_cond:
                for rect in range(0,7,2):
                    mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                    pos_x = points_tags[z][3+rect]
                    pos_y = points_tags[z][4+rect]
                    width = points_tags[z][11]
                    heigth = points_tags[z][12]
                    window=WINDOWS(mouse_pos_x,mouse_pos_y,width,heigth,pos_x-width/2,pos_y-heigth/2)

                    if not window.calcpos:
                        state_left = win32api.GetKeyState(0x01)
                        mouse_pos_x_old,mouse_pos_y_old=win32gui.GetCursorPos()
                        if prio_system:
                            item_config_old = dpg.get_item_configuration(points_tags[z][1])
                            color_old = item_config_old["color"]
                            pmin_old = item_config_old["pmin"]
                            pmax_old = item_config_old["pmax"]
                            
                            color_old = [255*color_old[0],255*color_old[1],255*color_old[2]]
                            #print(color_old,text_old,size_old)
                            dpg.delete_item(points_tags[z][1])
                            dpg.draw_rectangle(pmin=pmin_old,pmax=pmax_old,color=color_old,tag=points_tags[z][1],parent="drawlist")
                    
                        if rect == 4 or rect ==6:
                            pmin_old = dpg.get_item_configuration(points_tags[z][1])["pmin"]
                            pmax_old = dpg.get_item_configuration(points_tags[z][1])["pmax"] 
                            #pmin_old = [points_tags[z][3],points_tags[z][4]
                            #pmax_old = [points_tags[z][5],points_tags[z][6]
                        while True:
                            mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                            a = win32api.GetKeyState(0x01)
                            
                            mouse_pos_div_x=pos_x+(mouse_pos_x-mouse_pos_x_old)
                            mouse_pos_div_y=pos_y+(mouse_pos_y-mouse_pos_y_old)
                            points_tags[z][3+rect]=mouse_pos_div_x
                            points_tags[z][4+rect]=mouse_pos_div_y
                            if rect == 0:
                                points_tags[z][3]=mouse_pos_div_x
                                points_tags[z][4]=mouse_pos_div_y
                                points_tags[z][7]=mouse_pos_div_x
                                points_tags[z][10]=mouse_pos_div_y
                                dpg.configure_item(points_tags[z][1], pmin=(mouse_pos_div_x,mouse_pos_div_y))
                            if rect == 2:
                                points_tags[z][5]=mouse_pos_div_x
                                points_tags[z][6]=mouse_pos_div_y
                                points_tags[z][9]=mouse_pos_div_x
                                points_tags[z][8]=mouse_pos_div_y
                                dpg.configure_item(points_tags[z][1], pmax=(mouse_pos_div_x,mouse_pos_div_y))
                            if rect == 4:
                                points_tags[z][3]=mouse_pos_div_x
                               
                                points_tags[z][6]=mouse_pos_div_y

                                points_tags[z][7]=mouse_pos_div_x
                                points_tags[z][8]=mouse_pos_div_y
                                dpg.configure_item(points_tags[z][1], pmin=(mouse_pos_div_x,pmin_old[1]),pmax=(pmax_old[0],mouse_pos_div_y))
                            if rect == 6:
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
        
        for i in range(len(window_units)) :
            if dpg.is_item_shown(window_units[i]):
                mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                window_pos_x,window_pos_y=dpg.get_item_pos(window_units[i])
                window_x=dpg.get_item_width(window_units[i])
                window_y=dpg.get_item_height(window_units[i])
                if (not dpg.get_item_configuration(window_units[i])["autosize"] or not dpg.get_item_configuration(window_units[i])["no_resize"])  and dpg.get_item_state(window_units[i])["visible"]:
                    window_pos_x = window_pos_x + 4
                    window_pos_y = window_pos_y + 4
                    window_x = window_x - 9
                    window_y = window_y - 9
                if not dpg.get_item_state(window_units[i])["visible"]:
                    window_y = 20
                window=WINDOWS(mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y)
                window_=window_units[i]
                if not window.calcpos :
                    state_left = win32api.GetKeyState(0x01)
                    
                    mouse_pos_x_old,mouse_pos_y_old=win32gui.GetCursorPos()
                    if dpg.get_item_state(window_units[i])["visible"]:
                        window_pos_x = window_pos_x - 4
                        window_pos_y = window_pos_y - 4
                    while True:
                        mouse_pos_x,mouse_pos_y=win32gui.GetCursorPos()
                        a = win32api.GetKeyState(0x01)
                        
                        mouse_pos_div_x=window_pos_x+(mouse_pos_x-mouse_pos_x_old)
                        mouse_pos_div_y=window_pos_y+(mouse_pos_y-mouse_pos_y_old)
                        
                        dpg.set_item_pos(window_, pos=(mouse_pos_div_x,mouse_pos_div_y))
                        if sleep>0:
                            
                            time.sleep(sleep) #add this for performance to lower the thread cpu use so your core programm has enough cpu core space// higher value = more cpu for your core programm
                        if a!=state_left:
                            window_units.insert(0,window_units.pop(i))
                            break_cond=True
                            break

                if break_cond:
                    break
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
                
prev_state = None
window=WINDOWS(0,0,0,0,0,0)
window.calcpos = True
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
                if not dpg.get_item_state(name)["visible"]:
                    window_y = 20
                
                # Check if the cursor is within the window
                window=WINDOWS(mouse_pos_x,mouse_pos_y,window_x,window_y,window_pos_x,window_pos_y)
                
                if not window.calcpos:
                    
                    cursor_in_window = True
                    break
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