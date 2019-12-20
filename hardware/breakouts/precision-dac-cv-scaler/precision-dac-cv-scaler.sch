EESchema Schematic File Version 4
LIBS:precision-dac-cv-scaler-cache
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L precision-dac-cv-scaler:OPA4197 U1
U 1 1 5DD8C612
P 4050 1550
F 0 "U1" H 4350 1600 50  0000 L CNN
F 1 "OPA4197" H 4250 1500 50  0000 L CNN
F 2 "Package_SO:TSSOP-14_4.4x5mm_P0.65mm" H 4000 1650 50  0001 C CNN
F 3 "http://www.ti.com/product/OPA4197" H 4100 1750 50  0001 C CNN
	1    4050 1550
	1    0    0    -1  
$EndComp
Text GLabel 3250 1450 0    50   Input ~ 0
DAC_A
Wire Wire Line
	3250 1450 3750 1450
$Comp
L Device:R R8
U 1 1 5DD8DA7A
P 4700 1550
F 0 "R8" V 4493 1550 50  0000 C CNN
F 1 "1k" V 4584 1550 50  0000 C CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 4630 1550 50  0001 C CNN
F 3 "~" H 4700 1550 50  0001 C CNN
	1    4700 1550
	0    1    1    0   
$EndComp
$Comp
L Device:R R4
U 1 1 5DD8E953
P 3600 1950
F 0 "R4" V 3400 1700 50  0000 L CNN
F 1 "2.91k 0.1%" V 3500 1700 50  0000 L CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 3530 1950 50  0001 C CNN
F 3 "~" H 3600 1950 50  0001 C CNN
	1    3600 1950
	0    1    1    0   
$EndComp
Wire Wire Line
	4350 1550 4550 1550
Wire Wire Line
	4200 1950 3750 1950
Wire Wire Line
	3750 1950 3750 1650
Wire Wire Line
	4850 1950 4850 1550
Wire Wire Line
	4500 1950 4850 1950
$Comp
L Device:R R6
U 1 1 5DD8E451
P 4350 1950
F 0 "R6" V 4143 1950 50  0000 C CNN
F 1 "9.09k 0.1%" V 4234 1950 50  0000 C CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 4280 1950 50  0001 C CNN
F 3 "~" H 4350 1950 50  0001 C CNN
	1    4350 1950
	0    1    1    0   
$EndComp
$Comp
L precision-dac-cv-scaler:TMUX1134 U2
U 1 1 5DD9AB88
P 2050 4950
F 0 "U2" H 2050 5667 50  0000 C CNN
F 1 "TMUX1134" H 2050 5576 50  0000 C CNN
F 2 "Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm" H 1950 4800 50  0001 C CNN
F 3 "http://www.ti.com/product/TMUX1134" H 1950 4800 50  0001 C CNN
	1    2050 4950
	1    0    0    -1  
$EndComp
Text GLabel 1450 4800 0    50   Input ~ 0
RANGE_REF_A
Text GLabel 3450 1950 0    50   Input ~ 0
RANGE_REF_A
Connection ~ 3750 1950
Text GLabel 1450 4500 0    50   Input ~ 0
RANGE_A
$Comp
L power:GND #PWR0101
U 1 1 5DD9D797
P 1450 4600
F 0 "#PWR0101" H 1450 4350 50  0001 C CNN
F 1 "GND" V 1455 4472 50  0000 R CNN
F 2 "" H 1450 4600 50  0001 C CNN
F 3 "" H 1450 4600 50  0001 C CNN
	1    1450 4600
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5DD9E07B
P 1450 5100
F 0 "#PWR0102" H 1450 4850 50  0001 C CNN
F 1 "GND" V 1455 4972 50  0000 R CNN
F 2 "" H 1450 5100 50  0001 C CNN
F 3 "" H 1450 5100 50  0001 C CNN
	1    1450 5100
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 5DD9E3B4
P 2650 4600
F 0 "#PWR0103" H 2650 4350 50  0001 C CNN
F 1 "GND" V 2655 4472 50  0000 R CNN
F 2 "" H 2650 4600 50  0001 C CNN
F 3 "" H 2650 4600 50  0001 C CNN
	1    2650 4600
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 5DD9E90C
P 2650 5100
F 0 "#PWR0104" H 2650 4850 50  0001 C CNN
F 1 "GND" V 2655 4972 50  0000 R CNN
F 2 "" H 2650 5100 50  0001 C CNN
F 3 "" H 2650 5100 50  0001 C CNN
	1    2650 5100
	0    -1   -1   0   
