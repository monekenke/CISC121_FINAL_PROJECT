### APP INFORMATION ###
# time complexity: O(n²) worst case, O(n) best case (already sorted)
# space complexity: O(1) (sorted in-place)
# all AI DICLAIMERS are found where they were used

### IMPORTS ###
import gradio as gr
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO
from PIL import Image

################################
### BACKEND (ALGORITHM) CODE ###
################################

def insertion_sort(arr):

    # statistics (returned at the end of the program)
    steps = []
    comparisons = 0
    shifts = 0

    # initial state
    steps.append({
        'array': arr.copy(),
        'current_key': -1,
        'comparing': -1,
        'sorted_boundary': 0,
        'description': 'initial (unsorted) array'
    })

    # start at 2nd element in the array
    for i in range(1, len(arr)):
        # store the current element to be inserted later in the correct position
        key = arr[i]
        # points to the element before the current
        j = i - 1

        # shows which element is being inserted
        steps.append({
            'array': arr.copy(),
            'current_key': i,
            'comparing': -1,
            'sorted_boundary': i,
            'description': f'step {i}: selecting key = {key} at index {i}'
        })

        # build visualization arrays that show proper shifting
        original_arr = arr.copy()  # save original state before any shifts
        
        # move elements greater than key 1 position ahead
        # continue until the correct position is found for key
        while j >= 0 and arr[j] > key:
            # build a clean visualization array for comparison
            vis_arr = []
            
            # add all elements from 0 to j (including the comparing element)
            for k in range(j + 1):
                vis_arr.append(original_arr[k])
            
            # add the key right after j (showing it "moving down")
            vis_arr.append(key)
            
            # add elements between original j+1 and i (these will appear shifted)
            for k in range(j + 1, i):
                vis_arr.append(original_arr[k])
            
            # add remaining unsorted elements from i+1 onwards
            for k in range(i + 1, len(original_arr)):
                vis_arr.append(original_arr[k])
            
            # show comparison
            steps.append({
                'array': vis_arr,
                'current_key': j + 1,  # key is right after the comparing position
                'comparing': j,
                'sorted_boundary': i,
                'description': f'comparing {arr[j]} > {key}: true, will shift right'
            })
            
            # update statistics
            comparisons += 1
            shifts += 1
            
            # shift larger element right in actual array
            arr[j + 1] = arr[j]
            # move position to previous element
            j -= 1
            
        # one more comparison if it is exited due to arr[j] <= key
        if j >= 0:
            comparisons += 1
        # insert key at its correct position
        arr[j + 1] = key
        steps.append({
            'array': arr.copy(),
            'current_key': j + 1,
            'comparing': -1,
            'sorted_boundary': i,
            'description': f'inserting {key} at index {j + 1}'
        })
        
    # final state
    steps.append({
        'array': arr.copy(),
        'current_key': -1,
        'comparing': -1,
        'sorted_boundary': len(arr),
        'description': 'array fully sorted'
    })
    # return in-place modified array and other statistics
    return arr, steps, comparisons, shifts

###########################
### FRONTEND (GUI) CODE ###
###########################
# DISCLAIMER 1: Because of my unfamiliarity with GUIs on Python, I used Claude for help for a portion of this section.
# DISCLAIMER 2: Also because of my unfamiliarity with GUIs, I used a lot of help from StackOverflow and Reddit for help with individual libraries, as well as the syntax and formatting for the chart.
# AI DISCLAIMER: Used Claude to generate colours, recommended bar graph sizes/values, and also how to write the code to convert the graph data into an image.

