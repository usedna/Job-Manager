import json
import os.path
import sys
from client.input_control import get_path, get_par, get_coordinate


def menu():
    ops = {}
    while True:

        print("Please select the desired operations to be applied:")
        print()
        choice = input("1. Grayscale\n"
                       "2. Rotate\n"
                       "3. 3D Perspective transform\n"
                       "4. Distortion \n"
                       "5. Next step \n"
                       "6. Exit \n")
        if choice == '1':
            ops.update({'grayscale': {'parameters': {}
                                      }})
        elif choice == '2':
            angle = get_par('angle')
            ops.update({'rotate': {'parameters': {'angle': angle
                                                  }
                                   }
                        })
        elif choice == '3':
            original_edges = {'edge 1': [],
                              'edge 2': [],
                              'edge 3': [],
                              'edge 4': []
                              }
            transformed_edge = original_edges.copy()
            for i in range(4):
                original_edges['edge {}'.format(i + 1)] = get_coordinate('edge {} for '
                                                                         'original image(x y): '.format(i + 1))

            print()
            for i in range(4):
                transformed_edge['edge {}'.format(i + 1)] = get_coordinate('edge {} to '
                                                                           'transform image(x y): '.format(i + 1))

            ops.update({'transform': {'parameters': {
                'original': original_edges,
                'transform': transformed_edge
            }
            }
            })

        elif choice == '4':
            level = get_par('level')
            ops.update({'distortion': {'parameters': {
                'level': level
            }
            }
            })
        elif choice == '5':
            path = get_path()
            name = input("Please enter a name for the new image if you want: ")
            comment = input("Please enter a comment if you want: ")
            return {'image': path,
                    'name': name,
                    'comment': comment,
                    'operations': ops}

        elif choice == '6':
            sys.exit()


