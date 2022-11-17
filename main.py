import matplotlib.pyplot as plt
import numpy as np

figure, axes = plt.subplots()
axes.set_aspect(1)
plt.axis([-20, 20, -20, 20])

# holds all of the vertices and faces for all objects
all_obj_vert = []
all_obj_faces = []

def coord_to_xyz(all_coords):
    list_of_dic = []
    for i in all_obj_vert:
        xyz = {'x': i[0], 'y': i[1], 'z': i[2]}
        list_of_dic.append(xyz)
    return list_of_dic

def reverse_coord_to_xyz(all_coords):
    new_list = []
    for i in all_coords:
        each_line = []
        resultList = list(i.items())
        for j in resultList:
            each_line.append(j[1])
        #print(each_line)
        new_list.append(each_line)
    return new_list

def matrices(axis, angle):
    if axis == 'x':
        matrix = [[1, 0, 0], [0, np.cos(np.radians(angle)), -1 * np.sin(np.radians(angle))],
              [0, np.sin(np.radians(angle)), np.cos(np.radians(angle))]]
    elif axis == 'y':
        matrix = [[np.cos(np.radians(angle)), 0, np.sin(np.radians(angle))], [0, 1, 0],
              [- np.sin(np.radians(angle)), 0, np.cos(np.radians(angle))]]
    elif axis =='z':
        matrix = [[np.cos(np.radians(angle)), -1 * np.sin(np.radians(angle)), 0],
              [np.sin(np.radians(angle)), np.cos(np.radians(angle)), 0], [0, 0, 1]]
    return matrix

def rot_each_coords(loc, glob, angle, matrix):
    rotd_coords = []
    for i in range(len(matrix)):
        rotd_coords.append(np.inner(matrix[i], loc))
    return rotd_coords


def rot_whole_line(coords, glob, angle, axis):
    list_of_coords = []
    for i in range(len(coords)):
        new_coords = conversion(
           (coords[i]), glob, angle, matrices(axis, angle))
        list_of_coords.append(new_coords)
    return list_of_coords


def conversion(coord, glob, angle, matrices):
    list = [coord['x'], coord['y'], coord['z']]
    list_coord = rot_each_coords(list, glob, angle, matrices)
    return {'x': list_coord[0], 'y': list_coord[1], 'z': list_coord[2]}


def plot_plane(center_vector, x_angle, y_angle, z_angle, rotation_sequence):
    objects = [
        "toy_plane_body.obj",
        "toy_plane_left_front_wheel.obj",
        "toy_plane_right_front_wheel.obj",
        "toy_plane_left_back_wheel.obj",
        "toy_plane_right_back_wheel.obj",
        "toy_plane_propeller.obj"
    ]
    for obj in objects:# Import the OBJ
        file = open(obj)

        # Fills the list to become 2d matrices (list of lists) of point vectors and coord lists
        list_of_lines = file.readlines()

        for line in list_of_lines:
            if line[0] == 'v' and line[1] is not 'n':
                #print(line)
                line_v = line.strip('v \n')
                #print(line_v)
                pnt_vect = line_v.split(' ')

                for index, str in enumerate(pnt_vect):
                    pnt_vect[index] = float(str)
                all_obj_vert.append(pnt_vect)
            elif line[0] == 'v':
                #print(line)
                line_v = line.strip('vn \n')
                #print(line_v)
                pnt_vect = line_v.split(' ')

                for index, str in enumerate(pnt_vect):
                    pnt_vect[index] = float(str)
                all_obj_vert.append(pnt_vect)


            # Creates the face list
            elif line[0] == 'f':
                line_f = line.strip('f \n')
                face = line_f.split(' ')
                for index, str_num in enumerate(face):
                    dash = face[index].find('/')
                    face[index] = int(face[index][0:dash])-1
                all_obj_faces.append(face)
        rotatePart(center_vector, x_angle, y_angle, z_angle, rotation_sequence)



def plot_plane_single(center_vector, angle, axis):
    objects = [
        "toy_plane_body.obj",
        "toy_plane_left_front_wheel.obj",
        "toy_plane_right_front_wheel.obj",
        "toy_plane_left_back_wheel.obj",
        "toy_plane_right_back_wheel.obj",
        "toy_plane_propeller.obj"
    ]
    for obj in objects:# Import the OBJ
        file = open(obj)

        # Fills the list to become 2d matrices (list of lists) of point vectors and coord lists
        list_of_lines = file.readlines()

        for line in list_of_lines:
            if line[0] == 'v' and line[1] is not 'n':
                #print(line)
                line_v = line.strip('v \n')
                #print(line_v)
                pnt_vect = line_v.split(' ')

                for index, str in enumerate(pnt_vect):
                    pnt_vect[index] = float(str)
                all_obj_vert.append(pnt_vect)
            elif line[0] == 'v':
                #print(line)
                line_v = line.strip('vn \n')
                #print(line_v)
                pnt_vect = line_v.split(' ')

                for index, str in enumerate(pnt_vect):
                    pnt_vect[index] = float(str)
                all_obj_vert.append(pnt_vect)


            # Creates the face list
            elif line[0] == 'f':
                line_f = line.strip('f \n')
                face = line_f.split(' ')
                for index, str_num in enumerate(face):
                    dash = face[index].find('/')
                    face[index] = int(face[index][0:dash])-1
                all_obj_faces.append(face)
        if axis =='x':
            rotatePart(center_vector, angle, 0, 0, 'x')
        elif axis == 'y':
            rotatePart(center_vector, 0, angle, 0, 'y')
        elif axis == 'z':
            rotatePart(center_vector, 0, 0, z_angle, 'z')


