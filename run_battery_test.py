from korad import Kel103, KoradUdpComm, KelBatteryDischargeTest
comm = KoradUdpComm("10.11.1.16", "10.11.0.200")
kel = Kel103(comm)
test = KelBatteryDischargeTest(kel)
test.setup_for_test("cell1", True, 30, 2.6, 999)
test.run_test()
test.export_results()




bat_test_data = {
            'setting_id': 2,
            'max_current': 30,
            'set_current': 1,
            'voltage_cutoff': 3.5,
            'capacity_cutoff': 10,
            'time_cutoff': 10
        }
kel.set_battery_data(bat_test_data)