$EndComp
Text GLabel 1450 4700 0    50   Input ~ 0
MID_RANGE_VREF
Text GLabel 1450 5200 0    50   Input ~ 0
MID_RANGE_VREF
Text GLabel 2650 5200 2    50   Input ~ 0
MID_RANGE_VREF
Text GLabel 2650 4700 2    50   Input ~ 0
MID_RANGE_VREF
Text GLabel 1450 5000 0    50   Input ~ 0
RANGE_B
Text GLabel 1450 5300 0    50   Input ~ 0
RANGE_REF_B
Text GLabel 2650 4500 2    50   Input ~ 0
RANGE_C
Text GLabel 2650 5000 2    50   Input ~ 0
RANGE_D
Text GLabel 2650 4800 2    50   Input ~ 0
RANGE_REF_C
Text GLabel 2650 5300 2    50   Input ~ 0
RANGE_REF_D
$Comp
L power:+3V3 #PWR0105
U 1 1 5DD9F5D2
P 1700 6100
F 0 "#PWR0105" H 1700 5950 50  0001 C CNN
F 1 "+3V3" H 1715 6273 50  0000 C CNN
F 2 "" H 1700 6100 50  0001 C CNN
F 3 "" H 1700 6100 50  0001 C CNN
	1    1700 6100
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 5DD9FF2C
P 2000 6100
F 0 "#PWR0106" H 2000 5850 50  0001 C CNN
F 1 "GND" H 2005 5927 50  0000 C CNN
F 2 "" H 2000 6100 50  0001 C CNN
F 3 "" H 2000 6100 50  0001 C CNN
	1    2000 6100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0107
U 1 1 5DDA015A
P 2100 5600
F 0 "#PWR0107" H 2100 5350 50  0001 C CNN
F 1 "GND" H 2105 5427 50  0000 C CNN
F 2 "" H 2100 5600 50  0001 C CNN
F 3 "" H 2100 5600 50  0001 C CNN
	1    2100 5600
	1    0    0    -1  
$EndComp
Text GLabel 5050 1550 2    50   Input ~ 0
OUT_A
Wire Wire Line
	4850 1550 5050 1550
Connection ~ 4850 1550
$Comp
L power:+2V5 #PWR0108
U 1 1 5DDA0E1C
P 900 2900
F 0 "#PWR0108" H 900 2750 50  0001 C CNN
F 1 "+2V5" H 915 3073 50  0000 C CNN
F 2 "" H 900 2900 50  0001 C CNN
F 3 "" H 900 2900 50  0001 C CNN
	1    900  2900
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 5DDA145A
P 900 3350
F 0 "R2" V 650 3300 50  0000 C CNN
F 1 "9.09k 0.1%" V 750 3250 50  0000 C CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 830 3350 50  0001 C CNN
F 3 "~" H 900 3350 50  0001 C CNN
	1    900  3350
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 5DDA2D8D
P 900 3050
F 0 "R1" V 650 3100 50  0000 C CNN
F 1 "4.70k 0.1%" V 750 3100 50  0000 C CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 830 3050 50  0001 C CNN
F 3 "~" H 900 3050 50  0001 C CNN
	1    900  3050
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0109
U 1 1 5DDA34F8
P 900 3500
F 0 "#PWR0109" H 900 3250 50  0001 C CNN
F 1 "GND" H 905 3327 50  0000 C CNN
F 2 "" H 900 3500 50  0001 C CNN
F 3 "" H 900 3500 50  0001 C CNN
	1    900  3500
	1    0    0    -1  
$EndComp
Text GLabel 1700 3300 2    50   Input ~ 0
MID_RANGE_VREF
Wire Wire Line
	1050 3200 900  3200
Connection ~ 900  3200
Text Notes 1700 3250 0    50   ~ 0
1.648V
$Comp
L precision-dac-cv-scaler:OPA4197 U1
U 2 1 5DDA7821
P 6800 1550
F 0 "U1" H 7100 1600 50  0000 L CNN
F 1 "OPA4197" H 7000 1500 50  0000 L CNN
F 2 "Package_SO:TSSOP-14_4.4x5mm_P0.65mm" H 6750 1650 50  0001 C CNN
F 3 "http://www.ti.com/product/OPA4197" H 6850 1750 50  0001 C CNN
	2    6800 1550
	1    0    0    -1  
