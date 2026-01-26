import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def plot_sphere(ax, center, radius, color): # Function to plot a sphere for planets
    u = np.linspace(0, 2 * np.pi, 30)  # Reduced resolution
    v = np.linspace(0, np.pi, 30)
    u, v = np.meshgrid(u, v)
    x = center[0] + radius * np.cos(u) * np.sin(v)
    y = center[1] + radius * np.sin(u) * np.sin(v)
    z = center[2] + radius * np.cos(v)
    ax.plot_surface(x, y, z, color=color, alpha=1.0, edgecolor='none')

# the dictionary data contains all of our data!
data = { # 'planet': [semi-major axis {a}, eccentricity {e}, inclination {i}, longitude of ascending node {omega}, color in RGB format, radius in km {r}]
    'Mercury': [0.39, 0.206, 7.0, 48.3, (0.6, 0.6, 0.5), 2439.7],
    'Venus': [0.72, 0.007, 3.4, 76.7, (0.9, 0.9, 0.5), 6051.8],
    'Earth': [1.0, 0.017, 0.0, 0.0, (0.3, 0.6, 0.4), 6371.0],
    'Mars': [1.52, 0.093, 1.85, 49.6, (0.8, 0.3, 0.1), 3389.5],
    'Jupiter': [5.20, 0.048, 1.3, 100.5, (0.9, 0.5, 0.2), 69911],
    'Saturn': [9.58, 0.056, 2.5, 113.7, (0.9, 0.7, 0.3), 58232],
    'Uranus': [19.18, 0.046, 0.8, 74.0, (0.4, 0.8, 0.8), 25362],
    'Neptune': [30.07, 0.009, 1.8, 131.8, (0.2, 0.4, 0.8), 24622],
}

# this section adds dwarfs (and asteroids) to the dictionary. Disable it at necessity. 
# Yes, Pluto is not a planet!
other_solar_objects = { # 'dwarf planet': [semi-major axis {a}, eccentricity {e}, inclination {i}, longitude of ascending node {omega}, color in RGB format]
    'Ceres': [2.77, 0.076, 10.6, 80.3, (0.6, 0.5, 0.4), 473], # Ceres is a dwarf planet located in the asteroid belt between Mars and Jupiter.
    'Pluto': [39.48, 0.249, 17.1, 110.3, (0.8, 0.6, 0.4), 1188.3], # Pluto is a dwarf planet located in the Kuiper belt. It may be called a TNO
    'Eris': [67.78, 0.441, 44.0, 35.9, (0.5, 0.5, 0.9), 1163], # Eris is a dwarf planet located in the scattered disc region of the Kuiper belt.
    'Haumea': [43.13, 0.195, 28.2, 121.8, (0.9, 0.9, 1.0), 816], # Haumea is a dwarf planet located in the Kuiper belt. It is known for its elongated shape and fast rotation.
    'Vesta': [2.36, 0.089, 7.1, 103.9, (0.7, 0.6, 0.5), 262.7], # Vesta is a large asteroid located in the asteroid belt. It is one of the largest asteroids in the solar system.
    'Sedna': [506.8, 0.849, 11.9, 144.5, (0.9, 0.4, 0.4), 500] # Sedna is a real TNO (very large orbit), TNO=trans-Neptunian object. It is the only TNO I will use
}
data.update(other_solar_objects)


#next section adds Moon. Disable it at necessity.
moon_data = {
    'Moon': [0.00257, 0.0549, 5.145, 125.08, (0.5, 0.5, 0.6), 1737.4]
    }

# I want to make a 3d plot, which is the only reason i needed longitude of ascending node {omega} and inclination {i}. All others are just 2d parametrics

t = np.linspace(0, 2 * np.pi, 1000)  #time projection for plotting one ellipsoid orbit
t_current = datetime.now()  # current time (for planetary positions)
t_delta = (datetime.now() - datetime(2000, 1, 1)).days / 365.25 # reference time frame

fig = plt.figure(figsize=(10, 10))
fig.subplots_adjust(left=0.7)
ax = fig.add_subplot(111, projection='3d')

