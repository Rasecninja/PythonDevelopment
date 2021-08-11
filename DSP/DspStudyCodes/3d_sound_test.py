#################################################################################
#                                                                               #
#                         3D sound tests code                                   #
#                                                                               #
#################################################################################

################# Imports #########################
import math
import numpy as np
import scipy.io.wavfile as wav
import sys

#Importing files from different directory
sys.path.append('../Libraries')

from real_time_dsp import *
from progress_bar import *

####################### Variables ############################
#Sample frequency of the original wav file
fs=48000
#Frame counter
frame=0
#Total number of frames
total_frames=33437*4
#Check for effects loop
effect_frame=0

####### EQ curves in dB based on tests with audio interface ########
# Left front speaker position (DC and Nyquist value copied from close bin since waveshop doesnt provide them)
leftfront_eq_curve_left=[-8.799554999999998,-8.799554999999998, -6.947512000000003, -5.730532000000004, -4.2785359999999955, -3.641641, -3.792837000000006, -3.200928999999995, -0.6439590000000024, 0.6742630000000034, 0.7650469999999991, 0.7234029999999976, 0.1751080000000016, -0.8179799999999986, -1.6031909999999954, -2.662034999999996, -3.5441219999999944, -3.282245000000003, -1.9612380000000016, -0.5483880000000028, 1.2755309999999973, 2.7445509999999977, 3.7836300000000023, 4.1260200000000005, 4.233187999999998, 3.7468990000000026, 2.831592999999998, 2.0243560000000045, 1.3282120000000042, 0.9774470000000015, 0.2734910000000035, -0.250081999999999, -0.6297289999999975, -1.0385220000000004, -1.422893000000002, -2.0511470000000003, -2.217808000000005, -1.7691090000000003, -1.2399389999999997, -0.9053840000000051, -0.17593300000000056, 0.5370529999999967, 0.34888199999999614, -0.5432770000000033, -1.170694999999995, -1.6956849999999974, -2.4239159999999984, -3.4444350000000057, -4.202206000000004, -4.975824000000003, -6.0285730000000015, -6.939925000000002, -7.573097000000004, -7.465704000000002, -6.8845639999999975, -6.103014000000002, -5.533428000000001, -4.9402550000000005, -3.8645720000000026, -2.650976, -1.899605000000001, -1.328916999999997, -1.877521999999999, -3.264551999999995, -4.140442, -4.2067479999999975, -3.077708000000001, -0.9071449999999999, 1.4054450000000038, 3.614309999999996, 5.440090999999999, 6.678215999999999, 7.376063000000002, 7.051971999999996, 6.410627999999999, 5.464990999999998, 4.566913, 4.352509000000001, 4.174066, 3.785111999999998, 2.6743319999999997, 1.3378079999999954, 0.12222200000000072, -1.1630970000000005, -1.867444000000006, -2.256883000000002, -2.135795999999999, -1.9050259999999994, -2.6446439999999996, -4.374046, -4.6993909999999985, -0.3288919999999962, 3.6703930000000042, 6.017275999999999, 6.440737999999996, 5.229366000000002, 2.453154999999999, -1.5298330000000036, -2.761291, -0.8229139999999973, 0.41589199999999593, 0.6125280000000011, -0.2735490000000027, -1.9275360000000035, -4.130293999999999, -6.516232000000002, -8.666942999999996, -9.069066999999997, -7.671471000000004, -6.3662279999999996, -5.689854000000004, -5.784205, -5.881025000000001, -5.533616000000002, -4.310613999999994, -3.5798169999999985, -3.0313990000000004, -3.276643, -4.3973219999999955, -6.5638780000000025, -9.484966, -12.071315999999996, -13.635451999999994, -14.859569999999998, -15.558717000000001, -15.911744999999996, -16.265417999999997, -16.311805999999997,-16.311805999999997] 
leftfront_eq_curve_right=[-9.675719,-9.675719, -8.247025, -7.940268000000003, -7.529722, -8.271715, -10.412291000000003, -12.973217999999996, -12.345751999999997, -9.912906999999997, -9.252572, -8.756964000000004, -8.567649000000003, -8.384104, -7.451878999999998, -7.780805999999998, -8.487777999999999, -9.189765000000001, -9.703600000000002, -11.096283, -12.153078, -12.282415, -11.455204000000002, -10.264035, -9.179359000000005, -8.538691, -8.504619000000005, -8.774034, -9.145854999999997, -9.458708000000001, -10.805948999999998, -12.123836999999995, -13.348258999999999, -14.728211000000002, -15.934255, -17.185887, -18.101037000000005, -18.470049000000003, -18.361570999999998, -18.011698000000003, -17.230795, -16.297709000000005, -16.426643000000006, -17.814676, -18.887414999999997, -19.463836, -19.974875000000004, -20.898349000000003, -21.334290000000003, -21.480373, -21.961527000000004, -22.291142, -22.577813000000006, -22.299582, -22.049476, -22.031234000000005, -21.897629000000002, -20.263723999999996, -18.134164, -15.976318, -14.319217000000002, -12.511994999999999, -11.873981, -13.065928, -16.73847, -23.728887999999998, -25.253548000000002, -20.299363999999997, -16.867844999999996, -14.515039000000002, -12.504095999999997, -11.039625000000001, -9.430042999999998, -8.406303000000001, -7.691124000000002, -7.672238, -8.213346000000001, -8.567, -9.017665999999998, -9.347169000000001, -10.512194999999998, -11.990963, -13.645674, -15.730658000000005, -17.235961000000003, -18.104107, -18.025827999999997, -16.996776000000004, -15.960256999999999, -14.852989, -13.622152, -12.190212000000002, -11.507582999999997, -11.380254, -11.497391, -11.161045999999999, -10.695489000000002, -10.941875000000003, -12.407989999999998, -14.364522000000001, -16.917876000000007, -19.712908, -22.989764, -26.451822, -30.013195999999994, -34.706407000000006, -40.411936, -40.158193999999995, -34.249373999999996, -30.708345, -28.387576000000003, -26.976463000000003, -25.924644999999998, -24.934693000000003, -24.034977999999995, -23.590517, -23.433761000000004, -23.265680000000003, -22.533535999999998, -22.552397999999997, -23.633767, -24.841085999999997, -25.458229999999993, -26.506420999999996, -27.78743500000001, -29.549673999999996, -30.760239999999996, -30.450096999999992,-30.450096999999992]
# Left back speaker position
leftback_eq_curve_left=[-7.339929999999995,-7.339929999999995, -5.376635, -3.855724000000002, -1.7137519999999995, -0.11853599999999886, 0.45937599999999534, 0.7619950000000024, 1.207484000000001, 0.6232390000000017, -0.6193219999999968, -1.5441819999999993, -2.5846170000000015, -3.650942999999998, -3.310514999999995, -2.851253, -2.9250899999999973, -2.160772999999999, -1.7819330000000022, -2.1231750000000034, -1.6633110000000002, -0.8961010000000016, -0.5886539999999982, -0.9480409999999964, -1.2115630000000053, -1.9521969999999982, -3.5636950000000027, -5.891209999999994, -8.884003, -11.610627999999998, -13.226177, -14.665154000000001, -15.672857999999998, -15.717958000000003, -15.551284000000003, -14.674253, -13.141389000000004, -11.483275000000006, -9.797967999999997, -8.264477, -6.627704000000001, -5.255563000000002, -4.704128000000004, -5.145234000000002, -5.454074999999996, -5.650332999999996, -6.145308, -6.663379000000006, -6.968034000000003, -6.801529000000002, -6.6901009999999985, -6.9388369999999995, -7.041483000000007, -6.544922, -6.051347999999997, -5.851528000000002, -5.803776999999997, -5.397247999999998, -4.628532, -3.7846880000000027, -3.036358, -2.5314639999999997, -2.890032000000005, -3.6472709999999964, -3.894359999999999, -3.073654999999995, -1.5313850000000002, 0.2640430000000009, 2.0715320000000013, 3.9283309999999965, 5.678476, 7.003, 8.013665000000003, 8.824637999999997, 9.18517, 8.727448999999996, 7.516722999999999, 6.282672000000002, 5.421021, 4.8387569999999975, 3.979184, 3.0943219999999982, 2.439867000000003, 1.2205299999999966, -0.21524200000000349, -1.496971000000002, -1.5934969999999993, -1.111032999999999, -0.5166960000000032, 0.07340400000000358, 0.7088489999999972, 1.0755599999999994, 1.055531000000002, 0.40028099999999966, -1.0654910000000015, -3.1188939999999974, -5.230058999999997, -6.025192000000004, -6.500077999999995, -7.164946999999998, -8.601823000000003, -10.479543, -13.037229000000004, -16.328727, -19.324698999999995, -18.544865, -15.088675000000002, -11.81055, -9.019759, -6.778007000000002, -5.267552000000002, -4.105238999999997, -3.2782139999999984, -3.1434759999999997, -3.7509919999999966, -4.831406999999999, -5.803275000000006, -6.867094000000002, -7.988068999999996, -10.027400999999998, -12.867732000000004, -15.985963999999996, -19.543980999999995, -22.475581999999996, -24.170364999999997, -24.801795, -25.765687, -25.682790000000004,-25.682790000000004]
leftback_eq_curve_right=[-8.377736999999996,-8.377736999999996, -6.928348, -7.102941000000001, -6.758023999999999, -6.633116000000001, -7.544023000000003, -6.499392999999998, -4.782429999999998, -3.7894759999999934, -4.288904000000002, -4.804963000000001, -5.467779, -6.422932000000003, -7.256316999999996, -9.101980999999995, -10.199207000000001, -9.455143, -9.123778999999999, -8.996694000000005, -7.890009000000006, -6.674288000000004, -5.488762000000001, -4.935668999999997, -4.879021999999999, -4.917726999999999, -5.633289000000005, -6.300231999999994, -7.097124999999998, -7.916944000000001, -8.731776999999994, -9.426029999999997, -9.867320999999997, -10.700943000000002, -11.846224, -12.879169000000005, -14.043424000000002, -15.004491000000002, -15.338970000000003, -15.207072000000004, -14.557748000000004, -13.927029000000005, -13.992572000000003, -14.747112000000001, -15.612451, -16.443464999999996, -16.966006999999998, -17.405641000000003, -17.712671, -17.516791000000005, -17.120951000000005, -17.104647999999997, -17.592232000000003, -17.577530000000003, -17.584778999999997, -16.904315000000004, -15.714976999999998, -14.296427999999999, -13.211433, -12.231227000000004, -11.043121, -9.188226999999998, -7.234342000000005, -6.422990999999996, -6.565399999999997, -7.383505999999997, -8.228507, -8.505111, -8.236694, -7.552292000000001, -6.622191999999998, -5.822997999999998, -5.147188999999997, -4.546455000000002, -4.158783, -4.245169000000004, -5.243870000000001, -6.5141690000000025, -7.622306000000002, -8.621711000000005, -9.721066, -10.839710000000004, -11.340363999999994, -12.025415000000002, -12.992048000000004, -13.916069, -14.199206999999994, -13.985084999999998, -13.850093999999999, -13.866847, -13.803470000000004, -14.071331, -14.167429999999996, -14.302702000000004, -14.923052000000006, -15.0976, -14.411779000000003, -13.667000999999999, -13.604416999999998, -13.414504999999998, -13.112270000000002, -12.820411999999997, -12.972216000000003, -13.279275000000005, -13.568431999999994, -13.797857999999998, -13.771479, -13.789010999999995, -13.464738000000004, -13.150692, -13.220562000000001, -13.011122999999998, -12.233242999999995, -11.460541, -10.582845999999996, -9.828882999999998, -9.001921000000003, -8.611266, -8.686268999999996, -9.438490000000002, -10.783949, -12.022891999999999, -13.379314999999998, -14.607931, -15.352677, -16.652741000000006, -18.295762999999994, -19.170658999999993,-19.170658999999993]
# Right front speaker position
rightfront_eq_curve_left=[-9.233398000000001,-9.233398000000001, -8.240777999999999, -6.943874000000001, -6.443821999999997, -7.652152000000001, -10.102838000000006, -11.505103999999996, -8.952629000000002, -6.348475999999998, -4.207926999999998, -4.4457200000000014, -6.120023000000003, -6.605880999999997, -7.0431349999999995, -7.276052999999997, -7.841992999999995, -8.858122000000002, -9.742740000000005, -10.862084000000003, -11.705045000000005, -10.809691, -8.548153, -6.770474999999998, -5.690401000000001, -5.104405, -4.738835999999999, -5.782561999999999, -7.433211, -8.475459, -9.886322999999997, -11.050176, -11.912550000000003, -12.752287000000003, -13.233012000000002, -13.558301, -13.720925000000001, -13.498547000000002, -13.347999999999999, -13.529278000000005, -13.971448000000002, -15.166008000000005, -17.023129000000004, -18.759769, -20.215343999999995, -20.735089000000002, -21.079577, -21.378469000000003, -21.350052000000005, -21.069304000000002, -21.473632000000002, -21.673271, -21.060586, -20.801552, -20.441921999999998, -19.882147000000003, -18.687654000000002, -17.190333000000003, -16.037950000000002, -14.717854000000003, -13.981785000000002, -14.636078999999995, -17.829464, -24.646246999999995, -23.867669999999997, -18.472414999999998, -15.239440000000002, -12.980864999999994, -10.633675999999994, -8.601878, -6.505650000000003, -5.0214870000000005, -4.603448, -4.476029000000004, -4.7963200000000015, -5.681643000000001, -6.993889000000003, -8.703212, -9.992662000000003, -11.148129000000004, -12.657924999999999, -14.879690000000004, -16.499798, -17.299663000000002, -17.762396000000003, -17.848451000000004, -17.474596, -17.369853, -17.069738, -15.960099, -14.919552000000003, -13.969025000000002, -12.821585999999996, -10.783514000000004, -9.122297000000003, -8.446638999999998, -9.135406000000003, -10.48957, -11.385770999999998, -12.221704000000003, -13.882972000000002, -16.460627000000002, -19.866513000000005, -23.324940000000005, -26.74205, -28.998098, -28.825021, -29.217780999999995, -30.627584, -33.19650500000001, -35.854364000000004, -36.318673999999994, -36.697179, -38.140626, -36.44347199999999, -31.434281999999996, -28.737136, -27.487785000000002, -26.333127999999995, -25.499923000000003, -25.451104, -25.921098999999998, -27.431403999999993, -28.950498000000003, -29.173350000000006, -29.097482, -28.658395, -28.020954999999994,-28.020954999999994]
rightfront_eq_curve_right=[-9.974302999999999,-9.974302999999999, -6.478799000000002, -4.031976999999998, -2.420187999999996, -1.9424320000000037, -2.3123610000000028, -2.325164000000001, -0.42801500000000203, 1.1434450000000034, 2.6329659999999997, 2.8758339999999976, 1.5909000000000013, 1.0303220000000017, -0.23032099999999645, -1.5229229999999987, -1.9371399999999994, -2.671953000000002, -2.288201000000001, -1.0046500000000052, 0.9024569999999983, 2.800137999999997, 4.706802, 5.946686, 6.424862999999998, 6.737586, 6.518398999999999, 4.9493870000000015, 3.4959140000000026, 3.1208269999999985, 2.6579970000000017, 2.231529000000002, 1.9952490000000012, 1.5648839999999993, 1.0823099999999997, 0.5296269999999978, 0.4701399999999971, 0.8665959999999977, 1.1021469999999987, 1.3139899999999969, 1.2170009999999962, 0.7359559999999981, 0.10656799999999578, -0.8030940000000015, -1.8048199999999994, -2.422041, -2.7126889999999975, -3.033072000000004, -3.714371, -4.201235000000004, -4.884908000000003, -5.606000999999999, -6.659296000000005, -8.182469000000005, -9.537002999999999, -10.481674000000005, -11.629207000000001, -11.695779000000002, -10.221864000000004, -8.054526000000003, -6.109065000000001, -4.598663999999999, -4.305042, -5.690207999999998, -7.982289999999999, -7.450502999999998, -5.106826000000005, -3.2503109999999964, -1.8708249999999964, -0.7749260000000007, 0.22303099999999887, 1.3972860000000011, 2.7624920000000017, 3.962267999999998, 4.789303999999998, 5.117099999999997, 4.900117999999999, 4.229469999999999, 3.4122009999999996, 2.961468, 2.2257730000000002, 0.6789469999999973, -0.6946929999999938, -2.1862660000000034, -3.8107690000000005, -5.265852000000002, -5.8040419999999955, -5.744438000000002, -4.975490000000001, -3.863517999999999, -3.269117999999999, -3.549275999999999, -4.456151999999996, -3.5540889999999976, 0.24501399999999762, 3.9767980000000023, 6.274421, 7.092514999999999, 6.317478000000005, 4.318460000000002, 1.401410999999996, -2.1075030000000012, -4.418120000000002, -4.249109000000004, -3.6759559999999993, -3.629393999999998, -4.423031999999999, -6.104607999999999, -8.315055000000001, -10.766193999999999, -13.079643000000004, -14.318450999999996, -14.085718, -13.069544, -12.169080999999998, -11.934148, -12.607499000000004, -13.796901000000005, -13.690916999999999, -12.412402, -11.660290000000003, -11.405473, -11.979796999999998, -13.324916000000002, -15.194703000000004, -17.480784, -20.403608000000006, -23.280075000000004,-23.280075000000004]
# Right back speaker position
rightback_eq_curve_left=[-8.53152,-8.53152, -7.938957000000002, -7.269750000000002, -6.438117999999996, -5.936109000000002, -6.979958000000003, -7.340778, -6.460417999999997, -5.813603999999998, -3.8467229999999972, -4.067551999999999, -5.314577999999997, -6.343800999999999, -7.493589, -8.730846999999997, -9.859637999999997, -9.775551, -9.862548000000004, -10.859043, -10.382828000000003, -8.834564, -7.148150999999999, -5.939889000000001, -5.026049, -4.605590999999997, -4.704568999999999, -6.316755999999998, -8.611033999999997, -10.333756999999999, -11.717133999999994, -12.680343, -13.102246999999998, -13.188546000000002, -13.257792000000002, -13.310328000000005, -13.568468000000003, -14.038963000000003, -14.460456, -15.450285000000001, -17.027631000000007, -18.797983000000002, -19.680051000000006, -20.216968, -20.987716, -21.386426, -21.681187, -22.692226000000005, -24.311618000000003, -25.277763, -25.621326000000003, -23.389266, -22.131398000000004, -21.753466000000003, -21.305214999999997, -21.080459000000005, -20.174151000000002, -19.410382, -17.830863, -15.921686000000001, -14.241147000000005, -13.596468999999999, -14.603177000000002, -15.445831999999996, -14.913249999999998, -13.914949999999997, -12.996401000000006, -12.143300999999994, -11.055716999999994, -9.982034000000006, -8.959136999999998, -8.405808999999998, -8.112136, -8.066321000000002, -8.718074999999999, -9.863600000000005, -11.205688000000002, -12.185045000000002, -13.227153999999999, -14.144902000000002, -15.570993000000001, -18.009701, -20.255198, -22.260822000000005, -23.776083, -25.614454000000002, -26.445715, -27.007426000000002, -26.516870000000004, -24.132511, -21.251453000000005, -18.745692, -16.726009999999995, -14.415275999999999, -12.261016000000005, -10.807552000000001, -10.050625000000004, -10.033536000000005, -10.989621999999997, -11.992984, -13.061181000000005, -14.035683999999996, -15.069912000000002, -15.916357000000005, -16.449768, -17.130536, -18.096628000000003, -19.195634, -19.979767000000002, -20.791295000000005, -21.308420000000005, -21.418587000000002, -21.462489999999995, -21.215138000000003, -21.194111999999997, -21.861804, -22.669499000000002, -23.924124000000006, -25.887052999999995, -27.832518, -29.392013000000006, -30.847499999999997, -30.967002, -30.234028000000002, -30.282148, -30.581044000000006, -30.870101000000005, -30.577988999999995, -30.577988999999995]
rightback_eq_curve_right=[-8.411788000000001,-8.411788000000001, -4.872700000000002, -2.2631820000000005, -0.2632679999999965, 0.8148059999999973, 0.9139789999999977, 1.8207270000000015, 2.3104510000000005, 1.5134120000000024, 1.2192499999999988, 0.10578600000000193, -2.2564300000000017, -3.2891809999999992, -3.303866999999997, -3.0965069999999955, -2.4130559999999974, -2.198416999999999, -1.7881259999999983, -1.8805850000000035, -2.3381400000000028, -2.454853, -2.9406649999999956, -3.877727, -5.329163000000001, -7.014665000000001, -9.86616, -13.484214999999999, -11.707611, -8.657223000000002, -7.406385999999998, -6.560418999999996, -5.932403000000001, -6.087847000000004, -5.877895000000002, -5.585829000000004, -4.936416999999999, -3.8904720000000026, -2.6434789999999992, -1.6986270000000019, -1.114442000000004, -0.8067670000000007, -1.3152820000000034, -2.396698999999998, -3.1206069999999997, -3.5874239999999986, -3.918565000000001, -4.13664, -3.885704000000004, -3.451858999999999, -3.630476999999999, -3.9538050000000027, -4.197769000000001, -4.5060199999999995, -5.0251909999999995, -5.793663000000002, -6.606814, -7.182547, -7.402203999999998, -7.211449999999999, -6.889631999999999, -6.3726409999999944, -6.334622000000003, -8.065387999999999, -12.221217999999993, -14.077652999999998, -8.838574000000001, -4.913640999999998, -2.0244439999999955, 0.4307269999999974, 2.388587000000001, 3.9468499999999977, 5.094792000000002, 5.875384999999998, 6.294755999999996, 6.249913999999997, 5.958653999999999, 5.5037020000000005, 4.655998, 3.690527999999997, 2.385010000000001, 0.32963799999999566, -1.447146999999994, -2.951405000000001, -4.029858000000004, -4.539878000000002, -4.704808999999997, -5.094127999999998, -5.104548999999999, -4.9459990000000005, -5.004856000000004, -4.720728999999999, -3.8404309999999953, -2.7356130000000007, -1.4329530000000048, -0.24436099999999783, 0.36446699999999765, 0.05869399999999558, -1.3512759999999986, -3.303258999999997, -5.809885000000001, -8.261740000000003, -9.573671000000004, -9.396302000000006, -8.790357999999998, -8.259391, -8.218131999999997, -8.687770999999998, -9.406094000000003, -10.012306000000002, -10.372029000000005, -10.476103000000002, -10.239121999999995, -9.670338999999998, -8.650344999999994, -7.695233999999999, -6.776628000000002, -6.123736000000001, -5.973887999999995, -6.404927000000001, -7.797448000000003, -9.364281999999996, -11.140256999999998, -13.108998999999997, -14.851416, -16.441644999999994, -17.845168, -18.724203999999993,-18.724203999999993]
# Back speaker
back_eq_curve_left=[2.554226,2.554226, -9.671655999999999, -23.020085, -29.635262999999995, -34.108022999999996, -37.59212300000001, -40.708606, -43.058659000000006, -45.16509099999999, -47.358529000000004, -49.195060999999995, -50.938672, -52.76135300000001, -54.04022, -55.487143, -56.810541, -58.194359999999996, -59.33225100000001, -60.237778000000006, -61.10037200000001, -61.886356, -62.672053999999996, -63.620419, -64.445463, -65.065814, -65.71192200000002, -66.470562, -67.259469, -67.66111599999999, -67.81792999999999, -67.838657, -67.730604, -67.753773, -67.730018, -67.87731500000001, -67.83046300000001, -67.61318700000001, -67.59282400000001, -67.777388, -67.85999000000001, -67.577094, -67.471957, -67.595576, -67.600224, -67.728758, -67.653137, -67.529732, -67.352431, -67.521309, -67.629958, -67.595624, -67.874008, -67.70696000000001, -67.60901, -67.56979100000001, -67.60729, -67.553987, -67.414549, -67.485517, -67.645037, -67.58722499999999, -67.582464, -67.662713, -67.61466999999999, -67.535222, -67.643486, -67.658646, -67.714234, -67.64271500000001, -67.622605, -67.685147, -67.54448099999999, -67.526186, -67.544572, -67.565361, -67.593226, -67.516948, -67.43806000000001, -67.374158, -67.414136, -67.535642, -67.518981, -67.660988, -67.568938, -67.592455, -67.44181, -67.487566, -67.427303, -67.55382399999999, -67.694231, -67.617531, -67.63511299999999, -67.500633, -67.509663, -66.907689, -66.602923, -66.159709, -65.692982, -65.396072, -65.203055, -64.86440300000001, -64.28826900000001, -64.053495, -63.97169099999999, -63.474894, -63.075503999999995, -62.793476999999996, -62.603561000000006, -62.358813000000005, -62.367622, -62.167970000000004, -62.028231, -61.812008000000006, -61.59226399999999, -61.366804, -60.823175000000006, -60.341722, -59.444791, -58.400739, -57.29745700000001, -55.559084999999996, -53.39253399999999, -50.770953, -47.681502, -43.731896000000006, -39.244298, -34.26495499999999,-34.26495499999999]
back_eq_curve_right=[2.643345,2.643345, -9.582633999999999, -22.931563000000004, -29.5469, -34.02013900000001, -37.501374000000006, -40.616907, -42.971051, -45.078329999999994, -47.269223999999994, -49.097826999999995, -50.847094, -52.685526, -53.954725, -55.385785999999996, -56.723433, -58.11843699999999, -59.24613300000001, -60.15096700000001, -61.02177300000001, -61.783689, -62.59345199999999, -63.518772999999996, -64.376745, -65.002673, -65.617918, -66.358138, -67.162252, -67.66111599999999, -67.81792999999999, -67.838657, -67.730604, -67.753773, -67.730018, -67.87731500000001, -67.83046300000001, -67.61318700000001, -67.59282400000001, -67.777388, -67.85999000000001, -67.577094, -67.471957, -67.595576, -67.600224, -67.728758, -67.653137, -67.529732, -67.352431, -67.521309, -67.629958, -67.595624, -67.874008, -67.70696000000001, -67.60901, -67.56979100000001, -67.60729, -67.553987, -67.414549, -67.485517, -67.645037, -67.58722499999999, -67.582464, -67.662713, -67.61466999999999, -67.535222, -67.643486, -67.658646, -67.714234, -67.64271500000001, -67.622605, -67.685147, -67.54448099999999, -67.526186, -67.544572, -67.565361, -67.593226, -67.516948, -67.43806000000001, -67.374158, -67.414136, -67.535642, -67.518981, -67.660988, -67.568938, -67.592455, -67.44181, -67.487566, -67.427303, -67.55382399999999, -67.694231, -67.617531, -67.63511299999999, -67.500633, -67.208213, -66.780315, -66.39054900000001, -66.037648, -65.73954499999999, -65.44342800000001, -65.067215, -64.56298899999999, -64.20540500000001, -64.11788000000001, -63.958045999999996, -63.564455, -63.210357, -62.993475000000004, -62.798573999999995, -62.41409600000001, -62.25931800000001, -62.211306, -62.167874000000005, -61.707432, -61.448021000000004, -61.22695900000001, -60.712728999999996, -60.226008, -59.448494000000004, -58.482034, -57.268024, -55.493144, -53.378336999999995, -50.926437, -47.57620500000001, -43.64128099999999, -39.434989, -34.50383899999999,-34.50383899999999]

