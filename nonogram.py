from tkinter import *
import os
from PIL import Image, ImageTk
from tkinter import filedialog
import pickle
from tkinter import messagebox
import time
from abc import ABC, abstractmethod

class GUI(object):
    def __init__(self, storage):
        self.window = Tk()
        self.window.title("Your Nonogram")
        self.bg = PhotoImage(file = "images/bg_paper.png")
        self.storage = storage
        
        
        self.puzzle_library = PuzzleLibrary()
        self.selected_level = "easy"
        
        self.playing_created = False
        

        self.current_game = GameSession(
            self.puzzle_library.puzzles[self.selected_level][0]
        )
        
        
        #main menu frame
        self.main_menu_frame = Frame(self.window, width=800, height=600)
        self.main_menu_frame.pack()
        
        self.main_canvas = Canvas(self.main_menu_frame, width=800, height=600)
        self.main_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.main_canvas.pack()
        
        self.main_canvas.create_text(400, 100, text="Your",font=("Comic Sans MS", 40, "bold"), fill= "#6B5B4D")
        self.main_canvas.create_text(400, 150, text="Nonogram!",font=("Comic Sans MS", 47, "bold"), fill= "#372213")
    
        self.play_button = Button(self.main_canvas, text="Play", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_select_level)
        self.main_canvas.create_window(400, 325, window=self.play_button)
        
        self.create_button = Button(self.main_canvas, text="Creative Mode (play/create)", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_create_or_play)
        self.main_canvas.create_window(400, 400, window=self.create_button)
        
        self.gallery_button = Button(self.main_canvas, text="Gallery", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_gallery)
        self.main_canvas.create_window(400, 475, window=self.gallery_button)
        
        self.tut_button = Button(self.main_canvas, text="?", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_tutorial)
        self.main_canvas.create_window(750, 560, window=self.tut_button)
                
        self.pencil = PhotoImage(file="images/pencil.png")
        self.pencil = self.pencil.subsample(7,7)
        self.main_canvas.create_image(635, 275, image=self.pencil)
        
        self.brain = PhotoImage(file="images/brain.png")
        self.brain = self.brain.subsample(11,11)
        self.main_canvas.create_image(125, 85, image=self.brain)

        
        #select level frame
        self.select_level_frame = Frame(self.window, width=800, height=600)
        
        self.level_canvas = Canvas(self.select_level_frame, width=800, height=600)
        self.level_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.level_canvas.pack()
        
        self.level_canvas.create_text(400, 125, text="Select Level",font=("Comic Sans MS", 40, "bold"), fill= "#372213")
        
        self.easy_button = Button(self.level_canvas, text="Easy", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_easy_select)
        self.level_canvas.create_window(400, 250, window=self.easy_button)
        
        self.medium_button = Button(self.level_canvas, text="Medium", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_medium_select)
        self.level_canvas.create_window(400, 325, window=self.medium_button)
        
        self.hard_button = Button(self.level_canvas, text="Hard", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_hard_select)
        self.level_canvas.create_window(400, 400, window=self.hard_button)
        
        self.back_button = Button(self.level_canvas, text="<<Back", font=("Comic Sans MS", 15, "bold"), fg= "#817468", command=self.back_main)
        self.level_canvas.create_window(75, 50, window=self.back_button)
                
        self.level_canvas.create_text(400, 500, text="* The number of rows and columns varies depending on the seleted level. *",font=("Comic Sans MS", 10, "bold"), fill= "#817468")
        
        self.ez_devil = PhotoImage(file="images/ez_devil.png")
        self.ez_devil = self.ez_devil.subsample(20,20)
        self.level_canvas.create_image(550, 250, image=self.ez_devil)
        
        self.mid_devil = PhotoImage(file="images/mid_devil.png")
        self.mid_devil = self.mid_devil.subsample(20,20)
        self.level_canvas.create_image(245, 320, image=self.mid_devil)
        
        self.hard_devil = PhotoImage(file="images/hard_devil.png")
        self.hard_devil = self.hard_devil.subsample(20,20)
        self.level_canvas.create_image(550, 400, image=self.hard_devil)
        
        
        #select puzzle frame
        self.select_puzzle_frame = Frame(self.window, width=800, height=600)
                
        self.select_puz_canvas = Canvas(self.select_puzzle_frame, width=800, height=600)
        self.select_puz_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.select_puz_canvas.pack()
        
        self.select_puz_canvas.create_text(400, 100, text="Select Puzzle",font=("Comic Sans MS", 30, "bold"), fill= "#372213")
        
        self.puz_1_button = Button(self.select_puz_canvas, text="1", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.start_puzzle_1)
        self.select_puz_canvas.create_window(400, 250, window=self.puz_1_button)
        
        self.puz_2_button = Button(self.select_puz_canvas, text="2", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.start_puzzle_2)
        self.select_puz_canvas.create_window(400, 300, window=self.puz_2_button)
        
        self.puz_3_button = Button(self.select_puz_canvas, text="3", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.start_puzzle_3)
        self.select_puz_canvas.create_window(400, 350, window=self.puz_3_button)
        
        self.puz_4_button = Button(self.select_puz_canvas, text="4", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.start_puzzle_4)
        self.select_puz_canvas.create_window(400, 400, window=self.puz_4_button)
        
        self.puz_5_button = Button(self.select_puz_canvas, text="5", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.start_puzzle_5)
        self.select_puz_canvas.create_window(400, 450, window=self.puz_5_button)
        
        self.puz_back_button = Button(self.select_puzzle_frame, text="<<Back", font=("Comic Sans MS", 15, "bold"), fg= "#817468", command=self.back_select_level)
        self.select_puz_canvas.create_window(75, 50, window=self.puz_back_button)
        
        self.green_paint = PhotoImage(file="images/green_paint.png")
        self.yellow_paint = PhotoImage(file="images/yellow_paint.png")
        self.red_paint = PhotoImage(file="images/red_paint.png")
        
        self.green_paint = self.green_paint.subsample(6,6)
        self.yellow_paint = self.yellow_paint.subsample(6,6)
        self.red_paint = self.red_paint.subsample(6,6)
        
        self.big_easy_devil = PhotoImage(file="images/ez_devil.png")
        self.big_mid_devil = PhotoImage(file="images/mid_devil.png")
        self.big_hard_devil = PhotoImage(file="images/hard_devil.png")
        
        self.big_easy_devil = self.big_easy_devil.subsample(8,8)
        self.big_mid_devil = self.big_mid_devil.subsample(8,8)
        self.big_hard_devil = self.big_hard_devil.subsample(8,8)
        
        
        
        
        
        #puzzle frame      
        self.puzzle_frame = Frame(self.window, width=800, height=600)
          
        self.puzzle_canvas = Canvas(self.puzzle_frame, width=800, height=600)
        self.puzzle_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.puzzle_canvas.pack()
        
        self.heart = PhotoImage(file = "images/heart.png")
        self.heart = self.heart.subsample(20,20)
        
        self.heart_ids = []

        for i in range(3):
            heart = self.puzzle_canvas.create_image(
                325 + i * 65, 60, image= self.heart
            )
            self.heart_ids.append(heart)
            
        self.blank_heart = PhotoImage(file = "images/blank_heart.png")
        self.blank_heart = self.blank_heart.subsample(20,20)
        
        self.cross_wrong_ori = PhotoImage(file = "images/cross_wrong.png")
        self.cross_wrong = self.cross_wrong_ori
        
        self.cross_normal_ori = PhotoImage(file = "images/cross_normal.png")
        self.cross_normal = self.cross_normal_ori
        
        self.trophy = PhotoImage(file = "images/trophy.png")
        self.trophy = self.trophy.subsample(5, 5)
        
        self.bone = PhotoImage(file = "images/bone.png")
        self.bone = self.bone.subsample(5, 5)
        
        self.puzzle_canvas.create_text(400, 550, text="Left Click: Fill Cell | Right Click: Mark X",font=("Comic Sans MS", 10, "bold"), fill= "#817468")
        
        self.easy_back_button = Button(self.puzzle_frame, text="<<Back", font=("Comic Sans MS", 15, "bold"), fg= "#817468", command=self.back_select_puz)
        self.puzzle_canvas.create_window(75, 50, window=self.easy_back_button)
        
        self.cell_size = 50
        self.grid_x = 275
        self.grid_y = 200
        
        self.cell_ids = []
        self.create_grid()
        self.create_clues()
        
        self.info_text = self.puzzle_canvas.create_text( 400, 575, text="",font=("Comic Sans MS", 10, "bold"), fill= "#817468")
       
        
        #create or play your past created
        self.create_or_play_frame = Frame(self.window, width=800, height=600)
                                
        self.create_or_play_canvas = Canvas(self.create_or_play_frame, width=800, height=600)
        self.create_or_play_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.create_or_play_canvas.pack()
        
        self.play_create_button = Button(self.create_or_play_canvas, text="Your created puzzles", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_your_created_puz)
        self.create_or_play_canvas.create_window(400, 250, window=self.play_create_button)
        
        self.create_new_button = Button(self.create_or_play_canvas, text="Create new puzzle", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_select_create)
        self.create_or_play_canvas.create_window(400, 350, window=self.create_new_button)
        
        self.create_or_play_back_button = Button(self.create_or_play_canvas, text="<<Back", font=("Comic Sans MS", 15, "bold"), fg= "#817468", command=self.back_main)
        self.create_or_play_canvas.create_window(75, 50, window=self.create_or_play_back_button)
        
        self.color_plate = PhotoImage(file="images/color_plate.png")
        self.color_plate = self.color_plate.subsample(7,7)
        
        self.create_or_play_canvas.create_image(0, 350, image=self.color_plate, anchor="nw")
        
        self.color_brush = PhotoImage(file="images/color_brush.png")
        self.color_brush = self.color_brush.subsample(7,7)
        
        self.create_or_play_canvas.create_image(550, 350, image=self.color_brush, anchor="nw")
        
        
        
        #select create your puzzle frame
        self.select_create_frame = Frame(self.window, width=800, height=600)
                        
        self.select_create_canvas = Canvas(self.select_create_frame, width=800, height=600)
        self.select_create_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.select_create_canvas.pack()
        
        self.select_create_canvas.create_text(400, 125, text="Select your puzzle size",font=("Comic Sans MS", 35, "bold"), fill= "#372213")
        
        self.scp_back_button = Button(self.select_create_canvas, text="<<Back", font=("Comic Sans MS", 15, "bold"), fg= "#817468", command=self.show_create_or_play)
        self.select_create_canvas.create_window(75, 50, window=self.scp_back_button)
        
        self.fiveXfive_button = Button(self.select_create_canvas, text="5 x 5", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_create_5)
        self.select_create_canvas.create_window(400, 250, window=self.fiveXfive_button)
        
        self.tenXten_button = Button(self.select_create_canvas, text="10 x 10", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_create_10)
        self.select_create_canvas.create_window(400, 350, window=self.tenXten_button)
        
        self.fiftXfift_button = Button(self.select_create_canvas, text="15 x 15", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_create_15)
        self.select_create_canvas.create_window(400, 450, window=self.fiftXfift_button)
        
        self.select_create_canvas.create_image(0, 350, image=self.color_plate, anchor="nw")
        self.select_create_canvas.create_image(550, 350, image=self.color_brush, anchor="nw")
        
        #create your puzzle frame
        self.create_your_puzzle_frame = Frame(self.window, width=800, height=600)
                                
        self.create_your_puz_canvas = Canvas(self.create_your_puzzle_frame, width=800, height=600)
        self.create_your_puz_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.create_your_puz_canvas.pack()
        
        self.up_image = Button(self.create_your_puz_canvas, text="Upload Image", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.upload_image)
        self.create_your_puz_canvas.create_window(400, 50, window=self.up_image)
        
        self.create_your_puz_canvas.create_text(400, 550, text="Select the grid you want to colour.",font=("Comic Sans MS", 10, "bold"), fill= "#817468")
        
        self.done_button = Button(self.create_your_puz_canvas, text="Done", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.done_create_puzzle)
        self.create_your_puz_canvas.create_window( 700, 550, window=self.done_button)
        
        self.preview_button = Button(self.create_your_puz_canvas, text="Preview", font=("Comic Sans MS", 20, "bold"), fg= "#6B5B4D", command=self.show_preview)
        self.create_your_puz_canvas.create_window( 700, 480, window=self.preview_button)
        
        self.uploaded_image = None
        self.uploaded_photo = None
        
        self.cyp_back_button = Button(self.create_your_puz_canvas, text="<<Back", font=("Comic Sans MS", 15, "bold"), fg= "#817468", command=self.show_select_create)
        self.create_your_puz_canvas.create_window(75, 50, window=self.cyp_back_button)
        
        #preview ur created puzzle
        self.preview_frame = Frame(self.window, width=800, height=600)
        
        self.preview_canvas = Canvas(self.preview_frame, width = 800, height=600)
        self.preview_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.preview_canvas.pack()
        
        self.pv_back_button = Button(self.preview_canvas, text="<<Back", font=("Comic Sans MS", 15, "bold"), fg= "#817468", command=self.show_create_frame)
        self.preview_canvas.create_window(75, 50, window=self.pv_back_button)
        
        
        #your created puzzle
        self.your_created_puz_frame = Frame(self.window, width=800, height=600)
        self.your_created_puz_canvas = Canvas(self.your_created_puz_frame, width=800, height=600)
        self.your_created_puz_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.your_created_puz_canvas.pack()
         
        self.ycp_back_button = Button(self.your_created_puz_canvas, text="<<Back", font=("Comic Sans MS", 15, "bold"), fg= "#817468", command=self.show_create_or_play)
        self.your_created_puz_canvas.create_window(75, 50, window=self.ycp_back_button)
        
        self.your_created_puz_canvas.create_image(0, 350, image=self.color_plate, anchor="nw")
        self.your_created_puz_canvas.create_image(550, 350, image=self.color_brush, anchor="nw")
                
        #gallery frame
        self.gallery_frame = Frame(self.window, width=800, height=600)
                                        
        self.gallery_canvas = Canvas(self.gallery_frame, width=800, height=600)
        self.gallery_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.gallery_canvas.pack()
        
        self.gallery_back_button = Button(self.gallery_canvas, text="<<Back", font=("Comic Sans MS", 15, "bold"), fg= "#817468", command=self.back_main)
        self.gallery_canvas.create_window(75, 50, window=self.gallery_back_button)
        
        
        #name puzzle
        self.name_frame = Frame(self.window, width=800, height=600)
        
        self.name_canvas = Canvas(self.name_frame, width=800, height=600)
        self.name_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.name_canvas.pack()
        
        self.name_canvas.create_text(400, 150, text="Name your puzzle", font=("Comic Sans MS", 35, "bold"), fill="#372213")
        
        self.name_entry = Entry(self.name_canvas, font=("Comic Sans MS", 20), fg="#6B5B4D", width=20, justify="center")
        self.name_canvas.create_window(400, 220, window=self.name_entry)
        
        self.name_canvas.create_text(400, 300, text="Creator Name", font=("Comic Sans MS", 35, "bold"), fill="#372213")
        self.creator_name_entry = Entry(self.name_canvas, font=("Comic Sans MS", 20), fg="#6B5B4D", width=20, justify="center")
        self.name_canvas.create_window(400, 370, window=self.creator_name_entry)
        
        self.save_name_button = Button(self.name_canvas, text="Save", font=("Comic Sans MS", 20, "bold"), fg="#6B5B4D", command=self.save_created_puzzle)
        self.name_canvas.create_window(400, 460, window=self.save_name_button)
        
        self.name_back_button = Button(self.name_canvas, text="<<Back", font=("Comic Sans MS", 15, "bold"), fg= "#817468", command=self.show_create_frame)
        self.name_canvas.create_window(75, 50, window=self.name_back_button)
        
        
        
        #tutorial frame
        
        self.tutorial_frame = Frame(self.window, width=800, height=600)
        
        self.tutorial_canvas = Canvas(self.tutorial_frame, width=800, height=600, background="#372213")
        self.tutorial_canvas.pack()
        
        self.next_button = Button(self.tutorial_frame, text="Next>>", font=("Comic Sans MS", 15, "bold"), fg="#6B5B4D", command=self.next_tutorial)
        self.tutorial_canvas.create_window(700, 550, window=self.next_button)
        
        self.tut_back_button = Button(self.tutorial_canvas, text="<<Back", font=("Comic Sans MS", 15, "bold"), fg= "#817468", command=self.back_tutorial)
        self.tutorial_canvas.create_window(75, 50, window=self.tut_back_button)
        
        self.tut_pic_1 = PhotoImage(file="images/1.png")
        self.tut_pic_2 = PhotoImage(file="images/2.png")
        self.tut_pic_3 = PhotoImage(file="images/3.png")
        self.tut_pic_4 = PhotoImage(file="images/4.png")
        self.tut_pic_5 = PhotoImage(file="images/5.png")
        self.tut_pic_6 = PhotoImage(file="images/6.png")
        self.tut_pic_7 = PhotoImage(file="images/7.png")
        self.tut_pic_8 = PhotoImage(file="images/8.png")
        self.tut_pic_9 = PhotoImage(file="images/9.png")
        self.tut_pic_10 = PhotoImage(file="images/10.png")
        self.tut_pic_11 = PhotoImage(file="images/11.png")
        
        
        mainloop()
        
    def hide_frames(self):
        self.main_menu_frame.pack_forget()
        self.select_level_frame.pack_forget()
        self.puzzle_frame.pack_forget()
        self.create_or_play_frame.pack_forget()
        self.select_create_frame.pack_forget()
        self.create_your_puzzle_frame.pack_forget()
        self.gallery_frame.pack_forget()
        self.select_puzzle_frame.pack_forget()
        self.preview_frame.pack_forget()
        self.your_created_puz_frame.pack_forget()
        self.name_frame.pack_forget()
        self.tutorial_frame.pack_forget()
        
    def show_select_level(self):
        self.hide_frames()
        self.select_level_frame.pack()
            
    def show_easy_select(self):
        self.selected_level = "easy"
        self.show_select_puzzle()
                


    def show_medium_select(self):
        self.selected_level = "medium"
        self.show_select_puzzle()
       
    def show_hard_select(self):
        self.selected_level = "hard"
        self.show_select_puzzle()
           
    def show_select_puzzle(self):
        self.hide_frames()
        self.select_puzzle_frame.pack()
        self.select_puz_canvas.delete("paint")
        
        if self.selected_level == "easy":
            self.green_paint_id = self.select_puz_canvas.create_image(0, 300, image=self.green_paint, anchor="nw", tags="paint")
            self.big_easy_devil_id = self.select_puz_canvas.create_image(500, 100, image=self.big_easy_devil, anchor="nw", tags="paint")
            
        elif self.selected_level == "medium":
            self.yellow_paint_id = self.select_puz_canvas.create_image(0, 300, image=self.yellow_paint, anchor="nw", tags="paint")
            self.big_normal_devil_id = self.select_puz_canvas.create_image(500, 100, image=self.big_mid_devil, anchor="nw", tags="paint")
            
        else:
            self.red_paint_id = self.select_puz_canvas.create_image(0, 300, image=self.red_paint, anchor="nw", tags="paint")
            self.big_hard_devil_id = self.select_puz_canvas.create_image(500, 100, image=self.big_hard_devil, anchor="nw", tags="paint")
            
            
    def set_grid_size(self, size=None):
        
        if size is None:
            size = self.current_game.puzzle.size
        
        self.cell_size = min(50, 350//size)
        
        grid_width = size * self.cell_size
        grid_height = size * self.cell_size
        
        self.grid_x = (800 - grid_width) // 2
        self.grid_y = ( 600 - grid_height) // 2 + 20
        
    def set_cross_size(self):
        
        if self.selected_level == "easy":
            size =  40
        if self.selected_level == "medium":
            size = 60
        if self.selected_level == "hard":
            size = 80
        self.cross_normal = self.cross_normal_ori.subsample(size, size)
        self.cross_wrong = self.cross_wrong_ori.subsample(size, size)
        
        
    def start_puzzle(self, index):
        
        self.playing_created = False
    
        if self.selected_level == "easy":
            puzzle = self.puzzle_library.puzzles["easy"][index]

        elif self.selected_level == "medium":
            puzzle = self.puzzle_library.puzzles["medium"][index]

        elif self.selected_level == "hard":
            puzzle = self.puzzle_library.puzzles["hard"][index]

        self.current_game = GameSession(puzzle)
        
        self.set_grid_size()
        self.set_cross_size()
        self.reset_game_board()
        self.hide_frames()
        self.puzzle_frame.pack()
        
    def start_puzzle_1(self):
        self.start_puzzle(0)

    def start_puzzle_2(self):
        self.start_puzzle(1)

    def start_puzzle_3(self):
        self.start_puzzle(2)

    def start_puzzle_4(self):
        self.start_puzzle(3)

    def start_puzzle_5(self):
        self.start_puzzle(4)
        

        
    def show_create_or_play(self):
        
        self.hide_frames()
        self.create_or_play_frame.pack()
                
        
    def back_main(self):
        self.hide_frames()
        self.main_menu_frame.pack()
            
    def back_select_level(self):
        self.hide_frames()
        self.select_level_frame.pack()
        
    def back_select_puz(self):
        
        if self.playing_created:
            self.show_your_created_puz()
            
        else:
            self.hide_frames()
            self.select_puzzle_frame.pack()
        
    def create_grid(self):
        
        size = self.current_game.puzzle.size
        
        for row in range(size):
            row_ids = []
            
            for col in range(size):
                
                x1 = self.grid_x + col * self.cell_size
                y1 = self.grid_y + row * self.cell_size
                
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell = self.puzzle_canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="#6B5B4D", width=2, tags="grid")
                
                row_ids.append(cell)
                
            self.cell_ids.append(row_ids)
        
        self.puzzle_canvas.bind("<Button-1>", self.on_fill_cell) 
        self.puzzle_canvas.bind("<B1-Motion>", self.on_fill_cell)       
        self.puzzle_canvas.bind("<Button-3>", self.on_mark_cell)
        
    def create_clues(self, puzzle=None, canvas=None):
        
        if puzzle is None:
            puzzle = self.current_game.puzzle
            
        row_clues = puzzle.row_clues
        col_clues = puzzle.col_clues
        
        if canvas == None:
            canvas = self.puzzle_canvas

        if self.selected_level == "easy":
            size = 15
            gap = 25
            
        elif self.selected_level == "medium":
            size = 12
            gap = 18
            
        elif self.selected_level == "hard":
            size = 10
            gap = 15
            
        for row in range(len(row_clues)):

            y = self.grid_y + row * self.cell_size + self.cell_size // 2

            for i, clue in enumerate(row_clues[row]):

                x = self.grid_x - gap - (len(row_clues[row]) - i - 1) * gap

                canvas.create_text(
                    x, y,
                    text=clue,
                    font=("Comic Sans MS", size, "bold"),
                    fill="#6B5B4D",
                    tags="clue"
                )
            

        for col in range(len(col_clues)):

            x = self.grid_x + col * self.cell_size + self.cell_size // 2

            for i, clue in enumerate(col_clues[col]):

                y = self.grid_y - gap - (len(col_clues[col]) - i - 1) * gap

                canvas.create_text(
                    x, y,
                    text=clue,
                    font=("Comic Sans MS", size, "bold"),
                    fill="#6B5B4D",
                    tags="clue"
                )
        
        
    
    def on_fill_cell(self, event):

        col = (event.x - self.grid_x) // self.cell_size
        row = (event.y - self.grid_y) // self.cell_size

        size = self.current_game.puzzle.size
        
        if not (0 <= row < size and 0 <= col < size):
            return

        result = self.current_game.fill_cell(row, col)

        if result == "already":
            return
        
        if result == "finished":
            return

        x = self.grid_x + col * self.cell_size + self.cell_size // 2
        y = self.grid_y + row * self.cell_size + self.cell_size // 2

        if result == "correct":

            self.puzzle_canvas.itemconfig(
                self.cell_ids[row][col],
                fill="#6B5B4D"
            )
            
            self.auto_mark("row", row)
            self.auto_mark("column", col)
            
            if self.current_game.is_completed:
                self.reveal_photo()
                self.puzzle_canvas.after(2000, self.show_win)
                self.storage.add_to_gallery(self.current_game.puzzle.revealed_image)
    

        elif result == "wrong":

            self.puzzle_canvas.create_image(
                x, y, image=self.cross_wrong, tags="mark"
            )

            self.update_hearts()
            if self.current_game.lives <= 0:
                self.show_lose()
            
        
                        
    def on_mark_cell(self, event):

        col = (event.x - self.grid_x) // self.cell_size
        row = (event.y - self.grid_y) // self.cell_size
    
        size = self.current_game.puzzle.size
        
        if not (0 <= row < size and 0 <= col < size):
            return

        result = self.current_game.mark_cell(row, col)

        if result == "already":
            return
        
        if result == "finished":
            return

        if result == "correct":

            x = self.grid_x + col * self.cell_size + self.cell_size // 2
            y = self.grid_y + row * self.cell_size + self.cell_size // 2
            
            self.puzzle_canvas.create_image(     
                x, y, image=self.cross_normal, tags="mark"
            )

        elif result == "wrong":

            self.puzzle_canvas.itemconfig(
                self.cell_ids[row][col],
                fill="#CE4949"
            )

            self.update_hearts() 
            
            self.auto_mark("row", row)
            self.auto_mark("column", col)
            
            if self.current_game.lives <= 0:
                self.show_lose()
                
    def auto_mark(self, line_type, index):
        if not self.current_game.check_line_complete(line_type, index):
            return
        
        size = self.current_game.puzzle.size
        
        for i in range(size):
            
            if line_type == "row":
                row = index
                col = i
                
            else:
                row = i
                col = index
                
            if self.current_game.fill_grid[row][col] == 0 and self.current_game.mark_grid[row][col] == 0:
                x = self.grid_x + col * self.cell_size + self.cell_size // 2
                y = self.grid_y + row * self.cell_size + self.cell_size // 2
                
                self.puzzle_canvas.create_image(
                    x, y, image=self.cross_normal, tags="mark"
                )
                
                self.current_game.mark_grid[row][col] = 1
            
    def update_hearts(self):
        
        for i, heart in enumerate(self.heart_ids):
            if i < self.current_game.lives:
                self.puzzle_canvas.itemconfig(heart, image=self.heart)
            else:
                self.puzzle_canvas.itemconfig(heart, image=self.blank_heart)
                
    def reveal_photo(self):
        image = self.current_game.puzzle.revealed_image
        
        if image is None:
            return
        
        box = self.current_game.puzzle.size * self.cell_size
        self.reveal_box = box
        
        img = Image.open(image)
        img = img.resize((box, box))
        
        self.reveal_target = img
        empty = img.crop((0, 0, 1, box)) #crop(left top right bottom)
        self.solution_image = ImageTk.PhotoImage(empty)
        
        cx = self.grid_x + box // 2
        cy = self.grid_y + box // 2
        self.solution_id = self.puzzle_canvas.create_image(
            cx, cy, image=self.solution_image,tags="solution"
        )       
        
        self.wipe_pic()
        
        
    def wipe_pic(self, step = 0, total = 20):
    
        if not self.puzzle_canvas.find_withtag("solution"):
            return
        
        w = int(self.reveal_box * step / total)
        
        if w > 0:
            part = self.reveal_target.crop((0, 0, w, self.reveal_box))
            
            self.solution_image = ImageTk.PhotoImage(part)
            
            self.puzzle_canvas.itemconfig(self.solution_id, image=self.solution_image)
            
            
        if step < total:
            step += 1
            self.puzzle_canvas.after(50, self.wipe_pic, step, total)
        
        
    def show_win(self):
        
        self.trophy_id = self.puzzle_canvas.create_image(
            400, 0, image=self.trophy, tags="end"
        )
        
        self.move_trophy()
        
    def move_trophy(self):
        
        x, y = self.puzzle_canvas.coords(self.trophy_id)
        
        if y >= 300:
            self.puzzle_canvas.coords(self.trophy_id, 400, 300)
            return
        
        self.puzzle_canvas.move(self.trophy_id, 0, 15)
        self.puzzle_canvas.after(10, self.move_trophy)
    

        
    def show_lose(self):
        
        self.bone_id = self.puzzle_canvas.create_image(
            400, 300, image=self.bone, tags="end"
        )
        self.time = 12 
        self.move_bone()
        
    def move_bone(self):
        if self.time == 0:
            self.puzzle_canvas.coords(self.bone_id, 400, 300)
            return
        
        if self.time % 2 == 0:
            dx = 8
        else:
            dx = -8
        
        self.puzzle_canvas.coords(self.bone_id, 400 + dx, 300)
        
        self.time -= 1
        self.puzzle_canvas.after(50, self.move_bone)
        
    def reset_game_board(self):

        self.puzzle_canvas.delete("grid")
        self.puzzle_canvas.delete("clue")
        self.puzzle_canvas.delete("mark")
        self.puzzle_canvas.delete("end")
        self.puzzle_canvas.delete("solution")

        self.cell_ids = []

        self.create_grid()
        self.create_clues()

        self.update_hearts()
        
        self.puzzle_canvas.itemconfig(self.info_text, text=self.current_game.puzzle.get_info())
        
     
        
    #player creation zone
    
    def show_select_create(self):
                
        self.hide_frames()
        self.select_create_frame.pack()
        
    def show_create_your_grid(self, size):
        
        self.uploaded_image = None
        self.create_your_puz_canvas.delete("preview_img")
        self.creator = PuzzleCreator(size)
        self.hide_frames()
        self.create_your_puzzle_frame.pack()
        
        self.draw_creator_grid()
       
        
    def show_create_5(self):
        self.selected_level = "easy"
        self.show_create_your_grid(5)
        
    def show_create_10(self):
        self.selected_level = 'medium'
        self.show_create_your_grid(10)
        
    def show_create_15(self):
        self.selected_level = "hard"
        self.show_create_your_grid(15)
        
    def draw_creator_grid(self):
        size = self.creator.size
        
        self.create_your_puz_canvas.delete("grid")
        
        grid_size = 400
        cell_size = grid_size / size
        
        start_x = 200
        start_y = 100
        
        for row in range(size):
            for col in range(size):
                
                x1 = start_x + col * cell_size
                y1 = start_y + row * cell_size
                
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                if self.creator.solution_grid[row][col] == 1:
                    color = "#6B5B4D"
                else:
                    color = "white"
                    
                self.create_your_puz_canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="#817468",
                    tags="grid"
                )
                
        self.create_your_puz_canvas.bind(
            "<Button-1>", self.fill_creator_cell
        )
                
    def fill_creator_cell(self, event):
        size = self.creator.size
        
        grid_size = 400
        cell_size = grid_size/size
        
        start_x = 200
        start_y = 100
        
        col = int((event.x - start_x) / cell_size)   
        row = int((event.y - start_y) / cell_size)
        
        if 0 <= row < size and 0 <= col < size:
            
            if self.creator.solution_grid[row][col] == 0:
                self.creator.solution_grid[row][col] = 1
            
            else:
                self.creator.solution_grid[row][col] = 0
            
            self.draw_creator_grid()
            
        
    def show_preview(self):
        
        self.creator.generate_clues()
        
        self.hide_frames()
        self.preview_frame.pack()
        
        self.preview_canvas.delete("preview")
        self.preview_canvas.delete("clue")
        
        self.set_grid_size(self.creator.size)
        
        self.draw_preview()
        self.create_clues(self.creator, self.preview_canvas)
        
         
    def draw_preview(self):
        size = self.creator.size
            
        for row in range(size):
            
            for col in range(size):
                
                x1 = self.grid_x + col * self.cell_size
                y1 = self.grid_y + row * self.cell_size
                
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                if self.creator.solution_grid[row][col] == 1:
                    color = "#6B5B4D"
                else:
                    color = "white"
                    
                self.preview_canvas.create_rectangle(
                    x1,y1,x2,y2,
                    fill = color,
                    outline="#817468",
                    tags="preview"
                )
        
    def upload_image(self):
        path = filedialog.askopenfilename(
            title = "Select an image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")]
        )
        if not path:
            return
        
        try:
            img = Image.open(path).convert("RGB")
        except OSError:
            messagebox.showerror("Error", "Cannot open this image file.")
            return
        
        img.thumbnail((400, 400))
        
        self.uploaded_image = img
        
        for_show = img.copy()
        for_show.thumbnail((150, 150))
        
        self.uploaded_photo = ImageTk.PhotoImage(for_show)
        
        self.create_your_puz_canvas.delete("preview_img")
        self.create_your_puz_canvas.create_image(
            700, 250, image=self.uploaded_photo, tags="preview_img"
        )
        
    def done_create_puzzle(self):
            
        fill = False
        for row in self.creator.solution_grid:
            if 1 in row:
                fill= True
                
        if not fill:
            messagebox.showwarning("Empty", "Please fill in at least 1 cell")
            return
        
        self.name_entry.delete(0, END)
        self.creator_name_entry.delete(0, END)
        
        self.hide_frames()
        self.name_frame.pack()
        
        
        
    def save_created_puzzle(self):
        
        name = self.name_entry.get().strip()
        creator = self.creator_name_entry.get().strip()
        
        if name == "":
            messagebox.showwarning("No puzzle name", "Please enter a name")
            return

        if creator == "":
            messagebox.showwarning("No creator name", "Please enter a name")
            return
        
        if len(name) > 20 or len(creator) > 20:
            messagebox.showwarning("Too long", "Name must be within 20 characters")
            return
                
        grid = []
        
        for row in self.creator.solution_grid:
            grid.append(row[:])
            
        puzzle = CreatedPuzzle(name, self.creator.size, grid, creator)
        
        if self.uploaded_image is not None:
            img_path = os.path.join(self.storage.gallery, f"puzzle_{int(time.time())}.png")
        
            try:
                self.uploaded_image.save(img_path)
                puzzle.revealed_image = img_path
            
            except OSError:
                messagebox.showerror("Error", "Can not save image.")
                
            self.uploaded_image = None
            
        self.storage.add_puzzle(puzzle)
        self.show_create_or_play()
    
        
    def show_create_frame(self):
        self.hide_frames()
        self.create_your_puzzle_frame.pack()
        
        
    #player created puz 
    def show_your_created_puz(self):
        self.hide_frames()
        self.your_created_puz_frame.pack()
        
        self.your_created_puz_canvas.delete("item")
        
        for i, puzzle in enumerate(self.storage.puzzles):
            butt = Button(
                self.your_created_puz_canvas, text=puzzle.name, font=("Comic Sans MS", 15, "bold"), fg="#6B5B4D",
                command=self.make_play(puzzle)
            )
            self.your_created_puz_canvas.create_window(380, 200 + i * 50, window=butt, tags="item")
            
            delbutt = Button(
                self.your_created_puz_canvas, text="Delete", font=("Comic Sans MS", 12, "bold"), fg="#CE4949",
                command=self.make_delete(puzzle)
            )
            self.your_created_puz_canvas.create_window(560, 200 + i * 50, window=delbutt, tags="item")
            
    def make_play(self, puzzle):
        def play():
            self.play_create(puzzle)
            
        return play    
         
    def make_delete(self, puzzle):
        def delete():
            if messagebox.askyesno("Delete", f"Delete {puzzle.name}?"):
                self.storage.remove_puzzle(puzzle)
                self.show_your_created_puz()
        
        return delete
            
    def play_create(self, puzzle):
        
        self.playing_created = True
        
        self.current_game = GameSession(puzzle)
        sizes = {5: "easy", 10: "medium", 15: "hard"}
        self.selected_level = sizes[puzzle.size]
        
        self.set_grid_size()
        self.set_cross_size()
        self.reset_game_board()
        self.hide_frames()
        self.puzzle_frame.pack()
        
        
    
    #gallery
    def show_gallery(self):
        self.hide_frames()    
        self.gallery_frame.pack()
        
        self.gallery_canvas.delete("item")
        self.gallery_photos = []
        
        for i, path in enumerate(self.storage.gallery_items):
            try:
                img = Image.open(path)
            except OSError:
                continue
            
            img.thumbnail((100,100))
            photo = ImageTk.PhotoImage(img)
            self.gallery_photos.append(photo)
            
            col = i % 5
            row = i // 5
            x = 120 + col * 140
            y = 160 + row * 130
            self.gallery_canvas.create_image(x, y, image=photo, tags="item")
            
            
            
    #tutorial
    def show_tutorial(self):
        self.tutorial_step = 1
        self.hide_frames()
        self.tutorial_frame.pack()
        self.update_tutorial()
        
    
    def update_tutorial(self):
        
        self.tutorial_canvas.delete("tutorial")
        
        if self.tutorial_step == 1:
            text = "In main menu, you can see 4 options:\n1.Play - click when you want to play a normal mode.\n2.Creative Mode - here you can create and play your past created puzzles.\n3.Gallery - here you can see all revealed images of puzzles you completed.\n4.? - this is a tutorial."
            pic = self.tut_pic_1
            
        elif self.tutorial_step == 2:
            text = "If you click on \"Play\", it will show 3 level of difficulties\nIf you click on each of level, it will appear 5 puzzles that you can choose"
            pic = self.tut_pic_2
            
        elif self.tutorial_step == 3:
            text = "Each level has different size of grids. More grids, more chalenges.\nEasy - 5x5\nMedium - 10x10\nHard - 15x15"
            pic = self.tut_pic_3
            
            
        elif self.tutorial_step == 4:
            text = "Click left to fill the cell according to the clues show in each row and column.\nSeparate number means they should be separated at leat one cell.\nClick right to mark the cell you think it should be blank\nOnce every solution cells in each row/column are filled, the auto mark will appears"
            pic = self.tut_pic_4
            
        
        elif self.tutorial_step == 5:
            text = "If you fill in the wrong cell, red mark will appear to replace.\nIf you mark the wrong cell, red fill will appear to replace.\n Both reduces 1 of your lives."
            pic = self.tut_pic_5
            
        elif self.tutorial_step == 6:
            text = "If you cilck on \"Creative Mode\", there will be 2 options.\nTo play your past created puzzles or to create a new one"
            pic = self.tut_pic_6
            
        elif self.tutorial_step == 7:
            text = "If you choose to create a new one, there will be 3 sizes of grid you can choose.\nOnce you choose the size, you can click left to pick the cell you want to fill, click again to unfill.\nThen upload the revealed picture."
            pic = self.tut_pic_7
            
        elif self.tutorial_step == 8:
            text = "You can click preview to see your puzzle with generated clues."
            pic = self.tut_pic_8
            
        elif self.tutorial_step == 9:
            text = "Once you done creating the puzzle, you can click \"Done\".\nThe program will ask you to fill the puzzle's name and creator's name, then save."
            pic = self.tut_pic_9
            
        elif self.tutorial_step == 10:
            text = "Once you save the created puzzles, they will be saved in the \"Your created puzzles\" pagen\n, which you can come to play later.\nYou can click delete if you don't want that puzzle anymore."
            pic = self.tut_pic_10
            
        elif self.tutorial_step == 11:
            text = "This is the \"Gallery\" page.\nYou can view the picture of your completed puzzles, including the custom one\nnote - if you delete the created puzzles, their picture will be gone from gallery too."
            pic = self.tut_pic_11
            
        self.tutorial_canvas.create_text(400, 450, text=text,font=("Comic Sans MS", 10, "bold"), fill= "#D2BEAA", tags="tutorial")
        
        self.tutorial_canvas.create_image(0, 0, image=pic, anchor="nw", tags="tutorial")
            
        if self.tutorial_step == 11:
            self.next_button.config(text="Finish")
        
        else:
            self.next_button.config(text="Next")
            
    
    def next_tutorial(self):
        if self.tutorial_step < 11:
            self.tutorial_step += 1
            self.update_tutorial()
        
        else:
            self.back_main()
            
    def back_tutorial(self):
        if self.tutorial_step > 1:
            self.tutorial_step -= 1
            self.update_tutorial()
            
        else:
            self.back_main()
            
    
        
    
    

