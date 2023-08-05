import IRACCGateway

ac_list = IRACCGateway.connect()
print(ac_list)

new_status = ac_list[4]
new_status.switch_status = IRACCGateway.protocol.SwitchStatus.ON
IRACCGateway.push_status(new_status)