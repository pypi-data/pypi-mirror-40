#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Example code showing reflection at a glass-air interface in one dimension


import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as const
import time

import macromax
from macromax import utils
from macromax.examples import log


def show_air_glass_transition(impedance_matched=False, birefringent=False):
    wavelength = 488e-9
    angular_frequency = 2 * const.pi * const.c / wavelength
    source_amplitude = 1j * angular_frequency * const.mu_0
    p_source = np.array([0.0, 1.0, 1.0j])  # y-polarized

    # Set the sampling grid
    nb_samples = 1024
    sample_pitch = wavelength / 16
    x_range = sample_pitch * np.arange(nb_samples) - 5e-6

    # define the source
    source = -source_amplitude * sample_pitch * (np.abs(x_range) < sample_pitch/4)  # point source at 0
    source = p_source[:, np.newaxis] * source[np.newaxis, :]

    # define the medium
    epsilon_material = np.array([1.5, 1.48, 1.5]) ** 2
    has_object = (x_range >= 10e-6) & (x_range < 200e-6)
    permittivity = np.ones((1, 1, len(x_range)), dtype=np.complex64)
    # absorbing boundary
    boundary_thickness = 5e-6
    dist_in_boundary = np.maximum(0.0, np.maximum(-(x_range - (x_range[0] + boundary_thickness)),
                                                  x_range - (x_range[-1] - boundary_thickness)) / boundary_thickness)
    permittivity[:, :, :] += - 1.0 + 1.0 + (0.5j * dist_in_boundary)

    if birefringent:
        permittivity = np.eye(3)[:, :, np.newaxis] * permittivity
        for dim_idx in range(3):
            permittivity[dim_idx, dim_idx, has_object] += epsilon_material[dim_idx]
    else:
        permittivity[:, :, has_object] += epsilon_material[0]
    # permittivity = bandpass_and_remove_gain(permittivity, 2, x_range, wavelength/2)

    if impedance_matched:
        # Impedance matched everywhere
        permeability = permittivity
    else:
        # # Non-impedance matched glass
        # permeability = np.ones((1, 1, len(x_range)), dtype=np.complex64)
        # permeability[:, :, (x_range < -1e-6) | (x_range > 26e-6)] = np.exp(0.2j)  # absorbing boundary
        # permeability[:, :, (x_range >= 10e-6) & (x_range < 20e-6)] = 1.0
        # permeability = bandpass_and_remove_gain(permeability, 2, x_range)
        # No magnetic component
        permeability = 1.0  # The display function below would't expect a scalar

    # Prepare the display
    fig, ax = plt.subplots(2, 1, frameon=False, figsize=(12, 9), sharex=True)
    abs_line = ax[0].plot(x_range * 1e6, x_range * 0, color=[0, 0, 0])[0]
    poynting_line = ax[0].plot(x_range * 1e6, x_range * 0, color=[1, 0, 1])[0]
    energy_line = ax[0].plot(x_range * 1e6, x_range * 0, color=[1, 1, 0])[0]
    force_line = ax[0].plot(x_range * 1e6, x_range * 0, color=[0, 1, 1])[0]
    torque_line = ax[0].plot(x_range * 1e6, x_range * 0, color=[0.5, 0.5, 0.5])[0]
    real_line = ax[0].plot(x_range * 1e6, x_range * 0, color=[0, 0.7, 0])[0]
    imag_line = ax[0].plot(x_range * 1e6, x_range * 0, color=[1, 0, 0])[0]
    ax[0].set_xlabel("x  [$\mu$m]")
    ax[0].set_ylabel("E, S  [a.u.]")
    ax[0].set_xlim(x_range[[0, -1]] * 1e6)

    ax[1].plot(x_range[-1] * 2e6, 0, color=[0, 0, 0], label='|E|')
    ax[1].plot(x_range[-1] * 2e6, 0, color=[1, 0, 1], label='S')
    ax[1].plot(x_range[-1] * 2e6, 0, color=[0, 0.7, 0], label='$E_{real}$')
    ax[1].plot(x_range[-1] * 2e6, 0, color=[1, 0, 0], label='$E_{imag}$')
    ax[1].plot(x_range * 1e6, permittivity[0, 0].real, color=[0, 0, 1], linewidth=2.0, label='$\\epsilon_{real}$')
    ax[1].plot(x_range * 1e6, permittivity[0, 0].imag, color=[0, 0.5, 0.5], linewidth=2.0, label='$\\epsilon_{imag}$')
    if impedance_matched:
        ax[1].plot(x_range * 1e6, permeability[0, 0].real, color=[0.5, 0.25, 0], label='$\\mu_{real}$')
        ax[1].plot(x_range * 1e6, permeability[0, 0].imag, color=[0.5, 1, 0], label='$\\mu_{imag}$')
    ax[1].set_xlabel('x  [$\mu$m]')
    ax[1].set_ylabel('$\epsilon$, $\mu$')
    ax[1].set_xlim(x_range[[0, -1]] * 1e6)
    ax[1].legend(loc='upper right')

    plt.ion()

    # # Define a video writer
    # FFMpegWriter = manimation.writers['ffmpeg']
    # metadata = dict(title='air_glass_air_1D', artist='Matplotlib', comment='Movie support!')
    # writer = FFMpegWriter(fps=30, metadata=metadata)
    # with writer.saving(fig, "air_glass_air_1D.mp4"):
    #
    # Display the (intermediate) result
    #
    def display(s):
        E = s.E[1, :]
        H = s.H[2, :]
        S = s.S[0, :]
        f = s.f[0, :]
        u = s.energy_density
        torque = s.torque[0, :]
        # S = torque
        # print(np.mean(s.torque.flatten()))
        net_force = np.sum(s.f[:, has_object], axis=1) * s.sample_pitch[0]  # N m^-3 * m
        net_torque = np.sum(s.torque[:, has_object], axis=1) * s.sample_pitch[0]  # N m^-2 * m
        log.info('Net forward force on object: %0.3gpN/m^2, and torque: %0.3gx%0.3gx%0.3g fN/m.'
                 % (net_force[0] * 1e12, *(net_torque * 1e15)))
        # sigma = s.stress_tensor
        # po = macroscopicmaxwell.parallel_ops_column.ParallelOperations(3, s.shape, s.sample_pitch)
        # div_sigma = po.div(sigma)[0, 0, :]
        log.info("1D: Displaying iteration %0.0f: error %0.1f%%" % (s.iteration, 100 * s.residue))
        field_to_display = angular_frequency * E  # The source is polarized along this dimension
        max_val_to_display = np.maximum(np.max(np.abs(field_to_display)), np.finfo(field_to_display.dtype).eps)
        poynting_normalization = np.max(np.abs(S)) / max_val_to_display
        energy_normalization = np.max(np.abs(u)) / max_val_to_display
        force_normalization = np.max(np.abs(f)) / max_val_to_display
        torque_normalization = np.max(np.abs(torque)) / max_val_to_display

        abs_line.set_ydata(np.abs(field_to_display) ** 2 / max_val_to_display)
        poynting_line.set_ydata(np.real(S) / poynting_normalization)
        energy_line.set_ydata(np.real(u) / energy_normalization)
        force_line.set_ydata(np.real(f) / force_normalization)
        torque_line.set_ydata(np.real(torque) / (torque_normalization + (torque_normalization == 0)))
        real_line.set_ydata(np.real(field_to_display))
        imag_line.set_ydata(np.imag(field_to_display))
        ax[0].set_ylim(np.array((-1, 1)) * np.maximum(np.max(np.abs(field_to_display)), np.max(abs(field_to_display) ** 2 / max_val_to_display)) * 1.05 )
        figure_title = "Iteration %d, " % s.iteration
        ax[0].set_title(figure_title)

        # fig2 = plt.figure()
        # # plt.plot(x_range * 1e6, 0.5 * np.abs(E) ** 2)
        # # plt.plot(x_range * 1e6, 0.5 * np.abs(np.sqrt(const.mu_0 / const.epsilon_0) * np.abs(H)) ** 2)
        # # plt.plot(x_range * 1e6, np.sqrt(const.mu_0 / const.epsilon_0) * 0.5 * (E * np.conj(H)).real)
        #
        # plt.plot(x_range * 1e6, u)
        # # plt.plot(x_range * 1e6, f)
        # # plt.plot(x_range * 1e6, S)

        plt.pause(0.001)

        # writer.grab_frame()

    #
    # What to do after each iteration
    #
    def update_function(s):
        if np.mod(s.iteration, 100) == 0:
            log.info("Iteration %0.0f: rms error %0.1f%%" % (s.iteration, 100 * s.residue))
        if np.mod(s.iteration, 100) == 0:
            display(s)

        return s.residue > 1e-5 and s.iteration < 1e4

    # The actual work is done here:
    start_time = time.time()
    # import pyprofiler as prof
    # profiler = prof.start_profile()
    solution = macromax.solve(x_range, vacuum_wavelength=wavelength, source_distribution=source,
                              epsilon=permittivity, mu=permeability, callback=update_function
                              )
    # prof.end_profile(profiler)
    log.info("Calculation time: %0.3fs." % (time.time() - start_time))

    # Show final result
    log.info('Displaying final result.')
    display(solution)
    plt.show(block=False)


