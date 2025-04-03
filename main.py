import gi
import random
import string

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class RandomizerApp(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Randomizer App")
        self.set_default_size(600, 400)

        # Header Bar
        header_bar = Gtk.HeaderBar()
        self.set_titlebar(header_bar)
        
        # Box to center buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        header_bar.pack_start(button_box)

        # Menu buttons
        labels = ["Coin", "Dice", "Card", "Bag of Balls", "Numbers", "Characters", "Custom"]
        for label in labels:
            button = Gtk.Button(label=label)
            button.connect("clicked", self.on_menu_button_clicked)
            button_box.append(button)

        # Content Area
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.main_box.set_vexpand(True)
        self.set_child(self.main_box)

        self.label = Gtk.Label()
        self.main_box.append(self.label)

        # Coin Section
        self.coin_spin_button = Gtk.SpinButton()
        self.coin_spin_button.set_range(1, 100)
        self.coin_spin_button.set_increments(1, 1)
        self.coin_spin_button.set_visible(False)
        self.main_box.append(self.coin_spin_button)
        
        self.flip_button = Gtk.Button(label="Flip")
        self.flip_button.set_visible(False)
        self.flip_button.connect("clicked", self.on_flip_clicked)
        self.main_box.append(self.flip_button)
        
        self.flip_result_label = Gtk.Label()
        self.flip_result_label.set_visible(False)
        self.flip_result_label.set_wrap(True)
        self.main_box.append(self.flip_result_label)

        # Dice Section
        self.dice_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.dice_container.set_visible(False)
        self.main_box.append(self.dice_container)
        
        self.add_die_button = Gtk.Button(label="Add Die")
        self.add_die_button.connect("clicked", self.on_add_die_clicked)
        self.dice_container.append(self.add_die_button)

        self.dice_list = []

        self.dice_button = Gtk.Button(label="Toss Dice")
        self.dice_button.set_visible(False)
        self.dice_button.connect("clicked", self.on_dice_clicked)
        self.main_box.append(self.dice_button)
        
        self.dice_result_label = Gtk.Label()
        self.dice_result_label.set_visible(False)
        self.dice_result_label.set_wrap(True)
        self.main_box.append(self.dice_result_label)

        self.card_button = Gtk.Button(label="Pick Card")
        self.card_button.set_visible(False)
        self.card_button.connect("clicked", self.on_card_clicked)
        self.main_box.append(self.card_button)

        self.blue_ball_spin = Gtk.SpinButton()
        self.blue_ball_spin.set_range(0, 100)
        self.blue_ball_spin.set_value(7)
        self.blue_ball_spin.set_increments(1, 1)
        self.blue_ball_spin.set_visible(False)
        self.main_box.append(self.blue_ball_spin)

        self.red_ball_spin = Gtk.SpinButton()
        self.red_ball_spin.set_range(0, 100)
        self.red_ball_spin.set_value(3)
        self.red_ball_spin.set_increments(1, 1)
        self.red_ball_spin.set_visible(False)
        self.main_box.append(self.red_ball_spin)

        self.ball_button = Gtk.Button(label="Pick Ball")
        self.ball_button.set_visible(False)
        self.ball_button.connect("clicked", self.on_ball_clicked)
        self.main_box.append(self.ball_button)

        # Numbers Section
        self.numbers_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.numbers_container.set_visible(False)
        self.main_box.append(self.numbers_container)
        
        # Lower limit controls
        lower_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        lower_label = Gtk.Label(label="Lower Limit:")
        lower_box.append(lower_label)
        self.lower_spin = Gtk.SpinButton()
        self.lower_spin.set_range(-100000, 100000)
        self.lower_spin.set_value(0)
        self.lower_spin.set_increments(1, 10)
        lower_box.append(self.lower_spin)
        self.numbers_container.append(lower_box)
        
        # Upper limit controls
        upper_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        upper_label = Gtk.Label(label="Upper Limit:")
        upper_box.append(upper_label)
        self.upper_spin = Gtk.SpinButton()
        self.upper_spin.set_range(-100000, 100000)
        self.upper_spin.set_value(999)
        self.upper_spin.set_increments(1, 10)
        upper_box.append(self.upper_spin)
        self.numbers_container.append(upper_box)

        self.number_button = Gtk.Button(label="Pick Number")
        self.number_button.set_visible(False)
        self.number_button.connect("clicked", self.on_number_clicked)
        self.main_box.append(self.number_button)

        # Characters Section
        self.characters_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.characters_container.set_visible(False)
        self.main_box.append(self.characters_container)
        
        # Character set selection
        char_set_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        char_set_label = Gtk.Label(label="Character Set:")
        char_set_box.append(char_set_label)
        
        self.char_set_dropdown = Gtk.DropDown.new_from_strings([
            "ASCII Printable",
            "UTF-8 (Basic)",
            "English Alphabet (Upper)",
            "English Alphabet (Lower)",
            "Digits",
            "Punctuation"
        ])
        char_set_box.append(self.char_set_dropdown)
        self.characters_container.append(char_set_box)

        self.character_button = Gtk.Button(label="Pick Character")
        self.character_button.set_visible(False)
        self.character_button.connect("clicked", self.on_character_clicked)
        self.main_box.append(self.character_button)

        # Custom Section
        self.custom_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.custom_container.set_visible(False)
        self.main_box.append(self.custom_container)
        
        # Custom list entry
        custom_entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        custom_label = Gtk.Label(label="Enter items (comma separated):")
        custom_entry_box.append(custom_label)
        
        self.custom_entry = Gtk.Entry()
        self.custom_entry.set_placeholder_text("e.g., Apple, Banana, Cherry, 42, #")
        self.custom_entry.set_hexpand(True)
        custom_entry_box.append(self.custom_entry)
        self.custom_container.append(custom_entry_box)
        
        # Example label
        example_label = Gtk.Label(label="Example: Red, Green, Blue, 1, 2, 3")
        example_label.set_css_classes(["dim-label"])
        self.custom_container.append(example_label)

        self.custom_button = Gtk.Button(label="Pick Custom")
        self.custom_button.set_visible(False)
        self.custom_button.connect("clicked", self.on_custom_clicked)
        self.main_box.append(self.custom_button)
        
        self.custom_result_label = Gtk.Label()
        self.custom_result_label.set_visible(False)
        self.custom_result_label.set_wrap(True)
        self.main_box.append(self.custom_result_label)

    def on_menu_button_clicked(self, button):
        selected_option = button.get_label()
        
        self.coin_spin_button.set_visible(selected_option == "Coin")
        self.flip_button.set_visible(selected_option == "Coin")
        self.flip_result_label.set_visible(selected_option == "Coin")
        
        self.dice_container.set_visible(selected_option == "Dice")
        self.dice_button.set_visible(selected_option == "Dice")
        self.dice_result_label.set_visible(selected_option == "Dice")
        
        self.card_button.set_visible(selected_option == "Card")
        self.blue_ball_spin.set_visible(selected_option == "Bag of Balls")
        self.red_ball_spin.set_visible(selected_option == "Bag of Balls")
        self.ball_button.set_visible(selected_option == "Bag of Balls")
        self.numbers_container.set_visible(selected_option == "Numbers")
        self.number_button.set_visible(selected_option == "Numbers")
        self.characters_container.set_visible(selected_option == "Characters")
        self.character_button.set_visible(selected_option == "Characters")
        self.custom_container.set_visible(selected_option == "Custom")
        self.custom_button.set_visible(selected_option == "Custom")
        self.custom_result_label.set_visible(selected_option == "Custom")

    def on_add_die_clicked(self, button):
        if len(self.dice_list) < 10:
            die_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            die_spin_button = Gtk.SpinButton()
            die_spin_button.set_range(2, 100)
            die_spin_button.set_value(6)
            die_spin_button.set_increments(1, 1)
            die_box.append(die_spin_button)
            self.dice_container.append(die_box)
            self.dice_list.append(die_spin_button)

    def on_flip_clicked(self, button):
        num_coins = min(self.coin_spin_button.get_value_as_int(), 100)
        results = [random.choice(["Heads", "Tails"]) for _ in range(num_coins)]
        self.flip_result_label.set_text(f"Results: {', '.join(results)}")

    def on_dice_clicked(self, button):
        results = [random.randint(1, int(die.get_value())) for die in self.dice_list]
        self.dice_result_label.set_text(f"Results: {', '.join(map(str, results))}")

    def on_card_clicked(self, button):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        card = f"{random.choice(ranks)} of {random.choice(suits)}"
        self.label.set_text(f"Card Drawn: {card}")

    def on_ball_clicked(self, button):
        result = random.choice(["Red Ball"] * 3 + ["Blue Ball"] * 7)
        self.label.set_text(f"Ball Picked: {result}")

    def on_number_clicked(self, button):
        lower = self.lower_spin.get_value_as_int()
        upper = self.upper_spin.get_value_as_int()
        # Ensure lower is less than upper
        if lower > upper:
            lower, upper = upper, lower
            self.lower_spin.set_value(lower)
            self.upper_spin.set_value(upper)
        result = random.randint(lower, upper)
        self.label.set_text(f"Number Picked: {result}")

    def on_character_clicked(self, button):
        selected = self.char_set_dropdown.get_selected()
        
        if selected == 0:  # ASCII Printable
            chars = string.printable.strip()
        elif selected == 1:  # UTF-8 (Basic)
            chars = ''.join(chr(i) for i in range(32, 127))  # Basic ASCII
        elif selected == 2:  # English Alphabet (Upper)
            chars = string.ascii_uppercase
        elif selected == 3:  # English Alphabet (Lower)
            chars = string.ascii_lowercase
        elif selected == 4:  # Digits
            chars = string.digits
        elif selected == 5:  # Punctuation
            chars = string.punctuation
        else:
            chars = string.printable.strip()  # Default to ASCII printable
        
        result = random.choice(chars)
        self.label.set_text(f"Character Picked: {result} (Unicode: U+{ord(result):04X})")

    def on_custom_clicked(self, button):
        custom_text = self.custom_entry.get_text().strip()
        if not custom_text:
            self.custom_result_label.set_text("Please enter some items first!")
            return
            
        # Split by comma and strip whitespace from each item
        custom_list = [item.strip() for item in custom_text.split(",") if item.strip()]
        
        if not custom_list:
            self.custom_result_label.set_text("No valid items found in the list!")
            return
            
        result = random.choice(custom_list)
        self.custom_result_label.set_text(f"Custom Pick: {result}\nFrom: {', '.join(custom_list)}")

class RandomizerAppGtk(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.RandomizerApp")

    def do_activate(self):
        window = RandomizerApp(self)
        window.present()

if __name__ == "__main__":
    app = RandomizerAppGtk()
    app.run()