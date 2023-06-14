import matplotlib.pyplot as plt
import time

# Number of points on the string
number_of_points = 50

# Point magnitude setup
point_magnitudes_current  = [0.0] * number_of_points
point_magnitudes_current[25] = 10
point_magnitudes_previous = point_magnitudes_current.copy()

# Time setup
time_current = 0
timestep_current = 0
timestep_length = 10
timestep_max = 500
timestep_duration_seconds = 0.01

# Multiplier on acceleration based on distance
spring_multiplier = 0.1

# Velocity is multiplied by this value before other calculations
velocity_multiplier = 1

# Returns a single point's new magnitude based on its velocity and the location of its neighbors
def calculate_new_point_magnitude(point_index: int) -> float:

    # Get the point's magnitude from the list
    point_magnitude = point_magnitudes_current[point_index]

    # Get the velocity of the point based on current magnitude and previous magnitude
    point_velocity = ((point_magnitudes_current[point_index] - point_magnitudes_previous[point_index]) / timestep_length) * velocity_multiplier

    # Get the total relative magnitude of all neighboring points
    total_relative_neighbor_magnitude = 0
    if 0 <= point_index-1 < len(point_magnitudes_current):
        total_relative_neighbor_magnitude += (point_magnitudes_current[point_index-1] - point_magnitude)
    if 0 <= point_index+1 < len(point_magnitudes_current):
        total_relative_neighbor_magnitude += (point_magnitudes_current[point_index+1] - point_magnitude)

    # Assign an acceleration to the point based on the relative magnitude of neighboring points
    point_acceleration = total_relative_neighbor_magnitude * spring_multiplier

    # Calculate new point velocity based on acceleration
    new_point_velocity = point_velocity + (point_acceleration / timestep_length)

    # Calculate change in magnitude for point based on velocity
    point_magnitude_delta = new_point_velocity * timestep_length

    # Calculate new magnitude based on distance based on magnitude delta
    new_current_point_magnitude = point_magnitude + point_magnitude_delta

    return new_current_point_magnitude

# Iterates the simulation by one timestep
def iterate_timestep():
    global point_magnitudes_current
    global point_magnitudes_previous

    global time_current
    global timestep_current

    # Tick the clock up
    timestep_current += 1
    time_current    += timestep_length

    # Use list comprehension to make new point magnitudes list
    point_magnitudes_new = [calculate_new_point_magnitude(point_index) for point_index, magnitude in enumerate(point_magnitudes_current)]

    # Update the other two point magnitude lists
    point_magnitudes_previous = point_magnitudes_current.copy()
    point_magnitudes_current  = point_magnitudes_new.copy()

# Function from ChatGPT to plot the values
def plot_values(values):
    # Turn on interactive mode
    plt.ion()

    # Create a list for x-axis values
    x_values = range(len(values))
    
    # Create the plot
    plt.scatter(x_values, values)
    
    # Add title and labels
    plt.title("Waves :)")
    plt.xlabel("X")
    plt.ylabel("Y")

    # Set fixed axes limits
    #plt.xlim(number_of_points)
    plt.ylim([-20, 20])
    
    # Display the plot
    plt.draw()
    plt.pause(timestep_duration_seconds)

    # Clear the plot for the next update
    plt.cla()


def main():
    while timestep_current <= timestep_max:
        # rounded_display_magnitudes = [round(magnitude) for magnitude in point_magnitudes_current]
        # print(timestep_current)
        plot_values(point_magnitudes_current)
        time.sleep(timestep_duration_seconds)
        iterate_timestep()

if __name__ == '__main__':
    main()