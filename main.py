import tkinter as tk
from tkinter import ttk
import time
import json
import os 

users = []
roles = ["imp","baron","poisoner","scarlet_woman","spy","butler","drunk","recluse","saint","chef","empath","fortune_teller","investigator","librarian","mayor","monk","ravenkeeper","slayer","soldier","undertaker","virgin","washerwoman","po","pukka","shabaloth","zombuul","assassin","devils_advocate","godfather","mastermind","goon","lunatic","moonchild","tinker","chambermaid","courtier","exorcist","fool","gambler","gossip","grandmother","innkeeper","minstrel","pacifist","professor","sailor","tea_lady","fang_gu","no_dashii","vigormortis","vortox","cerenovus","evil_twin","pit-hag","witch","barber","klutz","mutant","sweetheart","artist","clockmaker","dreamer","flowergirl","juggler","mathematician","oracle","philosopher","sage","savant","seamstress","snake_charmer","town_crier","riot","al-hadikhia","legion","leviathan","lleech","lil_monsta","boomdandy","goblin","fearmonger","widow","marionette","mezepheles","psychopath","acrobat","damsel","golem","heretic","politician","puzzlemaster","snitch","amnesiac","atheist","balloonist","bounty_hunter","cannibal","cult_leader","farmer","fisherman","general","lycanthrope","huntsman","magician","noble","pixie","preacher","poppy_grower","king","choirboy","engineer","alchemist","nightwatchman","angel","buddhist","djinn","doomsayer","duchess","fibbin","fiddler","hells_librarian","revolutionary","sentinel","spirit_of_ivory","storm_catcher","toymaker","deus_ex_fiasco","veiled","apprentice","barista","beggar","bishop","bone_collector","bureaucrat","butcher","deviant","gangster","gunslinger","harlot","judge","matron","scapegoat","thief","voudon"]
info = ""
day_log = []
roles = sorted(roles)
bluff_log = []
vote_log = []
possible_roles = []

def update_time():
    current_time = time.strftime('%A %B %d, %Y %I:%M:%S %p')
    time_var.set(current_time)
    time_label.after(1000, update_time)

def update_game_info(*args):
    info = notes_text.get("1.0", "end-1c")


def update_users(*args):
    print("update users")
    # Split by newline
    users = users_text.get("1.0", "end-1c").splitlines()
    # Remove empty lines
    users = [user for user in users if user != ""]
    new_user_dropdown['values'] = users
    new_vote_dropdown['values'] = users
    new_vote_dropdown2['values'] = users

    # Clear the table
    role_table.delete(*role_table.get_children())
    for user in users:
        role_table.insert("", "end", values=[user, ""] + [0] * len(roles))

def save_game():
    print("save game");
    # Save the game info

    # Clear possible roles
    possible_roles.clear()
    # Get Roles from table
    for child in role_table.get_children():
        user = role_table.item(child)["values"][0]
        role = role_table.item(child)["values"][1]

        possible_roles.append({
            "user": user,
            "role": role
        })

    game_info = {
        "day": day_var.get(),
        "role": t_role.get(),
        "notes": notes_text.get("1.0", "end-1c"),
        "users": users_text.get("1.0", "end-1c").splitlines(),
        "day_log": day_log,
        "bluff_log": bluff_log,
        "vote_log": vote_log,
        "possible_roles": possible_roles,
    }

    with open(os.getcwd() + f"/data/game_info.json", "w") as f:
        json.dump(game_info, f, indent=4)

def new_day():
    print("new day")
    day_var.set(str(int(day_var.get()) + 1))
    
    # Save notes in array of dicts
    day_log.append({
        "day": day_var.get(),
        "notes": notes_text.get("1.0", "end-1c")
    })

    # Clear the notes
    #notes_text.delete("1.0", "end-1c")

def add_bluff():
    bluff = {
        "day": day_var.get(),
        "user": new_user_dropdown.get(),
        "bluffed_role_1": new_bluff_dropdown.get(),
        "bluffed_role_2": new_bluff_dropdown2.get(),
        "bluffed_role_3": new_bluff_dropdown3.get(),
    }
    bluff_table.insert("", "end", values=(bluff["day"], bluff["user"], f"{bluff['bluffed_role_1']},{bluff['bluffed_role_2']},{bluff['bluffed_role_3']}"))
    bluff_log.append(bluff)
    print(bluff)

def remove_bluff():
    print("remove bluff")
    selected = bluff_table.selection()
    bluff_table.delete(selected)


def add_vote():
    vote = {
        "day": day_var.get(),
        "user": new_vote_dropdown.get(),
        "nominated_user": new_vote_dropdown2.get(),
        "vote_count": vote_count_input.get(),
    }
    nomination_table.insert("", "end", values=(vote["day"], vote["user"], vote["nominated_user"], vote["vote_count"]))
    vote_log.append(vote)

def remove_vote():
    print("remove vote")
    selected = nomination_table.selection()
    nomination_table.delete(selected)

