import IRACCGateway

ac_list = IRACCGateway.connect()
print(ac_list)
print(IRACCGateway.fetch_status())

new_status = ac_list[4]
new_status.switch_status = IRACCGateway.protocol.SwitchStatus.ON
IRACCGateway.push_status(new_status)

print(IRACCGateway.fetch_outside_temperature())