#Embraer 175 Dictionary
Embraer_Wings_Dict = dict({
    'b_wing' : [93 + 11/12,"ft"],     #ft!
    'S_wing' : [783,"ft2"],            #ft^2!
    'S_wet' : [1313.9,"ft2"],         #ft^2*
    'S_exposed' : [690.56,"ft2"],      #ft^2*
    'quarterchord_sweep' : [22.86, "deg"], #deg*
    'c_root' : [16.24, 'ft'],          #ft*
    'c_tip' : [4.31, 'ft'],            #ft*
    'alpha_c_root' : 3,        #deg*
    'alpha_c_tip' : -3,        #deg*
    'c_joint' : [10.41, "ft"],         #ft*
    'y_joint' : [10.41, "ft"],         #ft*
    'ydiff' : [36.31, "ft"],           #|ytip-yroot| in ft*
    'tc_MAX' : 13.46/100,      #*
    'tc_avg' : 9.33/100,       #*
    'tc_maxtip' : 9/100,       #*
    'xc_tc_MAX' : .4,          #*
    'c_tip_wingtip' : [1.65, "ft"],    #ft
    'S_wingtip' : [65, "ft2"],          #ft^2*
    'tapratio_wingtip' : .1,   #*
    'cpr/c' : .3,              #*
    'S_flapped' : [151.86, "ft2"],      #ft^2
    'dCldalpha' : [0.114, "invdeg"],       #1/deg (dC_l/d(alpha))
    'r_LE' : [0.21, "ft"],             #ft*
    'h_wing_AVE' : [8.32, "ft"],       #ft*
    'CL_0' : .5,              #* coeff when alpha=0
})

Embraer_HorizontalStabilizer_Dict = dict({
    'b_h' : [32.75, "ft"],             #ft!
    'S_h' : [250 + 37/144, "ft2"],      #ft^2!
    'S_exposed_h' : [212.14, "ft2"],    #ft^2
    'quarterchord_sweep_h' : [30.5, "deg"],#deg*
    'c_root_h' : [10.0, "ft"],         #ft*
    'c_tip_h' : [3.8, "ft"],           #ft
    'tc_MAX_h' : 8/100,        #*
    'tc_avg_h' : 5.33/100,     #*
    'xc_tc_MAX_h' : 35/100,    #*
})

Embraer_VerticalStabilizer_Dict = dict({
    'b_v' : [18.17, "ft"],             #ft*
    'S_v' : [174 + 55/144, "ft2"],      #ft^2!
    'S_wet_v' : [391.10, "ft"],        #ft*... how was this found?
    'S_exposed_v' : [195.09, "ft"],    #ft*
    'c_average_v' : [14.17, "ft"],     #ft*
    'quarterchord_sweep_v' : 38.76, #deg*
    'c_root_v' : [20.46, "ft"],        #ft*
    'c_tip_v' : [4.48, "ft"],          #ft 
    'tc_MAX_v' : 8/100,        #*
    'tc_avg_v' : 5.33/100,     #*
    'xc_tc_MAX_v' : 35/100,    #* 
})

Embraer_Pylons_Dict = dict({
    'l_p' : [4.6, "ft"],               #ft*
    'c' : [8, "ft"],                   #ft
    't_p' : [0.4, "ft"],                #ft*
    'S_wet_p' : [49.33, "ft2"],          #ft^2*
    'S_exposed_p' : [24.63, "ft2"],      #ft^2*
})

Embraer_Fuselage_Dict = dict({
    'l_f' : [103 + 11/12, "ft"],       #ft!
    'd_f' : [10.69, "ft"],             #ft*
    'd_base_f' : [1.28, "ft"],         #ft*
    'S_wet_f' : [3024.6, "ft2"],        #ft^2*
    'S_plan_f' : [805.64, "ft2"],       #ft^2*
    'S_front_f' : [106.42, "ft2"],      #ft^2*
    'S_base_f' : [1.29, "ft2"],         #ft^2*
    'S_front_gear' : [32.86, "ft2"],    #ft^2*
})

Embraer_Nacelles_Dict = dict({
    'l_n' : [13.11, "ft"],             #ft*
    'd_n' : [5.43, "ft"],              #ft*
    't_n' : [3.38, "ft"],              #ft*
    'S_plan_n' : [50.08, "ft2"],        #ft^2*
    'S_front_n' : [22.64, "ft2"],       #ft^2*
})

Embraer_Performance_Dict = dict({
    'MaxMach' : 0.82,           #Mach
    'MGTOW' : [85517, 'lbf'],            #lbf
    'MGLW' : [74957, 'lbf'],             #lbf
    'BasicOp' : [48250, 'lbf'],          #lbf
    'MaxZeroFuel' : [69887, 'lbf'],      #lbf
    'MaximumPay' : [21636, 'lbf'],       #lbf
    'MaxFuel' : [6.7*3071, 'lbf'],       #lbf
    'MaxCruise' : 0.82,         #Mach
    'ServiceCeiling' : [41000, 'ft'],   #ft

})
# !!!!!! Flight_Data_ERJ_175 from matlab
Embraer175_Dict = dict({
    "Name" : "ERJ_175",
    "Wings" : Embraer_Wings_Dict,
    "Horizontal_Stabilizer" : Embraer_HorizontalStabilizer_Dict,
    "Vertical_Stabilizer" : Embraer_VerticalStabilizer_Dict,
    "Pylons" : Embraer_Pylons_Dict,
    "Fuselage" : Embraer_Fuselage_Dict,
    "Nacelles" : Embraer_Nacelles_Dict,
    "Performance" : Embraer_Performance_Dict
})