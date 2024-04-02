from tkinter import Tk, Canvas, PhotoImage, Button
import pandas
import random
import os
from send_email import send_mail


BACKGROUND_COLOR = "#B1DDC6"
current_item = {}
acronyms_dict = {}
# Read the data from the csv file and convert it to a dictionary using pandas
try:
    data = pandas.read_csv("data/acronyms_to_learn.csv", on_bad_lines='skip')
except FileNotFoundError:
    original_data = pandas.read_csv("data/acronyms.csv", on_bad_lines='skip')
    acronyms_dict = original_data.to_dict(orient="records")
else:
    acronyms_dict = data.to_dict(orient="records")


def next_card():
    global current_item
    global timer_to_flip_card
    screen.after_cancel(timer_to_flip_card)  # Resets timer back to zero every time you go to a new card
    current_item = random.choice(acronyms_dict)
    abbreviation_word = current_item["Abbreviation"]
    canvas.itemconfig(title_text, text="Abbreviation", fill="black")
    canvas.itemconfig(abbreviation_text, text=abbreviation_word, fill="black")
    canvas.itemconfig(card_background, image=img_card_front)
    timer_to_flip_card = screen.after(3000, func=flip_the_card)  # set up a new timer to wait for 3 seconds


def flip_the_card():
    abbreviation_meaning = current_item["Meaning"]
    canvas.itemconfig(title_text, text="Meaning", fill="white")
    canvas.itemconfig(abbreviation_text, text=abbreviation_meaning, fill="white")
    canvas.itemconfig(card_background, image=img_card_back)


def remove_known_acronym():
    global current_item
    acronyms_dict.remove(current_item)
    unknown_acronyms = pandas.DataFrame(acronyms_dict)
    unknown_acronyms.to_csv("data/acronyms_to_learn.csv", index=False)
    # Check if user knows all the words, by checking if the acronyms_to_learn.csv file is empty
    # when empty then delete the file, to avoid IndexError:index out of range error when user runs it again
    # print(len(acronyms_dict))
    if len(acronyms_dict) == 0:
        if os.path.exists("data/acronyms_to_learn.csv"):
            os.remove("data/acronyms_to_learn.csv")
            # Exit/Close the flashcard window/screen, when use masters all the acronyms for the exams
            screen.destroy()
            # Send email to remind user to go and take the CompTia Exams.
            send_mail(message="You can now go and take the CompTIA Security+ Exams.")
    else:
        next_card()


screen = Tk()
screen.title("Flashcard - CompTIA Security+ Acronyms")
screen.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# Flip the card after a given amount of seconds
timer_to_flip_card = screen.after(3000, func=flip_the_card)

canvas = Canvas(width=800, height=526)
img_card_front = PhotoImage(file="images/card_front.png")
img_card_back = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=img_card_front)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
abbreviation_text = canvas.create_text(400, 263, text="", font=("Ariel", 24, "italic"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# unknown button
unknown_button = Button(text="I don't Know", font=("Ariel", 18, "italic"), width=10, bg="#d95730", fg="white",
                        highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)
# Known button
known_button = Button(text="I Know", font=("Ariel", 18, "italic"), bg="#84d930", fg="white", width=10,
                      highlightthickness=0, command=remove_known_acronym)
known_button.grid(row=1, column=1)

next_card()

screen.mainloop()


