def is_point_inside_polygon(x, y, polygon):
    """
    Determine if the point (x, y) is inside the closed polygon.

    Args:
    x, y -- x and y coordinates of the point.
    polygon -- a list of tuples [(x1, y1), (x2, y2), ..., (xn, yn)] representing the vertices of the polygon.

    Returns:
    True if the point is inside the polygon, False otherwise.
    """

    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

import matplotlib.pyplot as plt

def plot_polygon_and_point(polygon, point, inside):
    # Unzip the polygon coordinates for plotting
    x_poly, y_poly = zip(*polygon)

    # Create a new figure
    plt.figure()

    # Plot the polygon
    plt.plot(x_poly + (x_poly[0],), y_poly + (y_poly[0],), 'b-', label='Polygon')

    # Plot the point
    point_color = 'green' if inside else 'red'
    plt.scatter(*point, color=point_color, label='Point ("Inside" if green, "Outside" if red)')

    # Set plot labels and legend
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Point in Polygon')
    plt.legend()

    # Show the plot
    plt.show()

# Example usage
polygon = [(1, 1), (5, 1), (5, 5), (1, 5)]  # A square
point = (3, 3)  # Inside the square
print(is_point_inside_polygon(point[0], point[1], polygon))  # Expected output: True

inside = is_point_inside_polygon(point[0], point[1], polygon)  # Using the previously defined function

# Plotting
plot_polygon_and_point(polygon, point, inside)