$EndComp
Text GLabel 6000 1450 0    50   Input ~ 0
DAC_B
Wire Wire Line
	6000 1450 6500 1450
$Comp
L Device:R R14
U 1 1 5DDA782D
P 7450 1550
F 0 "R14" V 7243 1550 50  0000 C CNN
F 1 "1k" V 7334 1550 50  0000 C CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 7380 1550 50  0001 C CNN
F 3 "~" H 7450 1550 50  0001 C CNN
	1    7450 1550
	0    1    1    0   
$EndComp
$Comp
L Device:R R10
U 1 1 5DDA7837
P 6350 1950
F 0 "R10" V 6150 1700 50  0000 L CNN
F 1 "2.91k 0.1%" V 6250 1700 50  0000 L CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 6280 1950 50  0001 C CNN
F 3 "~" H 6350 1950 50  0001 C CNN
	1    6350 1950
	0    1    1    0   
$EndComp
Wire Wire Line
	7100 1550 7300 1550
Wire Wire Line
	6950 1950 6500 1950
Wire Wire Line
	6500 1950 6500 1650
Wire Wire Line
	7600 1950 7600 1550
Wire Wire Line
	7250 1950 7600 1950
$Comp
L Device:R R12
U 1 1 5DDA7852
P 7100 1950
F 0 "R12" V 6893 1950 50  0000 C CNN
F 1 "9.09k 0.1%" V 6984 1950 50  0000 C CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 7030 1950 50  0001 C CNN
F 3 "~" H 7100 1950 50  0001 C CNN
	1    7100 1950
	0    1    1    0   
$EndComp
Text GLabel 6200 1950 0    50   Input ~ 0
RANGE_REF_B
Connection ~ 6500 1950
Text GLabel 7800 1550 2    50   Input ~ 0
OUT_B
Wire Wire Line
	7600 1550 7800 1550
Connection ~ 7600 1550
$Comp
L precision-dac-cv-scaler:OPA4197 U1
U 3 1 5DDAE2F1
P 4000 2950
F 0 "U1" H 4300 3000 50  0000 L CNN
F 1 "OPA4197" H 4200 2900 50  0000 L CNN
F 2 "Package_SO:TSSOP-14_4.4x5mm_P0.65mm" H 3950 3050 50  0001 C CNN
F 3 "http://www.ti.com/product/OPA4197" H 4050 3150 50  0001 C CNN
	3    4000 2950
	1    0    0    -1  
$EndComp
Text GLabel 3200 2850 0    50   Input ~ 0
DAC_C
Wire Wire Line
	3200 2850 3700 2850
$Comp
L Device:R R7
U 1 1 5DDAE2FD
P 4650 2950
F 0 "R7" V 4443 2950 50  0000 C CNN
F 1 "1k" V 4534 2950 50  0000 C CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 4580 2950 50  0001 C CNN
F 3 "~" H 4650 2950 50  0001 C CNN
	1    4650 2950
	0    1    1    0   
$EndComp
$Comp
L Device:R R3
U 1 1 5DDAE307
P 3550 3350
F 0 "R3" V 3350 3100 50  0000 L CNN
F 1 "2.91k 0.1%" V 3450 3100 50  0000 L CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 3480 3350 50  0001 C CNN
F 3 "~" H 3550 3350 50  0001 C CNN
	1    3550 3350
	0    1    1    0   
$EndComp
Wire Wire Line
	4300 2950 4500 2950
Wire Wire Line
	4150 3350 3700 3350
Wire Wire Line
	3700 3350 3700 3050
Wire Wire Line
	4800 3350 4800 2950
Wire Wire Line
	4450 3350 4800 3350
$Comp
L Device:R R5
U 1 1 5DDAE322
P 4300 3350
F 0 "R5" V 4093 3350 50  0000 C CNN
F 1 "9.09k 0.1%" V 4184 3350 50  0000 C CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 4230 3350 50  0001 C CNN
F 3 "~" H 4300 3350 50  0001 C CNN
	1    4300 3350
	0    1    1    0   
$EndComp
Text GLabel 3400 3350 0    50   Input ~ 0
RANGE_REF_C
Connection ~ 3700 3350
Text GLabel 5000 2950 2    50   Input ~ 0
OUT_C
Wire Wire Line
	4800 2950 5000 2950
