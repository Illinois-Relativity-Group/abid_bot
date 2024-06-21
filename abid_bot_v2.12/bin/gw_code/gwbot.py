import sys, os
from params_gw import params_gw


class GWBot:
    def __init__(self, params_gw):
        self.unpack_generalGWSettings(params_gw[0])
        self.unpack_psi4Settings(params_gw[1])
        self.unpack_gridSettings(params_gw[2])
        self.unpack_simulationSettings(params_gw[3])
        self.unpack_testGWSettings(params_gw[4])

    def unpack_generalGWSettings(self, generalGWSettings):
        self.root, self.test_flag, self.update_lookup, self.files_per_folder, \
            self.threeD_flag, self.all_times, self.start_time, self.end_time \
            = generalGWSettings
    def unpack_psi4Settings(self, psi4Settings):
        self.psi4_dir, self.psi4_num, self.psi4_f, \
            self.psi4_f_sorted, self.bin_dir \
            = psi4Settings
    def unpack_gridSettings(self, gridSettings):
        self.xy_max_3D, self.xy_num_3D, self.z_min_3D, self.z_max_3D, self.z_num_3D, \
            self.xy_max_2D, self.xy_num_2D, self.phi_1D, self.theta_1D, \
            self.choose_plane, self.plane_norm \
            = gridSettings
    def unpack_simulationSettings(self, simulationSettings):
        self.M_ADM, self.cutoff_w, self.r_areal, self.gw_dt, self.num_modes, \
            self.num_times, self.plot_all_modes, self.modes_to_plot \
            = simulationSettings
    def unpack_testGWSettings(self, testGWSettings):
        self.test_num_times, self.test_dt, self.test_kind, \
            self.test_R, self.test_M, self.test_Om \
            = testGWSettings

    def __str__(self):
        return f'root (str):      {self.root}\ntest_flag (bool):        {self.test_flag}\nM_ADM (float):        {self.M_ADM}'


gw = GWBot(params_gw)