import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
import matplotlib.ticker as ticker


def get_gif(input_path, output_file, duration=250):
    """ Generates a gif from images in input_path that change at a given time interval """
    # Assertions
    if not os.path.exists(input_path):
        raise OSError('Path does not exist: ' + input_path)
    if not os.path.isdir(input_path):
        raise OSError('input_path must be a directory: ' + input_path)
    if not os.listdir(input_path):
        raise OSError('Directory is empty: ' + input_path)

    # TODO
    file_names = os.listdir(input_path)
    file_names.sort(key=lambda x: int(x.split('.')[0][3:]))
    images = []
    for file_name in file_names:
        images.append(imageio.v3.imread(input_path + '/' + file_name))
    imageio.mimsave(output_file, images, duration=duration)


def visualize_solution(steps, output_path):
    """ Generates a set of images (png) for every np.array in steps and saves them in output_path """
    # Assertions
    if not os.path.exists(output_path):
        raise OSError('Path does not exist: ' + output_path)
    if not os.path.isdir(output_path):
        raise OSError('input_path must be a directory: ' + output_path)

    letters = 'abcdefjhijklmnopqrstuvwxyz'
    for step, board in enumerate(steps):
        size = board.shape[0]
        fig, ax = plt.subplots()
        ax.imshow(board, cmap='binary')
        # Mark positions where queens are met
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                if board[i][j] == 1:
                    ax.text(j, i, '♛', ha='center', va='center', color='white', fontsize=30)

        ax.set_xticks(np.arange(0, size, 1))
        ax.set_xticklabels(range(1, size + 1))
        ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(0.5, size + .5, 1)))

        ax.set_yticks(np.arange(0, size, 1))
        ax.set_yticklabels(list(letters[:size]))
        ax.yaxis.set_minor_locator(ticker.FixedLocator(np.arange(0.5, size + .5, 1)))

        ax.tick_params(which='both', bottom=False, left=False)
        ax.grid(visible=True, which='minor', color='black')
        ax.set_title(f'Step: {step+1}')

        fig.savefig(output_path + '/' + f'img{step + 1}.png', dpi=150)
        plt.close(fig)


if __name__ == '__main__':
    from nqueens import NQueens

    task = NQueens(8)
    task.solve()
    solution = task.first_solution

    path = 'solution_imgs'
    gif = 'solution.gif'
    if os.path.exists(path):
        for file in os.listdir(path):
            os.remove(path + '/' + file)
    else:
        os.mkdir(path)

    if os.path.exists(gif):
        os.remove(gif)

    visualize_solution(solution, path)
    get_gif(path, gif)

    for file in os.listdir(path):
        os.remove(path + '/' + file)
    os.rmdir(path)