class Puzzle(ABC):
    def __init__(self, name, size, solution_grid, revealed_image=None):
        self.name = name
        self.size = size
        self.solution_grid = solution_grid
        self.revealed_image = revealed_image
        
        self.row_clues = []
        self.col_clues = []
        
        self.generate_clues()
        
    @abstractmethod
    def get_info(self):
        pass
        
    def generate_clues(self):
        
        self.row_clues = []
        self.col_clues = []
        for row in self.solution_grid:
            clues = []
            count = 0
            for cell in row:
                if cell == 1:
                    count += 1
                elif count > 0:
                    clues.append(count)
                    count = 0
            if count > 0:
                clues.append(count)
            self.row_clues.append(clues)
            
        for col in range(self.size):
            clues = []
            count = 0
            for row in range(self.size):
                if self.solution_grid[row][col] == 1:
                    count += 1
                elif count > 0:
                    clues.append(count)
                    count = 0
            if count > 0:
                clues.append(count)
            self.col_clues.append(clues)
            
    def check_solution(self, player_grid):
        return player_grid == self.solution_grid
    


class PresetPuzzle(Puzzle):
    def __init__(self, name, size, solution_grid, difficulty, puzzle_id, revealed_image):
        super().__init__(name, size, solution_grid, revealed_image)
        self.difficulty = difficulty
        self.puzzle_id = puzzle_id
        
    def get_info(self):
        return f"{self.difficulty} - {self.puzzle_id}: {self.size} x {self.size}"
        
        