Connection ~ 4800 2950
$Comp
L precision-dac-cv-scaler:OPA4197 U1
U 4 1 5DDB22B0
P 6750 3000
F 0 "U1" H 7050 3050 50  0000 L CNN
F 1 "OPA4197" H 6950 2950 50  0000 L CNN
F 2 "Package_SO:TSSOP-14_4.4x5mm_P0.65mm" H 6700 3100 50  0001 C CNN
F 3 "http://www.ti.com/product/OPA4197" H 6800 3200 50  0001 C CNN
	4    6750 3000
	1    0    0    -1  
$EndComp
Text GLabel 5950 2900 0    50   Input ~ 0
DAC_D
Wire Wire Line
	5950 2900 6450 2900
$Comp
L Device:R R13
U 1 1 5DDB22B8
P 7400 3000
F 0 "R13" V 7193 3000 50  0000 C CNN
F 1 "1k" V 7284 3000 50  0000 C CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 7330 3000 50  0001 C CNN
F 3 "~" H 7400 3000 50  0001 C CNN
	1    7400 3000
	0    1    1    0   
$EndComp
$Comp
L Device:R R9
U 1 1 5DDB22BE
P 6300 3400
F 0 "R9" V 6100 3150 50  0000 L CNN
F 1 "2.91k 0.1%" V 6200 3150 50  0000 L CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 6230 3400 50  0001 C CNN
F 3 "~" H 6300 3400 50  0001 C CNN
	1    6300 3400
	0    1    1    0   
$EndComp
Wire Wire Line
	7050 3000 7250 3000
Wire Wire Line
	6900 3400 6450 3400
Wire Wire Line
	6450 3400 6450 3100
Wire Wire Line
	7550 3400 7550 3000
Wire Wire Line
	7200 3400 7550 3400
$Comp
L Device:R R11
U 1 1 5DDB22D1
P 7050 3400
F 0 "R11" V 6843 3400 50  0000 C CNN
F 1 "9.09k 0.1%" V 6934 3400 50  0000 C CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 6980 3400 50  0001 C CNN
F 3 "~" H 7050 3400 50  0001 C CNN
	1    7050 3400
	0    1    1    0   
$EndComp
Text GLabel 6150 3400 0    50   Input ~ 0
RANGE_REF_D
Connection ~ 6450 3400
Text GLabel 7750 3000 2    50   Input ~ 0
OUT_D
Wire Wire Line
	7550 3000 7750 3000
Connection ~ 7550 3000
$Comp
L precision-dac-cv-scaler:OPA4197 U1
U 5 1 5DDB3001
P 1150 1500
F 0 "U1" H 1150 1550 50  0000 L CNN
F 1 "OPA4197" H 1100 1450 50  0000 L CNN
F 2 "Package_SO:TSSOP-14_4.4x5mm_P0.65mm" H 1100 1600 50  0001 C CNN
F 3 "http://www.ti.com/product/OPA4197" H 1200 1700 50  0001 C CNN
	5    1150 1500
	1    0    0    -1  
$EndComp
$Comp
L power:-12V #PWR0110
U 1 1 5DDB4C3D
P 1050 2100
F 0 "#PWR0110" H 1050 2200 50  0001 C CNN
F 1 "-12V" H 1065 2273 50  0000 C CNN
F 2 "" H 1050 2100 50  0001 C CNN
F 3 "" H 1050 2100 50  0001 C CNN
	1    1050 2100
	-1   0    0    1   
$EndComp
$Comp
L power:+12V #PWR0111
U 1 1 5DDB542D
P 1050 900
F 0 "#PWR0111" H 1050 750 50  0001 C CNN
F 1 "+12V" H 1065 1073 50  0000 C CNN
F 2 "" H 1050 900 50  0001 C CNN
F 3 "" H 1050 900 50  0001 C CNN
	1    1050 900 
	1    0    0    -1  
$EndComp
$Comp
L Device:C C2
U 1 1 5DDB5788
P 900 1950
F 0 "C2" V 1150 1950 50  0000 C CNN
F 1 "0.1uF" V 1050 1950 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 938 1800 50  0001 C CNN
F 3 "~" H 900 1950 50  0001 C CNN
	1    900  1950
	-1   0    0    1   
$EndComp
Wire Wire Line
	1050 1800 900  1800
Wire Wire Line
	1050 1800 1050 2100
