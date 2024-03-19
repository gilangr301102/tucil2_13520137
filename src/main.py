from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

@dataclass
class Point:
    x: int
    y: int

class CurveBezierSol():
    def __init__(self):
        # Initialize the input values
        self.initial_points = []
        print("Silahkan Pilih Algoritma yang ingin dicoba: ")
        print("1. Brute Force")
        print("2. Divide and Conquer")
        self.algoritma = str(input("Pilih Algoritma [1,2]: "))
        if(self.algoritma=="1"):
            print("Menggunakan Algoritma Brute Force")
            self.manualInputHandling()
        else:
            print("Menggunakan Algoritma Divide and Conquer")
            command = self.inputCommandHandling()
            if(command=="2"):
                file_content = self.fileInputHandling()

                # Extract values from the input string
                self.n = int(file_content[0])  # n is the first line
                x_values = list(map(float, file_content[1].split()))
                y_values = list(map(float, file_content[2].split()))
                self.iteration = int(file_content[3])
                for i in range(self.n):
                    self.initial_points.append(Point(x_values[i], y_values[i]))
                # Print the extracted values
                print("N:", self.n)
                print("Points:", self.initial_points)
                print("Iteration:", self.iteration)
            else:
                self.manualInputHandling()
            self.is_visualize = str(input("Apakah ingin melihat proses visualisasi? [y/n]: "))
        self.bezier_generated_points = [[] for i in range(self.iteration+1)]
        self.bezier_curve_points = [[] for i in range(self.iteration+1)]

    def inputCommandHandling(self):
        # Get the input command from the user
        print("Input Options: ")
        print("1. Manual input")
        print("2. File input")
        command = str(input("Please choose format input file [1,2]: "))
        while(command != "1" and command != "2"):
            print("Unknown Input Command, please try again!")
            print("Input Options: ")
            print("1. Manual input")
            print("2. File input")
            command = str(input("Please choose format input file [1,2]: "))
        return command

    def fileInputHandling(self):
        # Read the file input
        with open('../test/input.txt', 'r') as file:
            file_content = file.read().strip().split('\n')
        return file_content

    def manualInputHandling(self):
        # Get the input from the user
        self.n = int(input("Masukkan n: "))
        self.iteration = int(input("Masukkan jumlah iterasi: "))
        for i in range(self.n):
            x = float(input("Masukkan Px"+str(i)+": "))
            y = float(input("Masukkan Py"+str(i)+": "))
            self.initial_points.append(Point(x,y))

    def get_midpoint(self, a: Point, b: Point):
        # Get the midpoint of two points
        return Point((a.x+b.x)/2,(a.y+b.y)/2)
    
    def generate_bezier_points_brute_force(self, initial_points, curr_iteration):
        for i in range(curr_iteration):
            temp_points = []
            for j in range(len(initial_points)-1):
                temp_points.append(self.get_midpoint(initial_points[j], initial_points[j+1]))
            initial_points = temp_points
        return initial_points


    def get_control_point(self, points: list[Point], curr_iteration, left_branches, right_branches):
        sz_points = len(points)
        if sz_points==1: # If left and right branches are empty, then it is the base case with only one point
            return points[0], left_branches, right_branches

        # Get all midpoints from current control points
        next_control_points = []
        for i in range(sz_points-1):
            midpoint = self.get_midpoint(points[i], points[i+1])
            next_control_points.append(midpoint)

        # Divide the control points into left and right branches
        left_branches.append(next_control_points[0])
        right_branches.append(next_control_points[-1])

        # Recursively call the function to get the next control points
        return self.get_control_point(next_control_points, curr_iteration, left_branches, right_branches)

    def generate_bezier_points_dnc(self, initial_points, curr_iteration):
        # Base case if the current iteration is greater than the maximum iteration ()
        if curr_iteration > self.iteration:
            return

        # Get the next control points and left and right branches
        next_control_point, left_branches, right_branches = self.get_control_point(initial_points, curr_iteration, [initial_points[0]], [initial_points[-1]])

        # Reverse the right branches
        right_branches = right_branches[::-1]

        # Get the size of the initial points
        sz_initial_points = len(initial_points)

        # Append the initial points to the bezier generated points
        for i in range(sz_initial_points):
            self.bezier_generated_points[curr_iteration].append(initial_points[i])

        # Append the next control points to the bezier generated points in the next iteration
        curr_iteration += 1
        
        # Recursively left branches to get the next control points on the left
        self.generate_bezier_points_dnc(left_branches, curr_iteration)

        # Append next control points on the bezier curve points
        if(curr_iteration<=self.iteration):
            for i in range(curr_iteration, self.iteration+1):
                self.bezier_curve_points[i].append(next_control_point)
        
        # Recursively right branches to get the next control points on the right
        self.generate_bezier_points_dnc(right_branches, curr_iteration)

    def get_bezier_solution(self):
        if(self.algoritma=="1"):
            print(self.generate_bezier_points_brute_force())
        else:
            # Append the initial points to the bezier curve points
            for i in range(self.iteration+1):
                self.bezier_curve_points[i].append(self.initial_points[0])

            # Generate the bezier points using divide and conquer
            self.generate_bezier_points_dnc(self.initial_points, 0)

            # Append the last points to the bezier curve points
            for i in range(self.iteration+1):
                self.bezier_curve_points[i].append(self.initial_points[-1])

    def visualize_all(self):
        # Visualize the bezier generated points and bezier curve points
        # sz_generated_points = len(self.bezier_generated_points)
        visualize_points_x = []
        visualize_points_y = []

        if(self.algoritma=="1"):
            temp_x = []
            temp_y = []
            for j in range(len(self.bezier_curve_points[-1])):
                temp_x.append(self.bezier_curve_points[-1][j].x)
                temp_y.append(self.bezier_curve_points[-1][j].y)
            visualize_points_x.append(temp_x)
            visualize_points_y.append(temp_y)
        else:
            if self.is_visualize == "y":
                for i in range(self.iteration+1):
                    temp_x = []
                    temp_y = []
                    for j in range(len(self.bezier_generated_points[i])):
                        temp_x.append(self.bezier_generated_points[i][j].x)
                        temp_y.append(self.bezier_generated_points[i][j].y)
                    visualize_points_x.append(temp_x)
                    visualize_points_y.append(temp_y)
                    temp_x = []
                    temp_y = []
                    for j in range(len(self.bezier_curve_points[i])):
                        temp_x.append(self.bezier_curve_points[i][j].x)
                        temp_y.append(self.bezier_curve_points[i][j].y)
                    visualize_points_x.append(temp_x)
                    visualize_points_y.append(temp_y)
            else:
                temp_x = []
                temp_y = []
                for j in range(len(self.bezier_curve_points[-1])):
                    temp_x.append(self.bezier_curve_points[-1][j].x)
                    temp_y.append(self.bezier_curve_points[-1][j].y)
                visualize_points_x.append(temp_x)
                visualize_points_y.append(temp_y)
                        # Initialize the plot
        fig, ax = plt.subplots()
        length_visualize_points = len(visualize_points_x)
        for i in range(length_visualize_points):
            line, = ax.plot(visualize_points_x[i], visualize_points_y[i])
            points, = ax.plot(visualize_points_x[i], visualize_points_y[i], 'o')

            # Randomize line and point colors
            line_color = ((i%2==1 or self.is_visualize=='n') and "#{:06x}".format(random.randint(0, 0xFFFFFF), label="Point") or "black")
            point_color = "#{:06x}".format(random.randint(0, 0xFFFFFF), label="Point")

            # Set line and point colors
            line.set_color(line_color)
            points.set_color(point_color)
            for j in range(len(visualize_points_x[i])):
                line.set_data(visualize_points_x[i][:j+1], visualize_points_y[i][:j+1])
                points.set_data(visualize_points_x[i][:j+1], visualize_points_y[i][:j+1])
                plt.pause(0.4)
                plt.draw()  # Update the plot
        # Adding labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Bezier Curve Visualization')
        ax.legend()

        # Turn off interactive mode
        plt.ioff()

        # Display the final plot
        plt.show()
        # Turn on interactive mode
        plt.ion()

def main():
    test = CurveBezierSol()
    test.get_bezier_solution()
    test.visualize_all()

if __name__ == "__main__":
    main()