#player creation zone
class CreatedPuzzle(Puzzle):
    def __init__(self, name, size, solution_grid, creator):
        super().__init__(name, size, solution_grid)
        self.creator = creator
        
    def get_info(self):
        return f"Name: {self.name}, Size: {self.size}x{self.size}, Created by: {self.creator}"
    
    
class PuzzleCreator(Puzzle):
    def __init__(self, size):
        
        solution_grid = []
        
        for i in range(size):
            row = []
            
            for j in range(size):
                row.append(0)
                
            solution_grid.append(row)

        super().__init__("Untitled", size, solution_grid)
        
    def get_info(self):
        return f"Creating a {self.size} x {self.size} puzzle"

#state and logic       
class GameSession(object):
    def __init__(self, puzzle, lives = 3):
        self.puzzle = puzzle
        self.lives = lives
        
        self.fill_grid = []
        self.mark_grid = []
        
        for i in range(puzzle.size):
            fill_row = []
            mark_row = []
            
            for j in range(puzzle.size):
                fill_row.append(0)
                mark_row.append(0)
                
            self.fill_grid.append(fill_row)
            self.mark_grid.append(mark_row)
            
            
        self.is_completed = False
        self.mistake = 0
        
    def fill_cell(self, row, col):
        
        if self.lives <= 0 or self.is_completed:
            return "finished"
        
        if self.fill_grid[row][col] == 1:
            return "already"

        if self.mark_grid[row][col] == 1:
            return "already"

        if self.puzzle.solution_grid[row][col] == 1:
            self.fill_grid[row][col] = 1
            self.check_win()
            return "correct"

        else:
            self.mark_grid[row][col] = 1
            self.mistake += 1
            self.lives -= 1
            return "wrong"
        
    def mark_cell(self, row, col):
        
        if self.lives <= 0 or self.is_completed:
            return "finished"
        
        if self.fill_grid[row][col] == 1:
            return "already"

        if self.mark_grid[row][col] == 1:
            return "already"

        self.mark_grid[row][col] = 1

        if self.puzzle.solution_grid[row][col] == 0:
            return "correct"

        else:
            self.mistake += 1
            self.lives -= 1
            return "wrong"
        
    def check_line_complete(self, line_type, index):

        if line_type == "row":
            for col in range(self.puzzle.size):
                if self.puzzle.solution_grid[index][col] == 1:
                    if (self.fill_grid[index][col] == 0
                        and self.mark_grid[index][col] == 0):
                        return False

            return True

        elif line_type == "column":
            for row in range(self.puzzle.size):
                if self.puzzle.solution_grid[row][index] == 1:
                    if (self.fill_grid[row][index] == 0
                        and self.mark_grid[row][index] == 0):
                        return False

            return True
        
        
        

    def check_win(self):
        if self.puzzle.check_solution(self.fill_grid):
            self.is_completed = True
            return True
        return False
    
        