Connection ~ 1050 1800
$Comp
L Device:C C1
U 1 1 5DDBC116
P 900 1050
F 0 "C1" V 1150 1050 50  0000 C CNN
F 1 "0.1uF" V 1050 1050 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 938 900 50  0001 C CNN
F 3 "~" H 900 1050 50  0001 C CNN
	1    900  1050
	-1   0    0    1   
$EndComp
Wire Wire Line
	1050 1200 900  1200
Wire Wire Line
	1050 900  1050 1200
Connection ~ 1050 1200
$Comp
L Device:C C3
U 1 1 5DDC0A8E
P 1850 6000
F 0 "C3" V 2100 6000 50  0000 C CNN
F 1 "0.1uF" V 2000 6000 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 1888 5850 50  0001 C CNN
F 3 "~" H 1850 6000 50  0001 C CNN
	1    1850 6000
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1700 6100 1700 6000
Wire Wire Line
	2000 6000 2000 6100
Wire Wire Line
	2000 6000 2000 5600
Connection ~ 2000 6000
Wire Wire Line
	1900 5600 1700 5600
Wire Wire Line
	1700 5600 1700 6000
Connection ~ 1700 6000
$Comp
L power:+12V #PWR0112
U 1 1 5DDCC912
P 9850 4250
F 0 "#PWR0112" H 9850 4100 50  0001 C CNN
F 1 "+12V" V 9865 4378 50  0000 L CNN
F 2 "" H 9850 4250 50  0001 C CNN
F 3 "" H 9850 4250 50  0001 C CNN
	1    9850 4250
	0    -1   -1   0   
$EndComp
$Comp
L power:-12V #PWR0113
U 1 1 5DDCD0B5
P 9850 4350
F 0 "#PWR0113" H 9850 4450 50  0001 C CNN
F 1 "-12V" V 9865 4478 50  0000 L CNN
F 2 "" H 9850 4350 50  0001 C CNN
F 3 "" H 9850 4350 50  0001 C CNN
	1    9850 4350
	0    -1   -1   0   
$EndComp
$Comp
L power:+3V3 #PWR0114
U 1 1 5DDCD93B
P 9850 4450
F 0 "#PWR0114" H 9850 4300 50  0001 C CNN
F 1 "+3V3" V 9865 4578 50  0000 L CNN
F 2 "" H 9850 4450 50  0001 C CNN
F 3 "" H 9850 4450 50  0001 C CNN
	1    9850 4450
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0115
U 1 1 5DDCE268
P 9850 4650
F 0 "#PWR0115" H 9850 4400 50  0001 C CNN
F 1 "GND" V 9855 4522 50  0000 R CNN
F 2 "" H 9850 4650 50  0001 C CNN
F 3 "" H 9850 4650 50  0001 C CNN
	1    9850 4650
	0    1    1    0   
$EndComp
$Comp
L power:+2V5 #PWR0116
U 1 1 5DDCE3F0
P 9850 4550
F 0 "#PWR0116" H 9850 4400 50  0001 C CNN
F 1 "+2V5" V 9865 4678 50  0000 L CNN
F 2 "" H 9850 4550 50  0001 C CNN
F 3 "" H 9850 4550 50  0001 C CNN
	1    9850 4550
	0    -1   -1   0   
$EndComp
Text GLabel 9850 4750 0    50   Input ~ 0
DAC_A
Text GLabel 9850 4950 0    50   Input ~ 0
DAC_C
Text GLabel 9850 4850 0    50   Input ~ 0
DAC_B
Text GLabel 9850 5050 0    50   Input ~ 0
DAC_D
Text GLabel 9850 5550 0    50   Input ~ 0
OUT_A
Text GLabel 9850 5650 0    50   Input ~ 0
OUT_B
Text GLabel 9850 5750 0    50   Input ~ 0
OUT_C
Text GLabel 9850 5850 0    50   Input ~ 0
OUT_D
Text GLabel 9850 5150 0    50   Input ~ 0
RANGE_A
Text GLabel 9850 5250 0    50   Input ~ 0
RANGE_B
Text GLabel 9850 5350 0    50   Input ~ 0
RANGE_C
Text GLabel 9850 5450 0    50   Input ~ 0
RANGE_D
$Comp
L SparkFun-Connectors:CONN_20LOCK_LONGPADS J1
U 1 1 5DDD20D2
P 9950 4250
F 0 "J1" H 9722 5105 45  0000 R CNN
F 1 "CONN_20LOCK_LONGPADS" H 9722 5189 45  0000 R CNN
F 2 "SF Connectors:1X20_LOCK_LONGPADS" H 9950 6350 20  0001 C CNN
F 3 "" H 9950 4250 50  0001 C CNN
F 4 "XXX-00000" H 9722 5284 60  0000 R CNN "Field4"
	1    9950 4250
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0117
U 1 1 5DDE2875
P 900 2100
F 0 "#PWR0117" H 900 1850 50  0001 C CNN
F 1 "GND" H 905 1927 50  0000 C CNN
F 2 "" H 900 2100 50  0001 C CNN
F 3 "" H 900 2100 50  0001 C CNN
	1    900  2100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0118