def update_role():
    print("update role")
    selected = role_table.selection()
    role_table.item(selected, values=(role_table.item(selected[0], "values")[0], user_role_dropdown2.get(), 0, 0, 0, 0, 0, 0))
    

class RoleDropdown(ttk.Combobox):
    def __init__(self, master, values, **kwargs):
        self.current_idx = 0
        self.values = values
        super().__init__(master, values=values, **kwargs)
        self.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        # Scroll up or down depending on the direction of the mouse wheel
        if event.delta > 0:
            self.current_idx = max(0, self.current_idx - 1)
        elif event.delta < 0:
            self.current_idx = min(len(self.values) - 1, self.current_idx + 1)
        self.set(self.values[self.current_idx])

    def update_values(self, new_values):
        self.values = new_values
        self['values'] = new_values

# Create the main window
root = tk.Tk()
root.title("Blood on the Clocktower")
root.geometry("850x500")
root.resizable(False, False)

# Create a notebook widget to hold the tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Create the first tab
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Info")


day_label = tk.Label(tab1, text="Current Day:")
day_label.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="w")

day_var = tk.StringVar(value="0")
day_entry = tk.Entry(tab1, textvariable=day_var)
day_entry.grid(row=0, column=1, padx=(0,10), pady=10, sticky="ew")
# Day Entry Readonly
day_entry.config(state="readonly")




role_label = tk.Label(tab1, text="Current Role:")
role_label.grid(row=1, column=0, padx=(10, 10), pady=10, sticky="w")

t_role = RoleDropdown(tab1, roles)
t_role.set("Select Role")
t_role.grid(row=1, column=1, padx=(10, 10), pady=10, sticky="w")

notes_label = tk.Label(tab1, text="Notes about current game:")
notes_label.grid(row=2, column=0, padx=(10, 10), pady=10, sticky="nw")

notes_text = tk.Text(tab1, height=10)
notes_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nw")
notes_text.bind('<KeyRelease>', update_game_info)

buttons_frame = tk.Frame(tab1)
buttons_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

save_button = tk.Button(buttons_frame, text="Save Game", command=lambda:{save_game()})
save_button.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="e")

new_day_btn = tk.Button(buttons_frame, text="New Day", command=lambda:{new_day()})
new_day_btn.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="e")

reset_button = tk.Button(buttons_frame, text="Reset Game")
reset_button.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="e")

# Add current date and time label
time_var = tk.StringVar()
time_label = tk.Label(tab1, textvariable=time_var)
time_label.grid(row=5, column=0, padx=(10, 10), pady=(10,5), sticky="w")
update_time()

# Add NeosVR Username
neos_label = tk.Label(tab1, text="NeosVR Username: U-Lynix")
neos_label.grid(row=6, column=0, padx=(10, 10), pady=0, sticky="w")

# Create the second tab
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Bluffs")

# Add widgets to the second tab
label2 = tk.Label(tab2, text="Bluffed Roles")
label2.grid(row=1, column=0, padx=(10, 10), pady=10, sticky="w")

frame = ttk.Frame(tab2)
frame.grid(row=2, column=0, padx=(10, 10), pady=10, sticky="w")

bluff_table = ttk.Treeview(frame, columns=("Day", "Username", "Bluffed Roles"), show="headings")
bluff_table.heading("Day", text="Day")
bluff_table.heading("Username", text="Username")
bluff_table.heading("Bluffed Roles", text="Bluffed Roles")
bluff_table.grid(row=0, column=0, sticky="w")

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=bluff_table.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
bluff_table.configure(yscrollcommand=scrollbar.set)

# New User Dropdown
new_user_label = tk.Label(tab2, text="New Bluff")
new_user_label.grid(row=3, column=0, padx=(10, 10), pady=5, sticky="w")

bluff_frame = tk.Frame(tab2)
bluff_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

new_user_var = tk.StringVar()
new_user_dropdown = RoleDropdown(bluff_frame, users)
new_user_dropdown.set("Select User")
new_user_dropdown.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="w")

new_bluff_var = tk.StringVar()
new_bluff_dropdown = RoleDropdown(bluff_frame, roles)
new_bluff_dropdown.set("Select Bluff 1")
new_bluff_dropdown.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="w")

new_bluff_var2 = tk.StringVar()
new_bluff_dropdown2 = RoleDropdown(bluff_frame, roles)
new_bluff_dropdown2.set("Select Bluff 2")
new_bluff_dropdown2.grid(row=0, column=2, padx=(10, 10), pady=10, sticky="w")

new_bluff_var3 = tk.StringVar()
new_bluff_var3.set("Select Bluff")
new_bluff_dropdown3 = RoleDropdown(bluff_frame, roles)
new_bluff_dropdown3.set("Select Bluff 3")
new_bluff_dropdown3.grid(row=0, column=3, padx=(10, 10), pady=10, sticky="w")

# Buttons
buttons_frame2 = tk.Frame(tab2)
buttons_frame2.grid(row=5, column=0, columnspan=2, padx=10, pady=0, sticky="nsew")


add_bluff_btn = tk.Button(buttons_frame2, text="Add Bluff", command=lambda:{add_bluff()})
add_bluff_btn.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="nw")

