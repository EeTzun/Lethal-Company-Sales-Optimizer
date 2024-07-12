from functools import lru_cache
import math
import tkinter as tk
from collections import Counter

def list_difference(list1, list2):
    counter1 = Counter(list1)
    counter2 = Counter(list2)
    
    counter1.subtract(counter2)
    result = list(counter1.elements())
    
    return result

@lru_cache(None)
def optimize_bag(n, dist, bag = tuple()):
    # uses a sorted bag
    if n == 0:
        # No more items in list
        return dist, []
    
    if bag[n] > dist:
        # This current item is bigger than the distance - cannot be removed
        return optimize_bag(n - 1, dist, bag=bag)
    
    # Calculate 2 options:
    # Option 1: Do not remove the nth item
    dist_n, list_n = optimize_bag(n - 1, dist, bag=bag)
    
    # Option 2: Remove the nth item
    dist_no_n, list_no_n = optimize_bag(n - 1, dist - bag[n], bag=bag)
    dist_no_n -= bag[n]
    
    # Return minimum distance
    # remove item if it makes no differece too
    if dist_no_n <= dist_n: 
        return dist_no_n, list_no_n + [bag[n]]
    else:
        return dist_n, list_n

class LethalCompanySalesOptimizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Lethal Company Sales Optimizer")

        self.prompt_label_numbers = tk.Label(root, text="Enter a list of numbers separated by commas:")
        self.prompt_label_numbers.pack()

        self.entry_numbers = tk.Entry(root, width=50)
        self.entry_numbers.pack()

        self.prompt_label_target = tk.Label(root, text="Enter the target number:")
        self.prompt_label_target.pack()

        self.entry_target = tk.Entry(root, width=50)
        self.entry_target.pack()

        self.submit_button = tk.Button(root, text="Submit", command=self.on_submit)
        self.submit_button.pack()

        self.result_label = tk.Label(root, text="Result: ")
        self.result_label.pack()

        self.sum_label = tk.Label(root, text="Sum: ")
        self.sum_label.pack()

        self.root.bind('<Return>', self.on_enter)

    def on_enter(self, event):
        self.on_submit()
        
    def on_submit(self):
        # Get the input from the entry widget
        input_text = self.entry_numbers.get()
        target = self.entry_target.get()
        # Preprocess input
        bag = input_text.split(',')
        bag_list = []
        for i in bag:
            try:
                if math.isclose(int(float(i)), float(i)):
                    bag_list.append(int(i))
                else:
                    bag_list.append(float(i))
            except:
                pass

        if math.isclose(int(float(target)), float(target)):
            target = int(float(target))
        else:
            target = float(target)

        # Sort the bag and initialize variables
        bag_list = sorted(bag_list)
        print(bag_list)
        n = len(bag_list)
        total_sum = sum(bag_list)
        dist = total_sum - target
        # Add dummy element for 1-based index
        bag_list = [0] + bag_list
        bag_list = tuple(bag_list)


        # Calculate sum:
        if sum(bag_list)<target:
            self.result_label.config(text=f"Sum of item values are too low: {sum(bag_list)}")
            return
        
        try:
            # Do calculations
            optimize_bag.cache_clear()
            final_dist, removed_items = optimize_bag(n, dist, bag=bag_list)
            remaining_items = list_difference(bag_list[1:],removed_items)

            # Display the result
            self.result_label.config(text=f"Result: {remaining_items}")
            self.sum_label.config(text=f"Sum: {sum(remaining_items)}")
        except ValueError:
            # Handle the case where the input is not a valid list of numbers
            self.messagebox.showerror("Invalid input", "Please enter a valid list of numbers separated by commas.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LethalCompanySalesOptimizer(root)
    root.mainloop()
