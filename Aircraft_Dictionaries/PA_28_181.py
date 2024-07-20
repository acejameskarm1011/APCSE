#PA28
from numpy import pi
PA_28_181_wings_dict = dict({
    "S_wing" : [171.8, "ft2"],
    "b_wing" : [35.5, "ft"],
    "S_wet" : [362.34, "ft2"],
    "c_bar" : [4.829, "ft"],
    "L_c_4_wing" : [5.25, "deg"],
    "tc_avg" : [0.124, "None"],
    "tc_max_loc" : [0.141, "None"],
    "tc_max" : [0.104, "None"],
    "c_tip" : [3.5, "ft"],
    "c_root" : [6 + (1/6), "ft"],
    "C_l_alpha" : [0.11031, "None"],
    "C_l_0" : [0.347, "None"],
    "rle" : [0.07217848, "None"]
})

PA_28_181_HorizontalStabilizer_dict = dict({
    "b_h" : [12 + 10.48/12,"ft"],
    "c_root_h" : [16.858332177318598 - 14.28583225600806, "ft"],
    "c_tip_h" : [16.858332177318598 - 14.28583225600806, "ft"],
    "L_c_4_h" : [0, "deg"],
    "S_h" : [(16.858332177318598 - 14.28583225600806)*12.9791667, "ft2"],
    "tc_max_h" : [0.06530633636363636, "None"],
    "tc_avg_h" : [0.1200344, "None"],
    "S_h_wet" : [68.08541736959069, "ft2"] ,
    "tc_max_loc_h" : [0.3003177, "None"]
})

PA_28_181_VerticalStabilizer_dict = dict({
    "V_stab_area" : [11.08438, "ft2"], 
    "S_v_wet" : [25.682414101748073, "ft2"],
    "tc_max_v" : [0.06530633636363636, "None"],
    "tc_avg_v" : [0.1200344, "None"],
    "tc_max_loc_v" : [0.3003177, "None"],
    "L_c_4_v" : [34.56949355, "deg"],
    "c_tip_v" : [1.707, "ft"],
    "c_root_v" : [3.858, "ft"],
    "b_v" : [4.0425, "ft"]
})

PA_28_181_Fuselage_dict = dict({
    "l_fus" : [16.8,"ft"],
    #H_fus_max = 3.75 #ft
    #H_fus_min =
    #W_fus = 3.5 #ft
    "S_fus_wet" : [(14427.8139+48.3790)/12/12*2, "ft2"],
    "d_fus" : [3.761694981/2+4.267672038/2, "ft"],
    "S_fus_maxfront" : [7.24534170483938*2, "ft2"],
    "S_fus_plan" : [31.2239431980914*2, "ft2"],
    "d_fus_b" : [1.25, "ft"],
})

PA_28_181_Performance_dict = dict({
    "ServiceCeiling" : [13240., "ft"]
})

PA_28_181_Mass_dict = dict({
    "MGTOW" : [2550., "lbf"],
    "MaxFuel" : [48*6., "lbf"],
    "EmptyMass" : [1600, "lbf"],
    "EmptyMass_Arm" : [87.5, "in"],
    "FrontSeat_Arm" : [80.5, "in"],
    "RearSeat_Arm" : [118.1, "in"],
    "Fuel_Arm" : [95, "in"],
    "Baggage_Arm" : [142.8, "in"]
})

PA_28_181_VSpeed_dict = dict({
    "GlideSpeed" : [76., "knots"],
    "BestClimbSpeed" : [76., "knots"],
    "RotationSpeed" : [66., "knots"],
    "NeverExceedSpeed" : [182., "knots"]
})

PA_28_181_Dict = dict({
    "Name" : "PA_28_181",
    "Wings" : PA_28_181_wings_dict,
    "Horizontal_Stabilizer" : PA_28_181_HorizontalStabilizer_dict,
    "Vertical_Stabilizer" : PA_28_181_VerticalStabilizer_dict,
    "Fuselage" : PA_28_181_Fuselage_dict,
    "Performance" : PA_28_181_Performance_dict,
    "VSpeed" : PA_28_181_VSpeed_dict,
    "Mass" : PA_28_181_Mass_dict
})