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
        command = self.inputCommandHandling()
        self.initial_points = []
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
        self.bezier_generated_points = [[] for i in range(self.iteration+1)]
        self.bezier_curve_points = []

    def inputCommandHandling(self):
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
        with open('../test/input.txt', 'r') as file:
            file_content = file.read().strip().split('\n')
        return file_content

    def manualInputHandling(self):
        self.n = int(input("Masukkan n: "))
        self.iteration = int(input("Masukkan jumlah iterasi: "))
        for i in range(self.n):
            x = float(input("Masukkan Px"+str(i)+": "))
            y = float(input("Masukkan Py"+str(i)+": "))
            self.initial_points.append(Point(x,y))

    def get_midpoint(self, a: Point, b: Point):
        return Point((a.x+b.x)/2,(a.y+b.y)/2)

    def get_control_point(self, points: list[Point], curr_iteration, left_branches, right_branches):
        sz_points = len(points)
        if sz_points==1:
            left_branches.append(points[0])
            right_branches.append(points[0])
            return points[0], left_branches, right_branches

        next_control_points = []
        for i in range(sz_points-1):
            midpoint = self.get_midpoint(points[i], points[i+1])
            next_control_points.append(midpoint)

        left_branches.append(next_control_points[0])
        right_branches.append(next_control_points[-1])

        return self.get_control_point(next_control_points, curr_iteration, left_branches, right_branches)

    def generate_bezier_points_dnc(self, initial_points, curr_iteration):
        if curr_iteration > self.iteration:
            return

        next_control_points, left_branches, right_branches = self.get_control_point(initial_points, curr_iteration, [initial_points[0]], [initial_points[-1]])

        right_branches = right_branches[::-1]

        sz_initial_points = len(initial_points)

        for i in range(sz_initial_points):
            self.bezier_generated_points[curr_iteration].append(initial_points[i])

        curr_iteration += 1

        self.generate_bezier_points_dnc(left_branches, curr_iteration)

        if(curr_iteration<=self.iteration):
            self.bezier_curve_points.append(next_control_points)
        
        self.generate_bezier_points_dnc(right_branches, curr_iteration)

    def get_bezier_solution(self):
        self.bezier_curve_points.append(self.initial_points[0])
        self.generate_bezier_points_dnc(self.initial_points, 0)
        self.bezier_curve_points.append(self.initial_points[self.n-1])

    def getSolution(self):
        sz_generated_points = len(self.bezier_generated_points)
        visualize_points_x = [[] for i in range(sz_generated_points+1)]
        visualize_points_y = [[] for i in range(sz_generated_points+1)]

        for i in range(sz_generated_points):
            for j in range(len(self.bezier_generated_points[i])):
                visualize_points_x[i].append(self.bezier_generated_points[i][j].x)
                visualize_points_y[i].append(self.bezier_generated_points[i][j].y)

        for i in range(len(self.bezier_curve_points)):
            visualize_points_x[sz_generated_points].append(self.bezier_curve_points[i].x)
            visualize_points_y[sz_generated_points].append(self.bezier_curve_points[i].y)

        # Initialize the plot
        fig, ax = plt.subplots()

        for i in range(sz_generated_points+1):
            line, = ax.plot(visualize_points_x[i], visualize_points_y[i])
            points, = ax.plot(visualize_points_x[i], visualize_points_y[i], 'o')

            # Randomize line and point colors
            line_color = (i==sz_generated_points and "red" or "black")
            point_color = "#{:06x}".format(random.randint(0, 0xFFFFFF), label="Point")

            # Set line and point colors
            line.set_color(line_color)
            points.set_color(point_color)
            for j in range(len(visualize_points_x[i])):
                line.set_data(visualize_points_x[i][:j+1], visualize_points_y[i][:j+1])
                points.set_data(visualize_points_x[i][:j+1], visualize_points_y[i][:j+1])
                plt.pause(0.7)
                plt.draw()  # Update the plot

        # Adding labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Line and Points Visualization')
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
    test.getSolution()

if __name__ == "__main__":
    main()