ax.plot([], [], label="Orbits are ellipses, located in three dimensions.", alpha=0) # intr0
ax.plot([], [], label="Current planetary positions are marked with a transparent sphere.", alpha=0)
ax.plot([], [], label="Real planets are hidden there as well (though yo uneed to squeeze in to see them.", alpha=0) # intr0
ax.plot([], [], label=" ", alpha=0) # empty plot for legend spacing

s_sun = 696340 / 149597870.7 # Sun's radius in AU (1 AU = 149597870.7 km)
ax.scatter([0], [0], [0], color='yellow', s=50, label='Sun', marker='*') # Sun label and transparent sphere
plot_sphere(ax, [0, 0, 0], s_sun, "yellow") # Sun's sphere
ax.plot([], [], label=" ", alpha=0) # empty plot for legend spacing

for i in data:  # plotting each planet through data dictionary
    #print(i, ":", data[i], sep ='')
    a = data[i][0]  # semi-major axis {a}
    e = data[i][1]  # eccentricity {e}
    inc = np.radians(data[i][2])  # inclination {i} [radians]
    omega = np.radians(data[i][3])  # longitude of ascending node {omega} [radians]
    b = a * ((1 - e**2)**0.5)  # semi-minor axis {b}

    x_t = a * np.cos(t) * np.cos(omega) - b * np.sin(t) * np.sin(omega) * np.cos(inc) # all x points for current planet
    y_t = a * np.cos(t) * np.sin(omega) + b * np.sin(t) * np.cos(omega) * np.cos(inc)  # all y points for current planet
    z_t = b * np.sin(t) * np.sin(inc)  # all z points for current planet

    # plotting the orbit of the current planet
    if i not in other_solar_objects: ax.plot(x_t, y_t, z_t, color=data[i][4], label=f"{i}")
    else: ax.plot(x_t, y_t, z_t, color=data[i][4], linestyle='dashed', alpha=0.3, label=f"{i}")

    # now for the current position of the planet
    T = a ** 1.5 # Super fun Kepler's third law
    theta = 2 * np.pi * (t_delta/T) % (2 * np.pi) # super UNfunny parametric angle for current position

    x_pos = a * np.cos(theta) * np.cos(omega) - b * np.sin(theta) * np.sin(omega) * np.cos(inc) # current x coordinate
    y_pos = a * np.cos(theta) * np.sin(omega) + b * np.sin(theta) * np.cos(omega) * np.cos(inc) # current y coordinate
    z_pos = b * np.sin(theta) * np.sin(inc) # current z coordinate

    # plotting the current position of the current planet
    ax.scatter([x_pos], [y_pos], [z_pos], color=data[i][4], s=50, marker="+")
    plot_sphere(ax, [x_pos, y_pos, z_pos], data[i][5] / 149597870.7, data[i][4]) # plotting the sphere of the current planet
    if i == 'Neptune': ax.plot([], [], label=" ", alpha=0) # empty plot for legend spacing
    if i == 'Sedna': ax.plot([], [], label=" ", alpha=0) # empty plot for legend spacing

    # here we add the moon to the Earth
    if i == 'Earth':
        a_m = moon_data['Moon'][0] # a
        e_m = moon_data['Moon'][1] # e
        inc_m = np.radians(moon_data['Moon'][2]) # i
        omega_m = np.radians(moon_data['Moon'][3]) # omega
        b_m = a_m * ((1 - e_m**2)**0.5) # b

        # we need to transform to Sun's reference frame

        x_m = x_pos + a_m * np.cos(t) * np.cos(omega_m) - b_m * np.sin(t) * np.sin(omega_m) * np.cos(inc_m) # current x coordinate of the moon in Sun's reference frame
        y_m = y_pos + a_m * np.cos(t) * np.sin(omega_m) + b_m * np.sin(t) * np.cos(omega_m) * np.cos(inc_m) # current y coordinate of the moon in Sun's reference frame
        z_m = z_pos + b_m * np.sin(t) * np.sin(inc_m) # current z coordinate of the moon in Sun's reference frame

        ax.plot(x_m, y_m, z_m, color=moon_data['Moon'][4], label="Moon") # plotting the orbit of the moon

        x_pos_m = x_pos + a_m * np.cos(theta) * np.cos(omega_m) - b_m * np.sin(theta) * np.sin(omega_m) * np.cos(inc_m) # current x coordinate of the moon in Sun's reference frame
        y_pos_m = y_pos + a_m * np.cos(theta) * np.sin(omega_m) + b_m * np.sin(theta) * np.cos(omega_m) * np.cos(inc_m) # current y coordinate of the moon in Sun's reference frame
        z_pos_m = z_pos + b_m * np.sin(theta) * np.sin(inc_m) # current z coordinate of the moon in Sun's reference frame

        ax.scatter([x_pos_m], [y_pos_m], [z_pos_m], color=moon_data['Moon'][4], s=20, marker='+') # plotting the current position of the moon
        plot_sphere(ax, [x_pos_m, y_pos_m, z_pos_m], moon_data['Moon'][5] / 149597870.7, moon_data['Moon'][4]) # plotting the sphere of the current moon



