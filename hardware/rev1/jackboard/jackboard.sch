EESchema Schematic File Version 4
LIBS:jackboard-cache
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Sol Jackboard"
Date "2020-01-15"
Rev "Rev1 v1"
Comp "Winterbloom"
Comment1 "Alethea Flowers"
Comment2 "thea.codes"
Comment3 "CC-BY-SA 4.0"
Comment4 ""
$EndDescr
Text GLabel 1050 1225 3    50   Input ~ 0
SWCLK
Text GLabel 2400 1225 3    50   Input ~ 0
D+
Text GLabel 2500 1225 3    50   Input ~ 0
D-
Text GLabel 1250 1225 3    50   Input ~ 0
NEOPIXEL
Wire Notes Line
	6900 6500 6900 7750
Wire Notes Line
	6900 6500 11200 6500
Text GLabel 3000 1225 3    50   Input ~ 0
GATE_A_OUT
Text GLabel 2900 1225 3    50   Input ~ 0
GATE_B_OUT
Text GLabel 2800 1225 3    50   Input ~ 0
GATE_C_OUT
Text GLabel 2700 1225 3    50   Input ~ 0
GATE_D_OUT
Text GLabel 1450 1225 3    50   Input ~ 0
CV_A
Text GLabel 1550 1225 3    50   Input ~ 0
CV_B
Text GLabel 1650 1225 3    50   Input ~ 0
CV_C
Text GLabel 1750 1225 3    50   Input ~ 0
CV_D
Text GLabel 1150 1225 3    50   Input ~ 0
SWDIO
Text GLabel 2300 1225 3    50   Input ~ 0
Reset
$Comp
L power:+3V3 #PWR0173
U 1 1 5E2995DF
P 1350 1225
F 0 "#PWR0173" H 1350 1075 50  0001 C CNN
F 1 "+3V3" V 1350 1375 50  0000 L CNN
F 2 "" H 1350 1225 50  0001 C CNN
F 3 "" H 1350 1225 50  0001 C CNN
	1    1350 1225
	-1   0    0    1   
$EndComp
$Comp
L Connector:Conn_01x10_Female J2
U 1 1 5E674F2E
P 1350 1025
F 0 "J2" V 1515 955 50  0000 C CNN
F 1 "Conn_01x10_Female" V 1424 955 50  0000 C CNN
F 2 "Connectors:1X10_LOCK" H 1350 1025 50  0001 C CNN
F 3 "~" H 1350 1025 50  0001 C CNN
	1    1350 1025
	0    -1   -1   0   
$EndComp
$Comp
L Connector:Conn_01x10_Female J3
U 1 1 5E676944
P 2600 1025
F 0 "J3" V 2765 955 50  0000 C CNN
F 1 "Conn_01x10_Female" V 2674 955 50  0000 C CNN
F 2 "Connectors:1X10_LOCK" H 2600 1025 50  0001 C CNN
F 3 "~" H 2600 1025 50  0001 C CNN
	1    2600 1025
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0174
U 1 1 5E67E886
P 950 1225
F 0 "#PWR0174" H 950 975 50  0001 C CNN
F 1 "GND" V 950 1025 50  0000 C CNN
F 2 "" H 950 1225 50  0001 C CNN
F 3 "" H 950 1225 50  0001 C CNN
	1    950  1225
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0175
U 1 1 5E67F3D8
P 1850 1225
F 0 "#PWR0175" H 1850 975 50  0001 C CNN
F 1 "GND" V 1850 1025 50  0000 C CNN
F 2 "" H 1850 1225 50  0001 C CNN
F 3 "" H 1850 1225 50  0001 C CNN
	1    1850 1225
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0176
U 1 1 5E67F93D
P 2200 1225
F 0 "#PWR0176" H 2200 975 50  0001 C CNN
F 1 "GND" V 2200 1025 50  0000 C CNN
F 2 "" H 2200 1225 50  0001 C CNN
F 3 "" H 2200 1225 50  0001 C CNN
	1    2200 1225
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0177
U 1 1 5E67FCE8
P 2600 1225
F 0 "#PWR0177" H 2600 975 50  0001 C CNN
F 1 "GND" V 2600 1025 50  0000 C CNN
F 2 "" H 2600 1225 50  0001 C CNN
F 3 "" H 2600 1225 50  0001 C CNN
	1    2600 1225
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0178
U 1 1 5E68025F
P 3100 1225
F 0 "#PWR0178" H 3100 975 50  0001 C CNN
F 1 "GND" V 3100 1025 50  0000 C CNN
F 2 "" H 3100 1225 50  0001 C CNN
F 3 "" H 3100 1225 50  0001 C CNN
	1    3100 1225
	1    0    0    -1  