def visualization(step_data):
    # creates a bar chart visualization of the current step
    
    arr = step_data['array']
    current_key = step_data['current_key']
    comparing = step_data['comparing']
    sorted_boundary = step_data['sorted_boundary']

    fig, ax = plt.subplots(figsize = (12, 6))

    # colours for each bar
    colours = []
    for i in range(len(arr)):
        # check comparing and current_key (highest priority is comparisons)
        if i == comparing:
            colours.append('#3498db')  # blue for comparing
        elif i == current_key:
            colours.append('#f39c12')  # orange for current key
        elif i < sorted_boundary:
            colours.append('#2ecc71')  # green for sorted portion
        else:
            colours.append('#95a5a6')  # gray for unsorted
    
    # create bar chart
    bars = ax.bar(range(len(arr)), arr, color=colours, edgecolor='black', linewidth=1.5)

    # add value labels on top of bars
    for i, (bar, val) in enumerate(zip(bars, arr)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{val}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')
        
    # styling
    ax.set_xlabel('index', fontsize=12, fontweight='bold')
    ax.set_ylabel('value', fontsize=12, fontweight='bold')
    ax.set_title(step_data['description'], fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(range(len(arr)))
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    # create legend
    legend_elements = [
        mpatches.Patch(color='#2ecc71', label='sorted'),
        mpatches.Patch(color='#f39c12', label='current key'),
        mpatches.Patch(color='#3498db', label='comparing'),
        mpatches.Patch(color='#95a5a6', label='unsorted')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    
    # convert plot to image
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    plt.close()
    
    return img

#########################
### UTILITY FUNCTIONS ###
#########################

# AI DICLAIMER: Used Claude to generate the below function, to make sure errors and edge cases are properly handled.
def parse_input(input_str, input_type):
# parses user input into a list of integers
    try:
        if input_type == "manual entry":
            # remove brackets and split by comma
            input_str = input_str.strip('[]')
            arr = [int(x.strip()) for x in input_str.split(',') if x.strip()]
        else:
            arr = eval(input_str)
        
        if len(arr) == 0:
            return None, "error: array cannot be empty for visualization"
        if len(arr) > 20:
            return None, "error: array size limited to 20 elements for visualization"
        
        return arr, None
    except:
        return None, "error: invalid input, enter comma-separated integers (e.g. 5, 3, 8, 1, etc.)"

# AI Disclaimer: Used Claude to generate parts of the below code, mainly how exactly to format everything and some recommendations on how to organize the statistics.
def sort_and_visualize(input_str, input_type, step_num):
    # handles sorting and visualization
    arr, error = parse_input(input_str, input_type)
    if error:
        return None, error, "", ""
    
    # insertion sort (with step tracking)
    sorted_arr, steps, comparisons, shifts = insertion_sort(arr.copy())

    # gets current step
    step_num = max(0, min(step_num, len(steps) - 1))
    current_step = steps[step_num]

    # create visualization
    img = visualization(current_step)
    
    # creates statistics text
    progress = f"Step {step_num + 1} of {len(steps)}"
    stats = f"""
    **STATISTICS**
    - total comparisons: {comparisons}
    - total shifts: {shifts}
    - array size: {len(arr)}
    - time complexity: O(n²) worst case, O(n) best case
    - space complexity: O(1)
    
    **FINAL SORTED ARRAY:** {sorted_arr}
        """
    
    return img, progress, stats, len(steps)

def create_interface():
    # creates the gradio interface
    with gr.Blocks(title = "INSERTION SORT VISUALIZATION") as demo:
        with gr.Row():
            with gr.Column(scale = 1):
                gr.Markdown("## INPUT OPTIONS")

                input_type = gr.Radio(
                    choices = ["manual entry", "preset examples"],
                    value = "manual entry",
                    label = "input type"
                )

                input_text = gr.Textbox(
                    label = "enter array",
                    placeholder = "e.g. 64, 34, 25, 12, 22, 11, 90, etc.",
                    value = "64, 34, 25, 12, 22, 11, 90",
                    lines = 2
                )

                preset_dropdown = gr.Dropdown(
                    # taken from older code only used to test inputs for the sorting algorithm
                    choices=[
                        "already sorted: [1, 2, 3, 4, 5, 6, 7]",
                        "reverse sorted: [9, 8, 7, 6, 5, 4, 3, 2, 1]",
                        "with duplicates: [3, 7, 3, 1, 7, 3]",
                        "with negatives: [-5, 3, -1, 7, -9, 2]",
                        "small array: [5, 2, 8]",
                        "single element: [42]"
                    ],
                    label = "preset examples",
                    visible = False
                )

                # handles whether or not the manual values are shown on-screen vs. the preset values
                def toggle_input(choice):
                    if choice == "manual entry":
                        return gr.update(visible = True), gr.update(visible = False)
                    else:
                        return gr.update(visible = False), gr.update(visible = True)
                
                input_type.change(
                    fn = toggle_input,
                    inputs = [input_type],
                    outputs = [input_text, preset_dropdown]
                )

                def update_from_preset(preset):
                    # extract array from preset string
                    return preset.split(": ")[1]
                
                preset_dropdown.change(
                    fn = update_from_preset,
                    inputs = [preset_dropdown],
                    outputs = [input_text]
                )

                sort_button = gr.Button("start sorting", variant = "primary", size = "lg")

                gr.Markdown("## step controls")
                step_slider = gr.Slider(
                    minimum = 0,
                    maximum = 10,
                    step = 1,
                    value = 0,
                    label = "Step Number",
                    interactive = True
                )

                with gr.Row():
                    prev_button = gr.Button("<- previous")
                    next_button = gr.Button("next ->")
                
                progress_text = gr.Textbox(label = "progress", interactive = False)
            
            with gr.Column(scale = 2):
                gr.Markdown("## visualization")
                viz_output = gr.Image(label = "array state", type = "pil")
                statistics = gr.Markdown("click 'start sorting' to begin")
        
        # hidden state to store total steps
        total_steps = gr.State(value = 10)

        ### event handlers ###
        # start sort
        def start_sort(input_str, input_type):
            img, prog, stats, steps = sort_and_visualize(input_str, input_type, 0)
            return img, prog, stats, steps, gr.update(maximum=steps-1, value=0)
        
        # buttons
        sort_button.click(
            fn = start_sort,
            inputs = [input_text, input_type],
            outputs = [viz_output, progress_text, statistics, total_steps, step_slider]
        )
        
        step_slider.change(
            fn = sort_and_visualize,
            inputs = [input_text, input_type, step_slider],
            outputs = [viz_output, progress_text, statistics, total_steps]
        )
        
        def prev_step(current_step):
            return max(0, current_step - 1)
        
        def next_step(current_step, total):
            return min(total - 1, current_step + 1)
        
        prev_button.click(
            fn = prev_step,
            inputs = [step_slider],
            outputs = [step_slider]
        )
        
        next_button.click(
            fn = next_step,
            inputs = [step_slider, total_steps],
            outputs = [step_slider]
        )

        gr.Markdown(
            """
            ### HOW TO USE:
            1. choose input method
            2. enter your array (comma-separated integers)
            3. click start sorting to begin visualization
            4. use controls to view steps and change visualization speed
            
            ### HOW THE ALGORITHM WORKS
            - builds a sorted array one element at a time
            - each step takes an element from the unsorted part and inserts it into the correct position in the sorted part
            - elements are shifted right to make room for the inserted value
            """
        )
    
    return demo

# handles main function
if __name__ == "__main__":
    demo = create_interface()
    demo.launch()