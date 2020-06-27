# stl_builder

This program creates an STL file of a surface based on the inputs provided in a config file. The output is an stl file of a surface that is described by evaluating a user supplied formula at various values of X and Y, and drawing triangular facets between the points.

Some sample surfaces I've made:

![](https://github.com/mikeabuilder/stl_maker/blob/master/Pictures/half-donut.jpg)



The program launches from the command line:

     MAIN_program.py

There are two  command line parameters

-h    prints this file

-f <inputfile>   REQUIRED PARAMETER. path to  the JSON file with the user  inputs.



 There are two sample files included in the 'main' directory:

​                 input.json 
​                 input_my_module.json

User inputs  in the JSON file are fully described in the "comments" in the example files:
  - Min and Max X (the surface is evaluated in a rectangle bounded by these values)

  - Number of steps between min and max in each direction (if the resulting surface is too rough, increasing the number of steps can improve this.

  - Output file type: text or binary (binary is a much smaller file)

  - Output file name: I'll add ".stl" to the end.

  - Output file directory

  - A python statement that will return a variable z, based on inputs x and y.

    

## About those two sample input files...


**input.JSON**
   Many interesting surfaces can be described by a simple equation, like "z=math.sin(x) * math.sin(y)".  A short equation like this can can easily be fit into the JSON file without it becoming cumbersome. And this is the easiest way to begin using this program.

**input_my_module.json**
Many interesting surfaces can require multiple lines of code to describe. For these situations, I recommend usinng two python statements in the JSON file, and this file is a sample of this.  The first line is an "import"  statement that points to a python module you would write yourself.  The  second statement is a call to a function in that module that returns a value  for z. Then, in the module, you can write as much python code as you need  to  come up with your z values. When your function is called by the  main_program, the values of x and y can be supplied (if you have this in    your function's input list)

 In the sample JSON, a module called 'my_complex_formula.py' is imported,    and a function in that file called 'return_my_z' is executed to get the z    value. If you look in my_complex_formula.py, you'll see that it is intended    to be used for equations that use polar coordinates (r, theta). Youll see a    conversion of x and y into polar coordinates, and several different    sample equations for z. ALl but one have been commented out.  Some are    simple one-liners, and some are more complex. You can change which one is    not commented out to see some shapes I created.  Note that if you leave    multiple equations not commneted out, then the last one that executes will    be the z value used. 

   Some of these "equations" can take a few lines of code to create, and one I    put in (called 'coiled snake') is fairly complex. And that's the point -    you can do some odd and complex things with this method.

   You can even pass new values from the input file to your module easily. All    of the contents of the json file are in a dictionary called    config["user_input_file"]. if you pass 'config' as an input to the function    you write, you can easily get any new values you put in the input file. 

## A few other things:

1. If the JSON input file has any JSON syntax errors, the error printed by this program should help you get close to the location of the error.
2. To run this program, you will need a couple of additional python modules beyond the default stuff. In particular, you will need

3. bitstring  ("pip install bitstring" from a command window)
   numpy ("pip install numpy" from a command window)
4. To look at the surfaces you create, you'll need to use a tool that can read and display surfaces in stl files. Some may not liek binary format, others may not like text format. I've opened all the surfaces created in my sample files using Fusion 360, and most using PrusaSlicer. 
5. Have FUN!
6. Lastly - I built this program using a "program stub" that I've evolved for myself and use whenever I write a new program. It's way more complex than   needed for this particular program. If you decide to try to read through my   code, I hope the comments will help you out.  
7. And one beyond lastly - I wrote and tested this in windows. It should work in other OS's but I have not tested it. If you run under linux, watch the path in the sample input files for the dreaded windows drive letter. 