$EndComp
$Comp
L Connector:AudioJack2_SwitchT J4
U 1 1 5E2067B3
P 1050 2375
F 0 "J4" H 1082 2700 50  0000 C CNN
F 1 "AudioJack2_SwitchT" H 1082 2609 50  0000 C CNN
F 2 "jackboard:WQP-PJ301M-12_JACK" H 1050 2375 50  0001 C CNN
F 3 "~" H 1050 2375 50  0001 C CNN
	1    1050 2375
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 5E206F3F
P 1250 2275
F 0 "#PWR0101" H 1250 2025 50  0001 C CNN
F 1 "GND" V 1250 2075 50  0000 C CNN
F 2 "" H 1250 2275 50  0001 C CNN
F 3 "" H 1250 2275 50  0001 C CNN
	1    1250 2275
	0    -1   -1   0   
$EndComp
Text GLabel 1250 2375 2    50   Input ~ 0
CV_A
$Comp
L Connector:AudioJack2_SwitchT J6
U 1 1 5E20B585
P 2000 2375
F 0 "J6" H 2032 2700 50  0000 C CNN
F 1 "AudioJack2_SwitchT" H 2032 2609 50  0000 C CNN
F 2 "jackboard:WQP-PJ301M-12_JACK" H 2000 2375 50  0001 C CNN
F 3 "~" H 2000 2375 50  0001 C CNN
	1    2000 2375
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5E20B58B
P 2200 2275
F 0 "#PWR0102" H 2200 2025 50  0001 C CNN
F 1 "GND" V 2200 2075 50  0000 C CNN
F 2 "" H 2200 2275 50  0001 C CNN
F 3 "" H 2200 2275 50  0001 C CNN
	1    2200 2275
	0    -1   -1   0   
$EndComp
$Comp
L Connector:AudioJack2_SwitchT J8
U 1 1 5E20C307
P 2900 2375
F 0 "J8" H 2932 2700 50  0000 C CNN
F 1 "AudioJack2_SwitchT" H 2932 2609 50  0000 C CNN
F 2 "jackboard:WQP-PJ301M-12_JACK" H 2900 2375 50  0001 C CNN
F 3 "~" H 2900 2375 50  0001 C CNN
	1    2900 2375
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 5E20C30D
P 3100 2275
F 0 "#PWR0103" H 3100 2025 50  0001 C CNN
F 1 "GND" V 3100 2075 50  0000 C CNN
F 2 "" H 3100 2275 50  0001 C CNN
F 3 "" H 3100 2275 50  0001 C CNN
	1    3100 2275
	0    -1   -1   0   
$EndComp
$Comp
L Connector:AudioJack2_SwitchT J10
U 1 1 5E20D73C
P 3775 2375
F 0 "J10" H 3807 2700 50  0000 C CNN
F 1 "AudioJack2_SwitchT" H 3807 2609 50  0000 C CNN
F 2 "jackboard:WQP-PJ301M-12_JACK" H 3775 2375 50  0001 C CNN
F 3 "~" H 3775 2375 50  0001 C CNN
	1    3775 2375
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 5E20D742
P 3975 2275
F 0 "#PWR0104" H 3975 2025 50  0001 C CNN
F 1 "GND" V 3975 2075 50  0000 C CNN
F 2 "" H 3975 2275 50  0001 C CNN
F 3 "" H 3975 2275 50  0001 C CNN
	1    3975 2275
	0    -1   -1   0   