def rotatePart(center_vector, x_angle, y_angle, z_angle, rotation_sequence):
    if rotation_sequence == 'RxRyRz':
        rotd_coordinates = rot_whole_line(coord_to_xyz(all_obj_vert), center_vector, x_angle, 'x')
        rotd_coordinates = rot_whole_line(rotd_coordinates, center_vector, y_angle, 'y')
        rotd_verts =  reverse_coord_to_xyz(rot_whole_line(rotd_coordinates, center_vector, z_angle, 'z'))
        plot_shape(rotd_verts)

    elif rotation_sequence == 'RyRxRz':
        rotd_coordinates = rot_whole_line(coord_to_xyz(all_obj_vert), center_vector, y_angle, 'y')
        rotd_coordinates = rot_whole_line(rotd_coordinates, center_vector, x_angle, 'x')
        rotd_verts = reverse_coord_to_xyz(rot_whole_line(rotd_coordinates, center_vector, z_angle, 'z'))
        plot_shape(rotd_verts)

    elif rotation_sequence == 'RzRyRx':
        rotd_coordinates = rot_whole_line(coord_to_xyz(all_obj_vert), center_vector, z_angle, 'z')
        rotd_coordinates = rot_whole_line(rotd_coordinates, center_vector, y_angle, 'y')
        rotd_verts = reverse_coord_to_xyz(rot_whole_line(rotd_coordinates, center_vector, x_angle, 'x'))
        plot_shape(rotd_verts)

    elif rotation_sequence == 'RzRxRy':
        rotd_coordinates = rot_whole_line(coord_to_xyz(all_obj_vert), center_vector, z_angle, 'z')
        rotd_coordinates = rot_whole_line(rotd_coordinates, center_vector, x_angle, 'x')
        rotd_verts = reverse_coord_to_xyz(rot_whole_line(rotd_coordinates, center_vector, y_angle, 'y'))
        plot_shape(rotd_verts)

    elif rotation_sequence == 'RxRzRy':
        rotd_coordinates = rot_whole_line(coord_to_xyz(all_obj_vert), center_vector, x_angle, 'x')
        rotd_coordinates = rot_whole_line(rotd_coordinates, center_vector, z_angle, 'z')
        rotd_verts = reverse_coord_to_xyz(rot_whole_line(rotd_coordinates, center_vector, y_angle, 'y'))
        plot_shape(rotd_verts)
    elif rotation_sequence == 'RyRzRx':
        rotd_coordinates = rot_whole_line(coord_to_xyz(all_obj_vert), center_vector, y_angle, 'y')
        rotd_coordinates = rot_whole_line(rotd_coordinates, center_vector, z_angle, 'z')
        rotd_verts = reverse_coord_to_xyz(rot_whole_line(rotd_coordinates, center_vector, x_angle, 'x'))
        plot_shape(rotd_verts)
    elif rotation_sequence == 'x':
        rotd_verts = reverse_coord_to_xyz(rot_whole_line(coord_to_xyz(all_obj_vert), center_vector, x_angle, 'x'))
        plot_shape(rotd_verts)
    elif rotation_sequence == 'y':
        rotd_verts = reverse_coord_to_xyz(rot_whole_line(coord_to_xyz(all_obj_vert), center_vector, y_angle, 'y'))
        plot_shape(rotd_verts)
    elif rotation_sequence == 'z':
        rotd_verts = reverse_coord_to_xyz(rot_whole_line(coord_to_xyz(all_obj_vert), center_vector, z_angle, 'z'))
        plot_shape(rotd_verts)
    else:
        print('The rotation sequence is invalid.')
        sys.exit()


def plot_shape(vert):

    # GRID SETUP FOR SEQUENTIAL COMBINED ROTATIONS
    # Loop to plot all tris
    for face in all_obj_faces:
        # plt.plot([0,1],[0,1], color='k')
        # vertex 0 to 1
        plt.plot([vert[face[0]][0], vert[face[1]][0]],
                 [vert[face[0]][1], vert[face[1]][1]],
                 color='k')
        # vertex 1 to 2
        plt.plot([vert[face[1]][0], vert[face[2]][0]],
                 [vert[face[1]][1], vert[face[2]][1]],
                 color='k')
        # vertex 2 to 0
        plt.plot([vert[face[2]][0], vert[face[0]][0]],
                 [vert[face[2]][1], vert[face[0]][1]],
                 color='k')

    all_obj_vert.clear()
    all_obj_faces.clear()




def main():
    # for three rotations, plot_plane([center_vector], x_angle, y_angle, z_angle, 'rotation')
    plot_plane([0, 0, 0], 30, 40, 50, 'RyRxRz')

    # for single rotation, plot_plane_single([center_vector], angle, 'axis')
    # ex) plot_plane_single([center_vector], 30, 'x')
    # plot_plane_single([5,5,5], 30, 'x')
    

    plt.show()





main()