def bandpass_and_remove_gain(v, dims, ranges, periods):
    """
    Helper function to smoothen inputs to the scale of the wavelength
    :param v: the input array.
    :param dims: the dimension to smoothen
    :param ranges: the coordinate vectors of the dimensions to smoothen
    :param periods: the standard deviation(s).
    :return: The smoothened array.
    """
    if np.isscalar(dims):
        dims = [dims]
    if np.isscalar(ranges[0]):
        ranges = [ranges]
    if np.isscalar(periods):
        periods = [periods] * len(ranges)
    v_ft = np.fft.fftn(v, axes=dims)
    for dim_idx in range(v.ndim - 2):
        f_range = utils.calc_frequency_ranges(ranges[dim_idx])[0]
        lowpass_filter = np.exp(-0.5*(np.abs(f_range) * periods[dim_idx])**2)
        v_ft *= utils.to_dim(lowpass_filter, v_ft.ndim, dims[dim_idx])
    v = np.fft.ifftn(v_ft, axes=dims)
    v[v.imag < 0] = v.real[v.imag < 0]  # remove and gain (may be introduced by rounding errors)
    return v


if __name__ == "__main__":
    start_time = time.time()
    show_air_glass_transition(impedance_matched=False, birefringent=False)
    # show_air_glass_transition(impedance_matched=True, birefringent=False)
    log.info("Total time: %0.3fs." % (time.time() - start_time))
    plt.show(block=True)
