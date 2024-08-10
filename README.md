# rubiks-cube-solver
Using various algorithms to analyze and create a program that will solve a rubik's cube.

The code will give two solutions: One using Kociemba's algoritham and the other using Korf's algorithm.

The moves files for Korf's algorithm will initially download databases of moves. This is a one time thing that will happen when you run the program for the first time.

To execute simply run solve.py

The input of the Rubik's cube uses computer vision to detect colors of all 6 faces and construct the cube when all 6 faces are captured.

The cube should be in the orientation of the below image.

![image](https://github.com/user-attachments/assets/2ee81b64-a3ef-4568-858a-9e69c10dd1fa)
