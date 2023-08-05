#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Example code showing scalar light propagation.


import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as const
import time

import macromax
from macromax import utils
from macromax.examples import log


def show_scatterer():
    #
    # Medium settings
    #
    data_shape = np.array([128, 256]) * 2
    wavelength = 500e-9
    boundary_thickness = 3e-6
    beam_diameter = 5e-6
    k0 = 2 * np.pi / wavelength
    angular_frequency = const.c * k0
    source_amplitude = 1j * angular_frequency * const.mu_0
    sample_pitch = np.array([1, 1]) * wavelength / 8
    ranges = utils.calc_ranges(data_shape, sample_pitch)
    incident_angle = 0 * np.pi / 180

    def rot_Z(a): return np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    incident_k = rot_Z(incident_angle) * k0 @ np.array([0, 1, 0])
    source = -source_amplitude * np.exp(1j * (incident_k[0]*ranges[0][:, np.newaxis] + incident_k[1]*ranges[1][np.newaxis, :]))
    # Aperture the incoming beam
    source = source * np.exp(-0.5*(np.abs(ranges[1][np.newaxis, :] - (ranges[1][0]+boundary_thickness))/wavelength)**2)
    source = source * np.exp(-0.5*((ranges[0][:, np.newaxis] - ranges[0][int(len(ranges[0])*1/2)])/(beam_diameter/2))**2)
    source = source[np.newaxis, ...]

    permittivity = np.ones((1, 1, *data_shape), dtype=np.complex128)
    # Add scatterer
    epsilon_crystal = 1.5
    R = np.sqrt(ranges[0][:, np.newaxis]**2 + ranges[1][np.newaxis, :]**2)
    permittivity[0, 0][R < 0.5*np.min(data_shape * sample_pitch)/2] = epsilon_crystal

    # Add boundary
    dist_in_boundary = np.maximum(
        np.maximum(0.0, -(ranges[0][:, np.newaxis] - (ranges[0][0]+boundary_thickness)))
        + np.maximum(0.0, ranges[0][:, np.newaxis] - (ranges[0][-1]-boundary_thickness)),
        np.maximum(0.0,-(ranges[1][np.newaxis, :] - (ranges[1][0]+boundary_thickness)))
        + np.maximum(0.0, ranges[1][np.newaxis, :] - (ranges[1][-1]-boundary_thickness))
    )
    weight_boundary = dist_in_boundary / boundary_thickness
    permittivity[0, 0, :, :] += -1.0 + (1.0 + 0.2j * weight_boundary)  # boundary

    # Prepare the display
    fig, axs = plt.subplots(1, 2, frameon=False, figsize=(12, 9))
    for ax in axs.ravel():
        ax.set_xlabel('y [$\mu$m]')
        ax.set_ylabel('x [$\mu$m]')
        ax.set_aspect('equal')

    images = axs[0].imshow(utils.complex2RGB(np.zeros(data_shape), 1),
                                     extent=np.array([*ranges[1][(0, -1),], *ranges[0][(0, -1), ]]) * 1e6)
    axs[1].imshow(utils.complex2RGB(permittivity[0, 0], 1),
                     extent=np.array([*ranges[1][[0, -1]], *ranges[0][[0, -1]]]) * 1e6)
    axs[1].set_title('$\chi$')
    plt.ion()

    #
    # Display the current solution
    #
    def display(s):
        log.info("2D: Displaying iteration %d: error %0.1f%%" % (s.iteration, 100 * s.residue))
        images.set_data(utils.complex2RGB(s.E[0], 1))
        figure_title = '$E' + "$ it %d: rms error %0.1f%% " % (s.iteration, 100 * s.residue)
        axs[0].set_title(figure_title)

        plt.draw()
        plt.pause(0.001)

    #
    # Display the (intermediate) result
    #
    def update_function(s):
        if np.mod(s.iteration, 10) == 0:
            log.info("Iteration %0.0f: rms error %0.1f%%" % (s.iteration, 100 * s.residue))
        if np.mod(s.iteration, 10) == 0:
            display(s)

        return s.residue > 1e-3 and s.iteration < 1e4

    # The actual work is done here:
    start_time = time.time()
    solution = macromax.solve(ranges, vacuum_wavelength=wavelength, source_distribution=source,
                              epsilon=permittivity, callback=update_function
                              )
    log.info("Calculation time: %0.3fs." % (time.time() - start_time))


    # Show final result
    log.info('Displaying final result.')
    display(solution)
    plt.show(block=True)


if __name__ == "__main__":
    start_time = time.time()
    show_scatterer()
    log.info("Total time: %0.3fs." % (time.time() - start_time))