$EndComp
$Comp
L Connector:AudioJack2_SwitchT J1
U 1 1 5E20FAF1
P 1025 3100
F 0 "J1" H 1057 3425 50  0000 C CNN
F 1 "AudioJack2_SwitchT" H 1057 3334 50  0000 C CNN
F 2 "jackboard:WQP-PJ301M-12_JACK" H 1025 3100 50  0001 C CNN
F 3 "~" H 1025 3100 50  0001 C CNN
	1    1025 3100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0105
U 1 1 5E20FAF7
P 1225 3000
F 0 "#PWR0105" H 1225 2750 50  0001 C CNN
F 1 "GND" V 1225 2800 50  0000 C CNN
F 2 "" H 1225 3000 50  0001 C CNN
F 3 "" H 1225 3000 50  0001 C CNN
	1    1225 3000
	0    -1   -1   0   
$EndComp
$Comp
L Connector:AudioJack2_SwitchT J5
U 1 1 5E20FAFE
P 1975 3100
F 0 "J5" H 2007 3425 50  0000 C CNN
F 1 "AudioJack2_SwitchT" H 2007 3334 50  0000 C CNN
F 2 "jackboard:WQP-PJ301M-12_JACK" H 1975 3100 50  0001 C CNN
F 3 "~" H 1975 3100 50  0001 C CNN
	1    1975 3100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 5E20FB04
P 2175 3000
F 0 "#PWR0106" H 2175 2750 50  0001 C CNN
F 1 "GND" V 2175 2800 50  0000 C CNN
F 2 "" H 2175 3000 50  0001 C CNN
F 3 "" H 2175 3000 50  0001 C CNN
	1    2175 3000
	0    -1   -1   0   
$EndComp
$Comp
L Connector:AudioJack2_SwitchT J7
U 1 1 5E20FB0B
P 2875 3100
F 0 "J7" H 2907 3425 50  0000 C CNN
F 1 "AudioJack2_SwitchT" H 2907 3334 50  0000 C CNN
F 2 "jackboard:WQP-PJ301M-12_JACK" H 2875 3100 50  0001 C CNN
F 3 "~" H 2875 3100 50  0001 C CNN
	1    2875 3100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0107
U 1 1 5E20FB11
P 3075 3000
F 0 "#PWR0107" H 3075 2750 50  0001 C CNN
F 1 "GND" V 3075 2800 50  0000 C CNN
F 2 "" H 3075 3000 50  0001 C CNN
F 3 "" H 3075 3000 50  0001 C CNN
	1    3075 3000
	0    -1   -1   0   
$EndComp
$Comp
L Connector:AudioJack2_SwitchT J9
U 1 1 5E20FB18
P 3750 3100
F 0 "J9" H 3782 3425 50  0000 C CNN
F 1 "AudioJack2_SwitchT" H 3782 3334 50  0000 C CNN
F 2 "jackboard:WQP-PJ301M-12_JACK" H 3750 3100 50  0001 C CNN
F 3 "~" H 3750 3100 50  0001 C CNN
	1    3750 3100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0108
U 1 1 5E20FB1E
P 3950 3000
F 0 "#PWR0108" H 3950 2750 50  0001 C CNN
F 1 "GND" V 3950 2800 50  0000 C CNN
F 2 "" H 3950 3000 50  0001 C CNN
F 3 "" H 3950 3000 50  0001 C CNN
	1    3950 3000
	0    -1   -1   0   
$EndComp
Text GLabel 2200 2375 2    50   Input ~ 0
CV_B
Text GLabel 3100 2375 2    50   Input ~ 0
CV_C
Text GLabel 3975 2375 2    50   Input ~ 0
CV_D
Text GLabel 1225 3100 2    50   Input ~ 0
GATE_A_OUT
Text GLabel 2175 3100 2    50   Input ~ 0
GATE_B_OUT
Text GLabel 3075 3100 2    50   Input ~ 0
GATE_C_OUT
Text GLabel 3950 3100 2    50   Input ~ 0
GATE_D_OUT
$Comp
L Connector:USB_B J11
U 1 1 5E210782
P 4200 1275
F 0 "J11" H 4257 1742 50  0000 C CNN
F 1 "USB_B" H 4257 1651 50  0000 C CNN
F 2 "Connector_USB:USB_B_TE_5787834_Vertical" H 4350 1225 50  0001 C CNN
F 3 " ~" H 4350 1225 50  0001 C CNN
	1    4200 1275
	1    0    0    -1  