# Now to approximate asteroid scatter without unnecessary complexity and precision

N = 1000 # number of random point-like asteroids code will generate (idea is creating a point-like swarm that eventually forms a 3d torus, no orbtis though)
# the higher the N, the more computational power the code would require

# first, the Asteroid belt 
a_a = np.random.uniform(2.1, 3.2, N) # a
e_a = np.random.uniform(0, 0.35, N) # eccentricities
b_a = a_a * ((1 - e_a**2)**0.5) # b
inc_a = np.radians(np.random.uniform(0, 10, N)) # inclination
omega_a = np.radians(np.random.uniform(0, 360, N)) # longitude of ascending node
t_a = np.random.uniform(0, 2 * np.pi, N) # t

x_a = a_a * np.cos(t_a) * np.cos(omega_a) - a_a * np.sqrt(1 - e_a**2) * np.sin(t_a) * np.sin(omega_a) * np.cos(inc_a)
y_a = a_a * np.cos(t_a) * np.sin(omega_a) + a_a * np.sqrt(1 - e_a**2) * np.sin(t_a) * np.cos(omega_a) * np.cos(inc_a)
z_a = a_a * np.sqrt(1 - e_a**2) * np.sin(t_a) * np.sin(inc_a)

ax.scatter(x_a, y_a, z_a, color='gray', s=1, alpha = 0.4, label='Asteroid Belt')


# second, the Kuiper belt 
a_k = np.random.uniform(30, 50, N) # a
e_k = np.random.uniform(0, 0.2, N) # eccentricity
b_k = a_k * ((1 - e_k**2)**0.5) # b
inc_k = np.radians(np.random.uniform(0, 15, N)) # inclination
omega_k = np.radians(np.random.uniform(0, 360, N)) # longitude of ascending node
t_k = np.random.uniform(0, 2 * np.pi, N) # t

x_k = a_k * np.cos(t_k) * np.cos(omega_k) - a_k * np.sqrt(1 - e_k**2) * np.sin(t_k) * np.sin(omega_k) * np.cos(inc_k)
y_k = a_k * np.cos(t_k) * np.sin(omega_k) + a_k * np.sqrt(1 - e_k**2) * np.sin(t_k) * np.cos(omega_k) * np.cos(inc_k)
z_k = a_k * np.sqrt(1 - e_k**2) * np.sin(t_k) * np.sin(inc_k)

ax.scatter(x_k, y_k, z_k, color='gray', s=1, alpha=0.4, label='Kuiper Belt')


ax.set_xlabel('x (au)')
ax.set_ylabel('y (au)')
ax.set_zlabel('z (au)')

plt.title('Solar System Model')

max_range = 100  # Focus on Neptune's orbit for easiness of coordinating one's view across our beautiful solar system. A little bit further for TNOs
# You can navigate the view by using inbuilt tools, so it would be wise to start from afar
ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)
ax.set_zlim(-max_range, max_range)
ax.set_box_aspect([1, 1, 1])

# Adjust legend
plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), fontsize=8)
plt.tight_layout()

plt.show()