class PuzzleStorage(object):
    def __init__(self, data = "data", gallery = "gallery"):
        self.data = data
        self.gallery = gallery
        self.puzzles = []
        
        self.gallery_items = []
        
        
        os.makedirs(self.data, exist_ok=True)
        os.makedirs(self.gallery, exist_ok=True)
        self.load_puzzles()
        self.load_gallery()
        
    def add_puzzle(self, puzzle):
        self.puzzles.append(puzzle)
        self.save_puzzles()
        
    def save_puzzles(self):
        try:
            with open(os.path.join(self.data, "created.pkl"), "wb") as f:
                pickle.dump(self.puzzles, f)
            
        except OSError as e:
            messagebox.showerror("Error", f"Cannot save the puzzle: {e}")
            
    def load_puzzles(self):
        try:
            with open(os.path.join(self.data, "created.pkl"), "rb") as f:
                self.puzzles = pickle.load(f)
        
        except FileNotFoundError:
            self.puzzles = []
            
        except (pickle.UnpicklingError, EOFError):
            messagebox.showerror("Error", "Save file is corrupted")
            self.puzzles = []
            
    def remove_puzzle(self, puzzle):
        if puzzle in self.puzzles:
            self.puzzles.remove(puzzle)
            self.save_puzzles()
            
        path = puzzle.revealed_image
        if path is not None:
            try:
                os.remove(path)
                
            except OSError as e:
                messagebox.showerror("Error", f"Cannot delete image: {e}")
                
            if path in self.gallery_items:
                self.gallery_items.remove(path)
                self.save_gallery()
                
    #gallery
    
    def add_to_gallery(self, img_path):
        if img_path is None:
            return
        
        if img_path in self.gallery_items:
            return
        
        self.gallery_items.append(img_path)
        self.save_gallery()
        
    def save_gallery(self):
        try:
            with open(os.path.join(self.data, "gallery.pkl"), "wb") as f:
                pickle.dump(self.gallery_items, f)
        except OSError as e:
            messagebox.showerror("Error", f"Cannot save gallery: {e}")
            
    def load_gallery(self):
        try:
            with open(os.path.join(self.data, "gallery.pkl"), "rb") as f:
                self.gallery_items = pickle.load(f)
                
        except FileNotFoundError:
            self.gallery_items = []
            
        except (pickle.UnpicklingError, EOFError):
            messagebox.showerror("Error", "Gallery file is corrupted")
            self.gallery_items = []
        
        
    