####################### Functions ############################
#Frequency domain
def eq_3d_process(input_data):
	left_data=input_data[0]
	right_data=input_data[1]
	#Progress bar related
	global frame
	frame+=1
	# print_progress(frame, total_frames, decimals = 0, barLength = 50)
	#EQ related
	global leftfront_eq_curve_left
	global leftfront_eq_curve_right
	global leftback_eq_curve_left
	global leftback_eq_curve_right
	global rightfront_eq_curve_left
	global rightfront_eq_curve_right
	global rightback_eq_curve_left
	global rightback_eq_curve_right
	global back_eq_curve_left
	global back_eq_curve_right
	global effect_frame
	#Checking the effect
	if(effect_frame>=0 and effect_frame<1000):	
		eq_curve_left=leftfront_eq_curve_left
		eq_curve_right=leftfront_eq_curve_right
	if(effect_frame>=1000 and effect_frame<2000):
		eq_curve_left=leftback_eq_curve_left
		eq_curve_right=leftback_eq_curve_right
	if(effect_frame>=2000 and effect_frame<3000):	
		eq_curve_left=back_eq_curve_left
		eq_curve_right=back_eq_curve_right
	if(effect_frame>=3000 and effect_frame<4000):	
		eq_curve_left=rightback_eq_curve_left
		eq_curve_right=rightback_eq_curve_right
	if(effect_frame>=4000 and effect_frame<5000):
		eq_curve_left=rightfront_eq_curve_left
		eq_curve_right=rightfront_eq_curve_right
	if(effect_frame>=4999): effect_frame=0
	else: effect_frame+=1

	#Applying gains
	output_left=[]
	output_right=[]
	for i in range(len(left_data)):
		output_left.append(left_data[i]*(10**(eq_curve_left[i]/20)))
		output_right.append(right_data[i]*(10**(eq_curve_right[i]/20)))
	output_data=[output_left,output_right]
	return output_data


####################### Calling ############################
left_in,right_in=wave_file_process("../ExampleMusic/Clean Male Speech Stereo.wav",block_size=32,stereo=True,freq_proc_func=eq_3d_process)
left=np.asarray(left_in, dtype=np.float32)
right=np.asarray(right_in, dtype=np.float32)
data=np.vstack((left, right)).T
wav.write("3d_test_out.wav",fs,data)
#print(frame)