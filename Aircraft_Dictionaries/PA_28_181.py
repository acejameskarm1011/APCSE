#PA28
PA_28_181_wings_dict = dict({
    'S_wing' : [171.8, "ft2"],
    'b_wing' : [35.5,'ft'],
})

PA_28_181_HorizontalStabilizer_dict = dict({
    'b_h' : [12 + 10.48/12,'ft']
})

PA_28_181_VerticalStabilizer_dict = dict({
})

PA_28_181_Fuselage_dict = dict({
    'l_f' : [24,'ft']
})

PA_28_181_Performance_dict = dict({
    "MGTOW" : [2550., "lbf"],
    "MaxFuel" : [48*6., 'lbf'],
    "GlideSpeed" : [76., "knots"],
    "BestClimbSpeed" : [76., "knots"],
    "RotationSpeed" : [66., "knots"],
    "ServiceCeiling" : [13240., "ft"]
})

PA_28_181_Dict = dict({
    "Name" : "PA_28_181",
    "Wings" : PA_28_181_wings_dict,
    "Horizontal_Stabilizer" : PA_28_181_HorizontalStabilizer_dict,
    "Vertical_Stabilizer" : PA_28_181_VerticalStabilizer_dict,
    "Fuselage" : PA_28_181_Fuselage_dict,
    "Performance" : PA_28_181_Performance_dict
})