class PuzzleLibrary(object):
    def __init__(self):
        
        #ez
        solution_ez_1 = [
            [ 0, 1, 0, 1, 0],
            [ 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1],
            [ 0, 1, 1, 1, 0],
            [ 0, 0, 1, 0, 0]
        ]
        
        solution_ez_2 = [
            [ 0, 1, 0, 1, 0],
            [ 0, 1, 1, 1, 0],
            [ 0, 1, 1, 1, 0],
            [ 0, 1, 1, 1, 0],
            [ 1, 1, 1, 1, 1]
        ]
        
        solution_ez_3 = [
            [ 0, 1, 0, 1, 0],
            [ 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1],
            [ 0, 1, 1, 1, 0]
        ]
        
        #mountain with sun in mid river last row
        solution_ez_4 = [
            [ 1, 0, 0, 0, 1],
            [ 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1]
        ]
        
        solution_ez_5 = [
            [ 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1],
            [ 0, 1, 1, 1, 0],
            [ 0, 0, 1, 0, 0],
            [ 0, 0, 1, 0, 0]
        ]
        
        #medium
        
        solution_mid_1 = [
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 0, 0, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        ]
        
        solution_mid_2 = [
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        solution_mid_3 = [
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 1, 0, 0, 0],
            [1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
        ]
        
        
        solution_mid_4 = [
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
            [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
            [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        ]
        
        solution_mid_5 = [
            [0, 1, 1, 1, 1, 0, 0, 0, 1, 1],
            [0, 0, 1, 1, 0, 1, 1, 0, 0, 1],
            [1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        ]

        #hard
        
        solution_hard_1 = [
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0],
            [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
             
        ]
        
        solution_hard_2 = [
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             
        ]
        
        solution_hard_3 = [
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
             
        ]
        
        solution_hard_4 = [
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0],
            [0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             
        ]
        
        solution_hard_5 = [
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
             
        ]
        
        self.puzzles = {
            "easy": [
                PresetPuzzle("Puzzle 1", 5, solution_ez_1, "Easy", 1, "images/solution1_pic.png"),
                PresetPuzzle("Puzzle 2", 5, solution_ez_2, "Easy", 2, "images/solution2_pic.png"),
                PresetPuzzle("Puzzle 3", 5, solution_ez_3, "Easy", 3, "images/solution3_pic.png"),
                PresetPuzzle("Puzzle 4", 5, solution_ez_4, "Easy", 4, "images/solution4_pic.png"),
                PresetPuzzle("Puzzle 5", 5, solution_ez_5, "Easy", 5, "images/solution5_pic.png")             
            ],
            "medium": [
                PresetPuzzle("Puzzle 1", 10, solution_mid_1, "Medium", 1, "images/solution6_pic.png"),
                PresetPuzzle("Puzzle 2", 10, solution_mid_2, "Medium", 2, "images/solution7_pic.png"),
                PresetPuzzle("Puzzle 3", 10, solution_mid_3, "Medium", 3, "images/solution8_pic.png"),
                PresetPuzzle("Puzzle 4", 10, solution_mid_4, "Medium", 4, "images/solution9_pic.png"),
                PresetPuzzle("Puzzle 5", 10, solution_mid_5, "Medium", 5, "images/solution10_pic.png")
            ],
            "hard": [
                PresetPuzzle("Puzzle 1", 15, solution_hard_1, "Hard", 1, "images/solution11_pic.png"),
                PresetPuzzle("Puzzle 2", 15, solution_hard_2, "Hard", 2, "images/solution12_pic.png"),
                PresetPuzzle("Puzzle 3", 15, solution_hard_3, "Hard", 3, "images/solution13_pic.png"),
                PresetPuzzle("Puzzle 4", 15, solution_hard_4, "Hard", 4, "images/solution14_pic.png"),
                PresetPuzzle("Puzzle 5", 15, solution_hard_5, "Hard", 5, "images/solution15_pic.png")
            ],
        }
        

app = GUI(PuzzleStorage())
