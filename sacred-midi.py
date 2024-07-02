import matplotlib.pyplot as plt
import numpy as np
import mido
from mido import MidiFile, MidiTrack, Message

def draw_circle(center, radius):
    return plt.Circle(center, radius, edgecolor='black', facecolor='none')

def draw_line(ax, point1, point2):
    ax.plot([point1[0], point2[0]], [point1[1], point2[1]], color='black')

def flower_of_life(radius, depth):
    centers = [(0, 0)]
    directions = [(np.cos(np.pi/3 * i), np.sin(np.pi/3 * i)) for i in range(6)]
    for _ in range(depth):
        new_centers = []
        for center in centers:
            for direction in directions:
                new_center = (center[0] + radius * direction[0], center[1] + radius * direction[1])
                if new_center not in centers:
                    new_centers.append(new_center)
        centers.extend(new_centers)
    return centers

def metatrons_cube(radius, depth):
    centers = flower_of_life(radius, depth)
    # Add the central circle
    centers.append((0, 0))
    return centers

def seed_of_life(radius):
    centers = [(0, 0)]
    directions = [(np.cos(np.pi/3 * i), np.sin(np.pi/3 * i)) for i in range(6)]
    for direction in directions:
        new_center = (radius * direction[0], radius * direction[1])
        centers.append(new_center)
    return centers

def vesica_piscis(radius):
    centers = [(0, 0), (radius, 0)]
    return centers

def scale_mapping(pitch, scale):
    scale_notes = {
        'C_major': [0, 2, 4, 5, 7, 9, 11, 12],
        'C_minor': [0, 2, 3, 5, 7, 8, 10, 12],
        'D_major': [2, 4, 6, 7, 9, 11, 13, 14],
        'D_minor': [2, 4, 5, 7, 9, 10, 12, 14],
        'E_major': [4, 6, 8, 9, 11, 13, 15, 16],
        'E_minor': [4, 6, 7, 9, 11, 12, 14, 16],
        'F_major': [5, 7, 9, 10, 12, 14, 16, 17],
        'F_minor': [5, 7, 8, 10, 12, 13, 15, 17],
        'G_major': [7, 9, 11, 12, 14, 16, 18, 19],
        'G_minor': [7, 9, 10, 12, 14, 15, 17, 19],
        'A_major': [9, 11, 13, 14, 16, 18, 20, 21],
        'A_minor': [9, 11, 12, 14, 16, 17, 19, 21],
        'B_major': [11, 13, 15, 16, 18, 20, 22, 23],
        'B_minor': [11, 13, 14, 16, 18, 19, 21, 23]
    }
    notes_in_scale = scale_notes[scale]
    octave = pitch // 12
    note_in_octave = pitch % 12
    closest_note = min(notes_in_scale, key=lambda x: abs(x - note_in_octave))
    return 12 * octave + closest_note

def map_to_midi(centers, min_pitch=60, max_pitch=72, min_duration=200, max_duration=600, scale='C_major'):
    x_values = [c[0] for c in centers]
    y_values = [c[1] for c in centers]
    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)
    
    midi_notes = []
    for center in centers:
        x, y = center
        pitch = int(np.interp(x, [min_x, max_x], [min_pitch, max_pitch]))
        octave_offset = (np.abs(center[0] + center[1]) % 2) * 12  # Octave variation
        pitch += octave_offset
        pitch = scale_mapping(pitch, scale)
        duration = int(np.interp(y, [min_y, max_y], [min_duration, max_duration]))
        velocity = int(np.interp(y, [min_y, max_y], [40, 127]))  # Dynamic range
        midi_notes.append((pitch, duration, velocity))
    return midi_notes

def create_midi(midi_notes, filename='output.mid'):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    for note, duration, velocity in midi_notes:
        track.append(Message('note_on', note=int(note), velocity=int(velocity), time=0))
        track.append(Message('note_off', note=int(note), velocity=int(velocity), time=int(duration)))
    
    mid.save(filename)

def generate_midi(pattern, radius, depth, filename, scale):
    if pattern == 'flower_of_life':
        centers = flower_of_life(radius, depth)
    elif pattern == 'metatrons_cube':
        centers = metatrons_cube(radius, depth)
    elif pattern == 'seed_of_life':
        centers = seed_of_life(radius)
    elif pattern == 'vesica_piscis':
        centers = vesica_piscis(radius)
    else:
        raise ValueError("Unsupported pattern")
    
    midi_notes = map_to_midi(centers, scale=scale)
    create_midi(midi_notes, filename)

# Example usage
generate_midi('metatrons_cube', radius=1, depth=3, filename='metatrons_cube_A_minor.mid', scale='A_minor')

# Visualization
centers = metatrons_cube(radius=1, depth=3)
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
for center in centers:
    circle = draw_circle(center, 1)
    ax.add_artist(circle)

# Draw lines to form Metatron's Cube
for i, center1 in enumerate(centers):
    for center2 in centers[i+1:]:
        draw_line(ax, center1, center2)

plt.show()

