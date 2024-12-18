
import pygame


def make_imlist(spritesheet, nims, vertical=False):
    # makes list from a spritesheet with nims images
    spritesheet = pygame.image.load(spritesheet)

    imlist = []

    if vertical:
        size = (spritesheet.get_width(),
                spritesheet.get_height() // nims)
        for row in range(nims):
            patch = pygame.Rect((0, size[1] * row), size)
            imlist.append(spritesheet.subsurface(patch))
    else:
        size = (spritesheet.get_width() // nims,
                spritesheet.get_height())
        for column in range(nims):
            patch = pygame.Rect((size[0] * column, 0), size)
            imlist.append(spritesheet.subsurface(patch))

    return imlist


def make_immat(spritesheet, nrows, ncols, vertical=False):
    # makes matrix from a spritesheet with nrows x ncols images
    spritesheet = pygame.image.load(spritesheet)

    size = (spritesheet.get_width() // ncols,
            spritesheet.get_height() // nrows)

    if not vertical:
        immat = [[] for i in range(nrows)]
        for row in range(nrows):
            for column in range(ncols):
                patch = pygame.Rect((size[0] * column, size[1] * row), size)
                immat[row].append(spritesheet.subsurface(patch))
    else:
        immat = [[] for i in range(ncols)]
        for column in range(ncols):
            for row in range(nrows):
                patch = pygame.Rect((size[0] * column, size[1] * row), size)
                immat[column].append(spritesheet.subsurface(patch))
    return immat


def im_resize_list(im, initial_size, final_size, steps):
    # makes a list of steps images
    # by resizing im from initial_size to final_size
    im = pygame.image.load(im)
    imlist = []
    step = ((final_size[0]-initial_size[0])/(steps-1),
            (final_size[1]-initial_size[1])/(steps-1))
    for i in range(steps):
        w = round(initial_size[0]+i*step[0])
        h = round(initial_size[1]+i*step[1])
        imlist.append(pygame.transform.scale(im, (w, h)))

    return imlist
