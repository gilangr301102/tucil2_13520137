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
        self.bezier_curve_points = [[] for i in range(self.iteration+1)]

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
            # Read the entire file as a single string
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
    
    def generate_bezier_points_dnc(self, p1, p2, p3, curr_iteration):
        if(curr_iteration>self.iteration):
            return

        midpoint1 = self.get_midpoint(p1,p2)
        midpoint2 = self.get_midpoint(p2,p3)
        midpoint3 = self.get_midpoint(midpoint1,midpoint2)
        # print("debug midpoint")
        # print(midpoint1)
        # print(midpoint2)
        # print(midpoint3)
        # print("------------")

        self.bezier_generated_points[curr_iteration].append(p2)

        curr_iteration += 1

        self.generate_bezier_points_dnc(p1,midpoint1,midpoint3,curr_iteration)

        self.generate_bezier_points_dnc(midpoint3,midpoint2,p3,curr_iteration)

    def get_bezier_solution(self):
        num_initial_branch = self.n - 2
        for i in range(num_initial_branch):
            self.bezier_generated_points[0].append(self.initial_points[i])
            self.generate_bezier_points_dnc(self.initial_points[i], self.initial_points[i+1], self.initial_points[i+2], 0)
            self.bezier_generated_points[0].append(self.initial_points[i+2])

    def getSolution(self):

        plt.ion()

        x = []
        y = []
        for i in range(len(self.bezier_generated_points[0])):
            x.append(self.bezier_generated_points[0][i].x)
            y.append(self.bezier_generated_points[0][i].y)

        # Initialize the plot
        fig, ax = plt.subplots()
        line, = ax.plot(x, y, color="#{:06x}".format(random.randint(0, 0xFFFFFF)), label='Line')
        points, = ax.plot(x, y, 'ro', label='Points', color="#{:06x}".format(random.randint(0, 0xFFFFFF)))

        # Adding labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Line and Points Visualization')
        ax.legend()

        # Plotting the line and points step by step
        for i in range(len(x)):
            line.set_data(x[:i+1], y[:i+1])
            points.set_data(x[:i+1], y[:i+1])
            plt.pause(1.2)  # Pause for 0.1 seconds to show the step
            plt.draw()  # Update the plot

        # Turn off interactive mode
        plt.ioff()

        # Display the final plot
        plt.show()

def main():
    test = CurveBezierSol()
    test.get_bezier_solution()
    test.getSolution()

if __name__ == "__main__":
    main()