$EndComp
Text GLabel 4500 1375 2    50   Input ~ 0
D-
Text GLabel 4500 1275 2    50   Input ~ 0
D+
$Comp
L power:GND #PWR0109
U 1 1 5E212515
P 4100 1675
F 0 "#PWR0109" H 4100 1425 50  0001 C CNN
F 1 "GND" V 4100 1475 50  0000 C CNN
F 2 "" H 4100 1675 50  0001 C CNN
F 3 "" H 4100 1675 50  0001 C CNN
	1    4100 1675
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0110
U 1 1 5E2129DC
P 4200 1675
F 0 "#PWR0110" H 4200 1425 50  0001 C CNN
F 1 "GND" V 4200 1475 50  0000 C CNN
F 2 "" H 4200 1675 50  0001 C CNN
F 3 "" H 4200 1675 50  0001 C CNN
	1    4200 1675
	1    0    0    -1  
$EndComp
NoConn ~ 4500 1075
NoConn ~ 3975 2475
NoConn ~ 3100 2475
NoConn ~ 2200 2475
NoConn ~ 1250 2475
NoConn ~ 1225 3200
NoConn ~ 2175 3200
NoConn ~ 3075 3200
NoConn ~ 3950 3200
$Comp
L LED:NeoPixel_THT D1
U 1 1 5E2137A8
P 5350 2725
F 0 "D1" H 5694 2771 50  0000 L CNN
F 1 "NeoPixel_THT" H 5694 2680 50  0000 L CNN
F 2 "LED_THT:LED_D5.0mm-4_RGB" H 5400 2425 50  0001 L TNN
F 3 "https://www.adafruit.com/product/1938" H 5450 2350 50  0001 L TNN
	1    5350 2725
	1    0    0    -1  
$EndComp
Text GLabel 5050 2725 0    50   Input ~ 0
NEOPIXEL
NoConn ~ 5650 2725
$Comp
L power:GND #PWR0111
U 1 1 5E214B0E
P 5350 3025
F 0 "#PWR0111" H 5350 2775 50  0001 C CNN
F 1 "GND" V 5350 2825 50  0000 C CNN
F 2 "" H 5350 3025 50  0001 C CNN
F 3 "" H 5350 3025 50  0001 C CNN
	1    5350 3025
	1    0    0    -1  
$EndComp
$Comp
L power:+3V3 #PWR0112
U 1 1 5E2150B5
P 5350 2425
F 0 "#PWR0112" H 5350 2275 50  0001 C CNN
F 1 "+3V3" V 5350 2575 50  0000 L CNN
F 2 "" H 5350 2425 50  0001 C CNN
F 3 "" H 5350 2425 50  0001 C CNN
	1    5350 2425
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push SW1
U 1 1 5E5DC434
P 1500 4150
F 0 "SW1" H 1500 4435 50  0000 C CNN
F 1 "SW_Push" H 1500 4344 50  0000 C CNN
F 2 "Button_Switch_THT:SW_PUSH_6mm" H 1500 4350 50  0001 C CNN
F 3 "~" H 1500 4350 50  0001 C CNN
	1    1500 4150
	1    0    0    -1  
$EndComp
Text GLabel 1300 4150 0    50   Input ~ 0
Reset
$Comp
L power:GND #PWR0113
U 1 1 5E5DD193
P 1700 4150
F 0 "#PWR0113" H 1700 3900 50  0001 C CNN
F 1 "GND" V 1700 3950 50  0000 C CNN
F 2 "" H 1700 4150 50  0001 C CNN
F 3 "" H 1700 4150 50  0001 C CNN
	1    1700 4150
	0    -1   -1   0   
$EndComp
$EndSCHEMATC