remove_bluff_btn = tk.Button(buttons_frame2, text="Remove Bluff", command=lambda:{remove_bluff()})
remove_bluff_btn.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="nw")




# Create the third tab
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Voting & Nomination")

# Add widgets to the third tab
label3 = tk.Label(tab3, text="Votes & Nominations")
label3.grid(row=1, column=0, padx=(10, 10), pady=10, sticky="w")

# Create a frame to contain the scrollbar and treeview
nomination_frame = ttk.Frame(tab3)
nomination_frame.grid(row=2, column=0, padx=(10, 10), pady=10, sticky="w")

# Create the treeview and scrollbar inside the frame
nomination_table = ttk.Treeview(nomination_frame, columns=("Day", "User", "Nominated User", "Vote Count"), show="headings")
nomination_table.heading("Day", text="Day")
nomination_table.heading("User", text="User")
nomination_table.heading("Nominated User", text="Nominated User")
nomination_table.heading("Vote Count", text="Vote Count")
nomination_table.pack(side="left", fill="both", expand=True)

nomination_scrollbar = ttk.Scrollbar(nomination_frame, orient="vertical", command=nomination_table.yview)
nomination_scrollbar.pack(side="right", fill="y")

# Set the scrollbar to control the treeview
nomination_table.configure(yscrollcommand=nomination_scrollbar.set)


new_vote = tk.Label(tab3, text="New Nomination")
new_vote.grid(row=3, column=0, padx=(10, 10), pady=5, sticky="w")

vote_frame = tk.Frame(tab3)
vote_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

new_vote_var = tk.StringVar()
new_vote_var.set("Select User")
new_vote_dropdown = RoleDropdown(vote_frame, users)
new_vote_dropdown.set("Nominating User")
new_vote_dropdown.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="w")

new_vote_var2 = tk.StringVar()
new_vote_dropdown2 = RoleDropdown(vote_frame, users)
new_vote_dropdown.set("Select User")
new_vote_dropdown2.set("Nominated User")
new_vote_dropdown2.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="w")

# Vote Count Input
vote_count_label = tk.Label(vote_frame, text="Vote Count: ")
vote_count_label.grid(row=0, column=2, padx=(10, 10), pady=10, sticky="w")
vote_count_input = tk.Entry(vote_frame, width=10)
vote_count_input.grid(row=0, column=3, padx=(10, 10), pady=10, sticky="w")

# Buttons
buttons_frame3 = tk.Frame(tab3)
buttons_frame3.grid(row=5, column=0, columnspan=2, padx=10, pady=0, sticky="nsew")

add_vote_btn = tk.Button(buttons_frame3, text="Add Vote", command=lambda:{add_vote()})
add_vote_btn.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="nw")

remove_vote_btn = tk.Button(buttons_frame3, text="Remove Vote", command=lambda:{remove_vote()})
remove_vote_btn.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="nw")

# Create the third tab
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="User Roles (Possible Roles)")

# Table
# Create a frame to contain the scrollbar and treeview
role_frame = ttk.Frame(tab4)
role_frame.grid(row=1, column=0, padx=(10, 10), pady=10, sticky="w")

label50 = tk.Label(tab4, text="Possible User Roles")
label50.grid(row=1, column=0, padx=(10, 10), pady=10, sticky="w")

frame_roles = ttk.Frame(tab4)
frame_roles.grid(row=2, column=0, padx=(10, 10), pady=10, sticky="w")

role_table = ttk.Treeview(frame_roles, columns=("Username", "Possible Role"), show="headings")
role_table.heading("Username", text="Username")
role_table.heading("Possible Role", text="Possible Role")
role_table.grid(row=0, column=0, sticky="w")

scrollbar = ttk.Scrollbar(frame_roles, orient="vertical", command=role_table.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
role_table.configure(yscrollcommand=scrollbar.set)

# Buttons Update Role
buttons_frame4 = tk.Frame(tab4)
buttons_frame4.grid(row=3, column=0, columnspan=2, padx=10, pady=0, sticky="nsew")

update_role_btn = tk.Button(buttons_frame4, text="Update Role", command=lambda:{update_role()})
update_role_btn.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="nw")

user_role_dropdown2 = RoleDropdown(buttons_frame4, roles)
user_role_dropdown2.set("Select Role")
user_role_dropdown2.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="w")


# Add widgets to the third tab
label4 = tk.Label(tab4, text="Game Setup")


# Create the third tab
tab5 = ttk.Frame(notebook)
notebook.add(tab5, text="Game Setup")

# Add Textbox for List of Users
users_label = tk.Label(tab5, text="List of Users (New line for each):")
users_label.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="w")

users_text = tk.Text(tab5, height=10)
users_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nw")
users_text.bind('<KeyRelease>', update_users)


# Script of Game
game_script_label = tk.Label(tab5, text="Script of Game:")
game_script_label.grid(row=2, column=0, padx=(10, 10), pady=10, sticky="w")

# Entry
game_script_text = tk.Entry(tab5)
game_script_text.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

# Start the main loop
root.mainloop()