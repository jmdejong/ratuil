# RATUIL

Responsive Ansicode Terminal User Interface Library

Ratuil a a Terminal UI library that was made for games that have the screen divided in multiple sections, and should support different (and changing) terminal sizes.
Another important feature is that the layout of the UI is generated from an XML file.

Ratuil was originally created with [Asciifarm](https://github.com/jmdejong/asciifarm) in mind.

<!-- There is currently no documentation yet. Take a look at game.xml and game.py to see how to use Ratuil. -->

## Example

This is an example layout:

    <?xml version="1.0"?>
    <hbox>
        <vbox width="20" align="right">
            <bar id="health" height="1" full-char="+" empty-char="-" full-style="fg:7; bg:2" empty-style="fg:7; bg: 1;" total="10" filled="8"></bar>
            <switchbox id="menus" selected="equipment" height="50%">
                <border key="inventory">
                    <listing id="inventory">
                        milk
                        eggs
                        bread
                    </listing>
                </border>
                <border char="#" key="equipment">
                    <listing id="equipment">
                        cotton underwear
                        cotton shirt
                        jeans
                        friendship bracelet
                    </listing>
                </border>
            </switchbox>
            <border char=" ">
                <textbox id="info" wrap="words">
    This is a great place to show some information.
    Textbox lines can be wrapped!
                </textbox>
            </border>
        </vbox>
        <fill width="1" align="right" style="fg:12;bg:4">
            @
        </fill>
        <vbox>
            <hbox align="bottom" height="1">
                <textbox width="2">&gt;</textbox>
                <textinput id="input"></textinput>
            </hbox>
            <log id="messages" align="bottom" height="20%%">
                Welcome to [game]
            </log>
            <border>
                <overlay>
                    <field id="field" char-size="2"></field>
                    <border offset-x="2" align="right" width="13" offset-y="1" height="3" style="reverse">
                        <textbox>hello world</textbox>
                    </border>
                </overlay>
            </border>
        </vbox>
    </hbox>

On a 80x20 screen it will show this output (but then with colours):

    +---------------------------------------------------------+@++++++++++++++++----
    |                                                         |@####################
    |                                          +-----------+  |@#*cotton underwear #
    |                                          |hello world|  |@# cotton shirt     #
    |                                          +-----------+  |@# jeans            #
    |                                                         |@# friendship bracel#
    |                                                         |@#                  #
    |                                                         |@#                  #
    |                                                         |@#                  #
    |                                                         |@#                  #
    |                                                         |@####################
    |                                                         |@                    
    |                                                         |@ This is a great    
    |                                                         |@ place to show some 
    |                                                         |@ information.       
    +---------------------------------------------------------+@ Textbox lines can  
                                                               @ be wrapped!        
                                                               @                    
    Welcome to [game]                                          @                    
    >                                                          @                    

The values of several elements can be changed from code.

## Global Attributes

As seen in the text, the elements can have several attributes.
Some of these are global.

- id: An identifier string to get this element. In the code you can get access to this element using Layout.get(id). This is the only way to access an element from code. If an element has an id this id should be unique.
- key: This is also an identifier, but is only needed to distinguish elements from their siblings. Currently this is only used for children of switchbox or overlay elements.
- offset-x, offset-y, width, height, align: These are the style attributes. They are used to position elements withing the parent attributes. Currently this is only used for children of hbox, vbox and overlay elements
  - width and height: the width and height of the element. If no width or height is given the element will cover the total available space.
  - min-width, min-height, max-width, max-height: minimum and maximum values for the sizes.
  - align: whether to align to left, right, top or bottom. Since top-left alignment is the default, only "right" and "bottom" will actually do something. The string can be a combination, for example "right;bottom".
    I will probably change the way this works a bit, and split it into align-hor and align-vert or something like that.
  - offset-x and offset-y: The values between the side of this element and the end of the available size. This is currently only used by children of overlay.
    If alignment is topleft (the default) these sizes are the distance between the start of the available area and the beginning of the element. If the alignment is bottom right these sizes are the distance between the end of the element and the end of the available area.
    If no offset is given it will be 0.
  
  The values for width, height, offset-x and offset-y can be absolute values, relative values or very relative values:
  - Absolute: The number of characters. This is just an integer without any suffix. Examples: "10", "0", "3"
  - Relative: The size relative to the size of the parent. This can be denoted by a real number followed by a "/" or "%". If the "%" sign is used the value is multiplied by 100 before multiplying by the size. Examples: "0.5/", "25%", "1/", "33.3%", "0.22/", "22%". The strings "0.22/" and "22%" denote the same value.
  - Very relative: The size relative to the available size after the previous siblings have taken their cut. This is the real available size. This is only used in children of hbox and vbox, otherwise this is treated as a regular relative size. This is denoted by having "//" or "%%" at the end. For the rest it works the same as relative. Examples: "0.5//", "100%%", "0.6//", "60%%". The strings "0.6//" and "60%%" denote the same value.
- hidden: The element and its children will not be drawn. Their update method will never be invoked.

## Elements

### charbox



### textbox

The most basic element for showing text.
It will show its given text (either in the xml or with the `set_text(text)` method) in the area that it has.

The 'wrap' attribute deals how overflow is handled.
By default, or if the value is "crop" the overflow is cropped.
If the value is "words" then the overflow is wrapped on whitespace (using `textwrap.wrap`).


### hbox

Draw its children horizontally next to each other. The order of the children is the order of priority. If the earlier children take up all much space the later children may not be draw

### vbox

Similar to hbox but vertically.

### switchbox

Only draws one of its children at a time. It is possible to pick from code which child is drawn using the `select(identifier)` method. Children can be selected by their index (starting at 0) or by their key if they have one.

### listing

A list of several strings (one on each line) of a certain item can be selected. If the list is longer than the available height, it will center on the selected item.

### border

Draw a border around its child. Can only have one child

### fill

Fill all available area with a pattern (or a single character).
This could also be used to make a separator line within an hbox or vbox.

### etc...

## Installing

    git clone https://github.com/jmdejong/ratuil.git
    pip3 install -e ratuil/ --user

## Usage

	# pick one of these 3 import for a screen
	# curses is recommended: it is the lightest and most efficient
	#from ratuil.bufferedscreen import Screen
	#from ratuil.ansiscreen import Screen
	from ratuil.cursedscreen import Screen
	
	from ratuil.layout import Layout
	
	screen = BufferedScreen() // Make the screen
	
	try:
		# always initialize the terminal before trying to do something with the screen 
		screen.initialize_terminal()
		
		screen.clear()

		layout = Layout.from_xml_file(screen, "layout.xml") // Load the layout from xml. This assumes that there is the file "layout.xml" in the current directory
		
		layout.update() // Draw the layout to the buffered screen
		screen.update() // Draw the buffer to the terminal
		
		// change something:
		log = layout.get("messages") // get the element with id "messages". For this example this is a log element.
		log.add_message("hello world") // add a new message to the log
		
		// draw again
		layout.update()
		screen.update()
	finally:
		# Always finalize the terminal.
		# This should be done from a finally block whose try block encompasses all usage of screen.
		# Failure to call this can leave the terminal in a weird state (no echoing, no cursor etc.)
		screen.finalize_terminal()

## Considerations

Currently an element has the attributes for both the styling relative to its parent, and for its own parameters.
It might be better to separate it.
Options are including an in-between element for these styling things (which makes it more verbose) or putting the syling into a single attribute (just like css).
I don't like either solution.