U 1 1 5DDE2C8A
P 900 900
F 0 "#PWR0118" H 900 650 50  0001 C CNN
F 1 "GND" H 905 727 50  0000 C CNN
F 2 "" H 900 900 50  0001 C CNN
F 3 "" H 900 900 50  0001 C CNN
	1    900  900 
	-1   0    0    1   
$EndComp
$Comp
L precision-dac-cv-scaler:OPA197 U?
U 1 1 5DE4F866
P 1350 3300
F 0 "U?" H 1400 3450 50  0000 L CNN
F 1 "OPA197" H 1350 3150 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:TSOT-23-5_HandSoldering" H 1250 3100 50  0001 L CNN
F 3 "http://www.ti.com/product/OPA197" H 1500 3450 50  0001 C CNN
	1    1350 3300
	1    0    0    -1  
$EndComp
Wire Wire Line
	1050 3400 1050 3650
Wire Wire Line
	1050 3650 1650 3650
Wire Wire Line
	1650 3650 1650 3300
Wire Wire Line
	1700 3300 1650 3300
Connection ~ 1650 3300
$Comp
L power:+12V #PWR?
U 1 1 5DE56327
P 1250 3000
F 0 "#PWR?" H 1250 2850 50  0001 C CNN
F 1 "+12V" H 1265 3173 50  0000 C CNN
F 2 "" H 1250 3000 50  0001 C CNN
F 3 "" H 1250 3000 50  0001 C CNN
	1    1250 3000
	1    0    0    -1  
$EndComp
$Comp
L power:-12V #PWR?
U 1 1 5DE56824
P 1250 3700
F 0 "#PWR?" H 1250 3800 50  0001 C CNN
F 1 "-12V" H 1265 3873 50  0000 C CNN
F 2 "" H 1250 3700 50  0001 C CNN
F 3 "" H 1250 3700 50  0001 C CNN
	1    1250 3700
	-1   0    0    1   
$EndComp
Wire Wire Line
	1250 3700 1250 3600
Wire Notes Line
	1500 2500 1500 500 
Wire Notes Line
	1500 500  500  500 
Wire Notes Line
	500  2500 2500 2500
Wire Notes Line
	2500 500  8500 500 
Wire Notes Line
	8500 500  8500 4000
Wire Notes Line
	2500 500  2500 4000
Wire Notes Line
	500  4000 8500 4000
Wire Notes Line
	500  6450 3800 6450
Wire Notes Line
	3800 6450 3800 4000
Wire Notes Line
	500  500  500  6450
Text Notes 550  600  0    50   ~ 0
Op Amp Power
Text Notes 550  2600 0    50   ~ 0
Mid range voltage reference
Text Notes 550  4100 0    50   ~ 0
Range switching IC
Text Notes 550  4200 0    39   ~ 0
Switches between 0v and 1.648v
Text Notes 2550 600  0    50   ~ 0
Range scaling amplifiers
Text Notes 2550 900  0    39   ~ 0
Scale 0-2.5v input from DACs to\n0 to +10v (when midrange ref is 0v)\nor\n-5 to +5v (when midrange ref is 1.648v)
Text Notes 3900 1150 0    39   ~ 0
Gain:\n- 0.1% resistors: 4.11 to 4.13\n- 1% resistors: 4.07 to 4.18\n\nVout max:\n- 0.1% resistors: 10.275v to 10.325v\n- 1% resistors: 10.175v to 10.450v
Text Notes 5050 800  0    39   ~ 0
Input voltage noise: 5.5nV/sqrtHz\nDAC ouput noise: 240nV/sqrtHz\nDAC output precision: 14bit
$EndSCHEMATC
